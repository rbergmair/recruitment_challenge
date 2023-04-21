% RB's Approach To SO1's Algorithm Challenge using Ideas from
  Bayesian and k-Nearest-Neighbor Classification
% Dr Richard Bergmair
% Oct-10 2015

Preface
=======

Notes on Style
--------------
So, this is my report on my approach to the algorithm challenge.
From my work with one of my previous clients, I'm quite used to doing a lot
of communication in written form and over the internet.  In particular, we
were using a ticketing system with a markup language in order to document
progress on the various tasks and projects we were working on, as well as
solicit comments and facilitate discussion.  I've decided to write this
document in a similar sort of style, writing it essentially the way I would
write an e-mail to a person who is well-known to me, who is an expert on the
subject matter under discussiona and who I would assume to give a
generally sympathetic reading to the document.

If you're trying to form an opinion on whether I can rise to the standard
of rigor common among scientists for published work, have a look at my web
page at [richard.bergmair.eu] for a proper publication list.

The Revolution Will Not Be Peer-Reviewed
----------------------------------------

I should stress that one of the features of this more informal style is the
general absence of citations and references of the kind that academics are
used to.
Wherever I actually use any outside resources or any outside documentation,
or whenever I have any pointers that I think might be helpful or interesting
to the reader, I do link to them.

But if, throughout this document, a reader forms the opinion that I am
expressing an idea that really, really, has a canonical reference that
should always go with it, and I don't put it in, then it's not for sheer
ignorance, but rather, it is a conscious decision on my part not to play
that game.  

For example, when I was finished with this software, and started writing
the report, I pondered slapping a label on it, such as "Bayesian k Nearest
Neighbors".  Putting that into Google, it turns out that someone has already
used the term as the title of [some slideshow].  As an academic, the onus
would now be on me, to try to figure out what they did, how that relates
to what I did, and then pretend like I was aware of their work and applied
it (even when there was independent discovery), or pretend like I was aware
of their work and saw a problem with it, justifying why I didn't apply
it, but when the solution to the problem is already on the table, then
IMHO it's not, in general, a good use of time to put a lot of work into
sorting out who invented the various ideas that ended up playing a role in
that solution.
A certain level of reflectiveness is however useful.  For example, when I
find myself using an idea a lot, I sometimes get sufficiently curious to
decide I want to make an effort to find out what it's called, who invented
it, and what other people have said about it, etc.  But what I'm trying to
say is that this is not a matter of principle, but rather that there needs
to be a conscious decision about whether or not that's a good use of time
in any particular case, especially in light of the fact that fly-fishing
is a good use of time, too.


More Pseudo-Philosophical Waffle
--------------------------------

Wearing my partitioner's hat, what I do is to apply the inventory of ideas
and techniques that my academic alter ego has picked up through the years
to try to understand the logic and the structure of the problem I'm trying
to solve.  That understanding more or less dictates a solution which is
the simplest solution to the problem.  If that solution is novel, then great.
If that solution is on page one of every textbook on the subject, then so be
it.  -- If you're a software developer, and you're confronted with a problem
that calls for a solution that is novel, and you can't see it, because you
lack the conceptual inventory, then that's weak.  If you're a dysfunctional
academic peddling a solution looking for a problem, and as a result, you
end up hallucinating complexity where none exists, then that's just as weak.
(See [Gsellmann's Weltmaschine]).  Okay, so that's that.

Solution vs. Exploration
------------------------

In this document, I will outline the solution to the SO1 algorithm challenge
that I came up with.  The purpose of the present document (`SOLUTION`) is to
tell you where that solution is located, and give you directions on how to get
there most efficiently, starting from a working knowledge of data science.
-- There is a separte
document (`EXPLORATION`) that deals with how I came to discover that route by
taking lots and lots of roads that ended up being dead ends, applying lots
and lots of analogies to problems I've dealt with in the past that sometimes
did, but often didn't apply here. --
A lot of readers won't be interested in reading about dead ends and about
similar problems that ended up not being helpful in solving this one.  So
it makes sense to put that in a separate document.

Incidentally, the same structure exists in the code.  There are two
separate Python projects (`so1rb` and `so1rb_explore`).
The project `so1rb_explore` is like "brainstorming" or like a "stream of
consciousness" stage in drafting some piece of creative writing.  It is
a sequence of self-contained scripts, each of which answers a simple
question about the data.  They do not share any common structure, but rather
they come about through a process of copying and pasting, which would not
normally be proper software engineering.  But the overarching idea here is
that you're trying to concentrate on the structure and the phenomena that are
in the data, not on the structure of the code, so you allow yourself to forget
about proper software engineering for the purpose of this exploration, so as
not to be distracted.

Then you start with a clean slate, and create a well-structured and reusable
piece of software that takes into account all and only those phenomena
actually exhibited by the data, with the structure of the code informed by
your knowledge of the structure of the data.  And that's what `so1rb` is.
--
If you skip straight to writing the code you're intending to be the ultimate
solution to the problem, then your starting point will essentially be a shot
in the dark.  As you try to improve upon a suboptimal situation, you'll find
yourself trying to add illumination by putting in lots of parameters,
switches, and debug-level code.  But at that stage, a lot of very basic
design choices will already have been made in a suboptimal way, and once
you've set all of your parameters and switches and deactivated all your
debug code, you'll end up with lots of orphaned code and unnecessary
complexity that makes it hard for people to read and understand and hence
to reuse that code in the future.



Structure of the Data & Feature Engineering
===========================================

Let's finally delve into the problem at hand, and start talking about the
data.  It's a CSV file, with the following columns

* $\mathrm{id}$ (which is also called $\mathtt{id}$ in the data) is, well,
  the identifier.  (You guessed that, didn't you?)
* $\mathrm{y}$ is the dependent variable, i.e. the class label we are trying
  to predict as part of the classification problem at hand.
* $\mathrm{C}$ (which is called $\mathtt{cid}$ in the data) is
  a number in the range $[1,30]$ and seems to represent a discrete
  symbol.  I'm assuming
  it stands for "categorical id" or so.
* Among the columns called $\mathtt{x}_1 \ldots \mathtt{x}_{100}$ in the data,
  there are 70 continuous-valued numeric columns, and 30 columns with
  values `0` or `1`.
  In what follows, I'll reindex these, so that
  $\mathrm{x}_i$ is the $i$-th of the continuous-valued features, and
  $\mathrm{b}_j$ is the $j$-th of the binary features
  (starting the indexing at one, in both cases).

The module `so1rb/so1rb_data/da_read.py` implements a reader that reads this
data format.

Throughout the rest of this section, I will describe the modules
under `so1rb_frontend`.  These are classes derived from `Frontend`,
and they all serve the purpose of preprocessing the data so as to
present it to the core classification algorithm in a suitable representation.

There are two stages to this:

* Decorrelation (= orthogonalization): So as to transform the data into
  a space in which features are as close as possible to pairwise mutually
  independent, which may or may not have the side effect of
  dimensionality reduction.
* Feature selection: So as to identify and remove any components in the
  decorrelated (orthogonalized) space, that are unrelated to the dependent
  variable $\mathrm{y}$.

I will start by describing the components that play a role here, and
then describe how to put them all together into a well-structured
feature engineering framework.


`BinaryFrontend`
----------------

The set of $30$ binary features
$\mathrm{b}_1, \mathrm{b}_2, \ldots, \mathrm{b}_{30}$
yields $2^{30} \approx 1\mathrm{G}$
combinations of values.
During the exploration stage of this project,
however, it turned out that, within a training sample of
$\approx 850\mathrm{k}$ data points, only $367$ combinations actually
appeared in data, which lead me to conclude that there is a rich set
of logical dependencies constraining the possibilities.  -- So there
seems to be plenty of scope here to achieve decorrelation and
dimensionality reduction through some kind of feature engineering.

To better understand the phenomenon at play, consider the following
example: In a table of horses, there might be a column $\mathrm{Gender}$,
taking on values $\mathrm{Stallion}$ or $\mathrm{Mare}$, and a column
$\mathrm{RegisteredStud}$, taking on values $\mathrm{Yes}$ or
$\mathrm{No}$.  Obviously, only a stallion can be a registered stud.

The type of feature engineering I'm suggesting here would combine this
into one column $\mathrm{StudbookStatus}$ taking on values
$\mathrm{RegisteredStud}$,
$\mathrm{UnregisteredStallion}$ or $\mathrm{Mare}$.
This would achieve decorrelation, meaning that the resulting
representation is better behaved with regard to the independence assumptions
that go into, for example, a Bayesian approach to the classification
problem.  It also achieves dimensionality reduction.

There is a drawback here: We're losing out on potentially
useful generalizations over data.  For example, the set of male horses
is a statistically and semantically coherent group, which we no longer
capture, since we're now cutting through that group by forcing the distinction
between registered studs and unregistered stallions.

In a scenario where there is very little data, this could lead to problems
if statistical cells become too small to allow for generalizations to become
significant.  But in the particular problem at hand, it does seem to me like
we have plenty of data relative to the data complexity of the classification
problem we're trying to solve, and that therefore we need not worry about
this.  So we would still have enough examples of registered studs and
unregistered stallions so that generalizations pertaining to male horses in
general will be able to take shape in a statistically significant manner
within each subgroup, even without the benefit of taking into account data
about male horses from the other subgroup.  But it remains true that this
lumping-together comes at a cost, so we wouldn't want to do it
unnecessarily.

Applying this idea back to our $30$ binary features, that means that we
wouldn't necessarily want to turn the binary features into just a single
categorical variable taking on 367 values, and disregard all internal
structure.  For example, it might well be that one of the binary features
is largely independent, with the 367 combinations breaking apart into a 
set of 183 combinations for the mutually dependent features, plus the value
zero for the independent one, and a set of 184 combinations for the
dependent features, plus the value one for the independent one.
It would, in such a case, be much preferable to allow the independent
feature to remain a distinct feature in its own right.

So what I did was to create a clustering method to try to
cluster the binary features accordingly.  In particular: The goal was
to partition the set of binary features into clusters, so that features
in the same clusters would be highly correlated with each other, but
uncorrelated to features in other clusters.

I used the information theoretic measure of [correlation] which is highly
related to [mutual information] and [entropy] in order to quantify how
correlated a binary feature was with another feature or with a set of
other features.

In particular, the method works as follows:

* Start with a set of binary features (initially the set of all features).
  Imagine them sitting in front of you in the middle of your desk.
* Among those features, identify that feature whose probability distribution
  yields the lowest correlation relative to the joint distribution of the
  remaining features.  So that is the feature which is the best candidate for
  "independent feature".  Remove that from the pile and put it on
  the left-hand side of your desk.
* Among the remaining features, identify the one whose probability
  distribution yields the lowest correlation with that feature on the
  left-hand side of your desk, and put it on the right-hand side of your desk.
* Look through the remaining features, one at a time.  For each feature
  do the following: Look at the correlation of that feature's probability
  distribution with the joint probability distribution of the features to
  your left.  And then also look at the correlation with the features to
  your right.  If it's more correlated with the ones on your left, add it
  to the pile of features on the left, otherwise the pile of features to
  the right.  If none of the two correlations exceed 50%, you add it to
  neither pile.
* After you're done with this, the set of features to your left and right
  will each be a cluster.  So you put each of them in its own drawer.
* Then you repeat the process with the features that remained in the
  middle of your desk which you didn't add to any pile because they weren't
  correlated enough.
* You keep repeating this, until there are no more features left on your
  desk.
* When you're done with this, each of your drawers will have a nice
  cluster of binary features sitting inside it.

In particular, the clusters that came out of the process were:

* $\mathrm{B}_1 = \langle \mathrm{b}_2 \rangle$
* $\mathrm{B}_2 = \langle \mathrm{b}_{10}, \mathrm{b}_{25} \rangle$
* $\mathrm{B}_3 = \langle \mathrm{b}_{1} \rangle$
* $\mathrm{B}_4 = \langle \mathrm{b}_{15} \rangle$
* $\mathrm{B}_5 = \langle \mathrm{b}_{27} \rangle$
* $\mathrm{B}_6 = \langle \mathrm{b}_{18} \rangle$
* $\mathrm{B}_7 = \langle \mathrm{b}_{22} \rangle$
* $\mathrm{B}_8 = \langle \mathrm{b}_{3},
                 \mathrm{b}_{4},
                 \mathrm{b}_{5},
                 \mathrm{b}_{6},
                 \mathrm{b}_{7},
                 \mathrm{b}_{8},
                 \mathrm{b}_{9},
                 \mathrm{b}_{11},
                 \mathrm{b}_{12},
                 \mathrm{b}_{13},
                 \mathrm{b}_{14},
                 \mathrm{b}_{16},
                 \mathrm{b}_{17},
                 \mathrm{b}_{19},
                 \mathrm{b}_{20},
                 \mathrm{b}_{21},
                 \mathrm{b}_{23},
                 \mathrm{b}_{24},
                 \mathrm{b}_{26},
                 \mathrm{b}_{28},
                 \mathrm{b}_{29},
                 \mathrm{b}_{30} \rangle$

Based on that, the `BinaryFrontend` will turn the 30-dimensional binary
input space into an 8-dimensional output space of categorical variables
by using binary encoding.

For example, if $\mathbf{b}_{10} = 1$ and
$\mathbf{b}_{25} = 0$,
then $\mathbf{B}_2 = 1*2^1 + 0*2^0 = 2$,
thus encoding the $2^2 = 4$ possible values for the combination of
$\mathrm{b}_{10}$ and $\mathrm{b}_{25}$.

For $\mathrm{B}_8$, which contains 22 binary features,
the number of possible combinations is in theory
$2^{22} \approx 4\mathrm{M}$, but since they are highly correlated
with each other, the number of values actually seen in data
will be much smaller.


`HomebrewContinuousFrontend`
----------------------------

We can now turn attention to the 70 continuous features
$\mathrm{x}_1, \mathrm{x}_2, \ldots, \mathrm{x}_{70}$.
During the exploration stage of this project, it turned out that some
pairs of dimensions show only weak correlations, while others show
strong correlations, either positive or negative.  Thinking of each
of the dimensions as being additively composed of information that
is useful to the classification problem at hand and of noise, results
suggested that there is a varying amount of noise on each of the
dimensions, with some dimensions possibly contributing nothing but
noise.  Handling the classification problem in the 70-dimensional
space directly seemed like the wrong approach.  Instead, it seemed
advisable to use some mechanism for dimensionality reduction that
would allow the noise component to cancel out.

The approach is, once again, based on the idea of partitioning the
set of features into clusters, so that features in the same cluster
would be highly correlated with each other, but uncorrelated to
features in other clusters.  In the output space resulting from
this technique, each cluster turns into a single dimension, the
value along that dimension being the average of the values along
the input dimensions in that cluster.

If, for example, the algorithm is considering as a working hypothesis,
the possibility that there might be two clusters
$\mathrm{X}_1
   = \lbrace \mathrm{x}_{1}, \mathrm{x}_{2} \rbrace$
and 
$\mathrm{X}_2
   = \lbrace \mathrm{x}_{4}, \mathrm{x}_{5}, \mathrm{x}_{6} \rbrace$,
then
$\mathbf{X}_1
   = \frac{1}{2} ( \mathbf{x}_{1} + \mathbf{x}_{2} )$
and
$\mathbf{X}_2
   = \frac{1}{3} ( \mathbf{x}_{4} + \mathbf{x}_{5} + \mathbf{x}_{6} )$.

In addition, there can be situations, where we flip the sign on a dimension
for purposes of computing the average.  For example, in the cluster
$\mathrm{X}_3 =
   \lbrace \mathrm{x}_{2}, -\mathrm{x}_{3}, \mathrm{x}_{9} \rbrace$,
the negative sign to $-\mathrm{x}_{3}$ would denote the fact that the
clustering algorithm observed a negative rather than a positive correlation
between $\mathrm{x}_{2}$ and $\mathrm{x}_{3}$, whereas the correlation between
$\mathrm{x}_{2}$ and $\mathrm{x}_{9}$ was positive.  In this case, the average
would be computed as 
$\mathbf{X}_3
   = \frac{1}{3} ( \mathbf{x}_{2} - \mathbf{x}_{3} + \mathbf{x}_{9} )$.

The hope is that, if a pair of features is correlated, the correlation
comes about because they both carry as an additive component the same piece
of information that is useful to the classification problem at hand, plus a
noise term that would cancel out when the average is computed.  For example,
if these are the returns on individual stocks, then one cluster might be
tech stocks, because they are all additively composed of tech sector risk,
plus idiosyncratic risk, whereas another cluster might be banking stocks,
because they are additively composed of banking sector risk, plus
idiosyncratic risk, etc.  If the classification at hand is a function of
sector risk, rather than the idiosyncratic risk on any particular stock,
then this would be the type of situation, where this kind of feature
engineering would do some good.  The added complexity of having to flip
signs sometimes would come about if, for example, these are stock options,
some of them being calls, and some of them being puts.  An IBM call would
have a positive return if the IBM stock has a positive return, whereas a
Microsoft put would have a negative return if the Microsoft stock has a
positive return.  So the negative correlation that might be observed between
an IBM call and a Microsoft put would indicate the sector risk portion,
but with an inverted sign.  If these were simply added together, the
interesting part would cancel out, instead of being amplified, so that's
why it would be necessary to flip the signs accordingly.

I will admit, at this point, that the evidence to suggest that the example
data in the classification problem at hand is of that type, is thin,
but the evidence to suggest any other kind of structure is just as thin, so
I decided to try this kind of feature engineering on this data, and see
where we end up.

The algorithm that creates the clusters works as follows: The starting
point is that each individual dimension is an individual cluster.
It then looks through all pairs of clusters, and merges the two which
have the highest correlation, subject to the fact that a correlation
of 0.33 is the minimum needed to justify merging.  This is repeatedly
done, until no two clusters can be merged.

The resulting set of clusters is as follows:

* $\mathrm{X}_1 = \lbrace \mathrm{x}_{24} \rbrace$
* $\mathrm{X}_2 = \lbrace -\mathrm{x}_{59}, \mathrm{x}_{38} \rbrace$
* $\mathrm{X}_3 = \lbrace -\mathrm{x}_{40}, \mathrm{x}_{22} \rbrace$
* $\mathrm{X}_4 = \lbrace -\mathrm{x}_{65}, \mathrm{x}_{7} \rbrace$
* $\mathrm{X}_5 = \lbrace -\mathrm{x}_{30}, \mathrm{x}_{23} \rbrace$
* $\mathrm{X}_6 = \lbrace -\mathrm{x}_{70},
                          -\mathrm{x}_{60},
                          \mathrm{x}_{47} \rbrace$
* $\mathrm{X}_7 = \lbrace$
  $-\mathrm{x}_{58},$
  $-\mathrm{x}_{55},$
  $-\mathrm{x}_{50},$
  $-\mathrm{x}_{43},$
  $-\mathrm{x}_{42},$
  $-\mathrm{x}_{36},$
  $-\mathrm{x}_{28},$
  $-\mathrm{x}_{27},$
  $-\mathrm{x}_{20},$
  $-\mathrm{x}_{8},$
  $-\mathrm{x}_{6},$
  $\mathrm{x}_{1},$
  $\mathrm{x}_{2},$
  $\mathrm{x}_{5},$
  $\mathrm{x}_{11},$
  $\mathrm{x}_{12},$
  $\mathrm{x}_{15},$
  $\mathrm{x}_{18},$
  $\mathrm{x}_{21},$
  $\mathrm{x}_{31},$
  $\mathrm{x}_{41},$
  $\mathrm{x}_{61} \rbrace$
* $\mathrm{X}_8 = \lbrace$
  $-\mathrm{x}_{69},$
  $-\mathrm{x}_{68},$
  $-\mathrm{x}_{64},$
  $-\mathrm{x}_{62},$
  $-\mathrm{x}_{57},$
  $-\mathrm{x}_{56},$
  $-\mathrm{x}_{53},$
  $-\mathrm{x}_{51},$
  $-\mathrm{x}_{44},$
  $-\mathrm{x}_{39},$
  $-\mathrm{x}_{37},$
  $-\mathrm{x}_{35},$
  $-\mathrm{x}_{29},$
  $-\mathrm{x}_{19},$
  $-\mathrm{x}_{13},$
  $-\mathrm{x}_9,$
  $\mathrm{x}_3,$
  $\mathrm{x}_4,$
  $\mathrm{x}_{10},$
  $\mathrm{x}_{14},$
  $\mathrm{x}_{16},$
  $\mathrm{x}_{17},$
  $\mathrm{x}_{25},$
  $\mathrm{x}_{26},$
  $\mathrm{x}_{32},$
  $\mathrm{x}_{33},$
  $\mathrm{x}_{34},$
  $\mathrm{x}_{45},$
  $\mathrm{x}_{46},$
  $\mathrm{x}_{48},$
  $\mathrm{x}_{49},$
  $\mathrm{x}_{52},$
  $\mathrm{x}_{54},$
  $\mathrm{x}_{63},$
  $\mathrm{x}_{66},$
  $\mathrm{x}_{67} \rbrace.$

So this translates the $70$-dimensional input space to an
$8$-dimensional output space.



`FeatureSelector`
-----------------

Applying the `BinaryFrontend` to the 30 binary features, we get
8 categorical features, plus the categorical feature
$\mathrm{C}$, which makes 9 categorical features.
Applying the `HomebrewContinuousFrontend` to the 70 continuous-valued
features, gives us 8 continuous-valued features, for a total
of 17 features.  Now, we'll try to further reduce that.

Both in the `BinaryFrontend` and in the `HomebrewContinuousFrontend`,
the basic idea was to perform a translation on the input space based
on the correlation structure that exists among the features, with the
goal of achieving decorrelation by grouping features together, which
leads to dimensionality reduction as a side-effect.
So the idea here is similar to many common feature engineering techniques,
such as Principal Component Analysis (PCA), which tries to explain as much
of the covariance in the data with as few dimensions as possible.

But applying PCA as a dimensionality reduction technique as a preprocessing
step for classification has the drawback that PCA does not at all take into
account the class labels you are trying to distinguish.  So there is nothing
to guarantee that PCA will not discard exactly those dimensions that are
useful to the classification problem at hand.

This is why in our approach, so far, no information has been directly
discarded.  The worst that can happen is that a dimension that seems
completely uncorrelated to everything else ends up in a cluster on its
own, thus, effectively being passed through unaltered from the input
space to the output space.

Within the feature selection stage of the feature engineering frontend,
the goal is to now finally get rid of those dimensions which do not carry
any information that is useful to the classification problem we are
trying to solve.

In order to do that, we first convert the 8 continuous-valued features
into categorical features, by assigning each value to one of 32 buckets
of equal probabilistic weight.  So, along each dimension, the first bucket
would contain values between the minimum and roughly the 3rd percentile,
the second bucket would contain values exceeding the 3rd percentile up
to about the 6th percentile, etc.  The component which does that is called
the `FeatureDiscretizer`.

So instead of looking at 9 categorical features, plus 8 continuous-values
features, the feature space, in the `FeatureSelector`'s view of the world
is composed of 17 categorical features.  -- N.b. that the discretization
is only used for the feature selection.  The continuous features retain their
original values for later use for classification.

The `FeatureSelector` then picks which features to keep and which to
eliminate based on the following criteria as quantified in information
theoretic terms:

- The five dimensions with the highest absolute information content are
  selected as "core" features.
- The three dimensions most highly correlated with the dependent variable
  `y` are added to those "core" features.
- All features with correlation higher than 50% relative to one of the
  core features are also selected (they are called the "satellite" features
  in the code).

Information content and correlation, in this example, is, once again,
measured in information theoretic terms.

Based on this procedure, the following dimensions are selected:

- $\lbrace
     \mathrm{C},
     \mathrm{B}_2,
     \mathrm{B}_4,
     \mathrm{B}_8,
     \mathrm{X}_3,
     \mathrm{X}_5,
     \mathrm{X}_8 \rbrace$

So, with the help of our feature engineering frontend, we can boil
down 1 categorical feature, 30 binary features, and 70 continuous-valued
features from the input space into 4 categorical features and
3 continuous-valued features in the output space.

The selection of the features above seems to
mesh well with some of the intuitions one might form
based on looking at the results from the previous two sections:
Among the binary features, it is exactly the two larger clusters that
end up getting selected here, which is the case more or less by definition,
since the larger number of binary features in each cluster leads to a larger
number of possible values for the resulting categorical feature, which, in
turn, leads to more information, as measured by entropy.  The only way this
wouldn't be the case is if it turned out that only a small number of the
combinations of values that are combinatorically possible actually appear
in the data, or that they appear in the data with a highly skewed
probability distribution.

Among the continuous-valued features, it is somewhat surprising that one
of the larger clusters, namely $\mathrm{X}_8$ does not make the list.
This, however, might well be genuinely the right thing to do.
Returning to our example about stock returns, it might jus tbe the case that
there are a lot of tech stocks in the data, but the dependent variable
simply isn't affected by the sector return of the tech sector.


How To Put It All Together
--------------------------

To bring the section on the feature engineering frontend to a conclusion,
I will summarize once more the components that are involved, and how they
all plug into each other.

* `CategoricalFrontend` is a structural placeholder (i.e. dummy class) that
  passes through the value of $\mathrm{C}$ unchanged.
* `BinaryFrontend` uses the correlation structure among binary features to
  create categorical variables grouping together clusters of binary features
  that are strongly correlated with each other, but uncorrelated to features
  in other clusters.
* `HomebrewContinuousFrontend` applies the same idea to continuous variables.
  It uses the correlation structure among continuous features to create a
  smaller number of continuous features which are averages across clusters
  of continuous features that are strongly correlated with each other, but
  uncorrelated to features in other clusters.
* `KPCAContinuousFrontend` is a (more or less) drop-in replacement for
  `HomebrewContinuousFrontend` that instead uses [scikit-learn]'s
  [Kernel PCA] method to digest the continuous features into a set of
  three continuous features.

Within the feature selection stage:

* `FeatureDiscretizer` turns the continuous-valued features which are the
  output of `HomebrewContinuousFrontend` into categorical variables by
  bucketizing them into 32 buckets of equal probabilitistic mass.
* `FeatureSelector` uses categorical features, including discretized
  continuous features, to look at the correlation structure and eliminate
  features that seem unrelated to the dependent variable $\mathrm{y}$.

The following schematic shows how those might interact with each other,
in an example-setting in which there are only 10, instead of 100, features.

<div style="width:25em">
![Fig1](Fig1.svg)
</div>


The Classifier
==============

The point of departure for the construction of the actual classifier is that
we are looking at 4 categorical features and 3 continuous-valued features, and
based on the exploration stage of this project, we know a few things about
the properties of the resulting feature space: First of all, the relative
proportion of positives vs negatives shows a great deal of variation, as one
selects different cells, as defined by combinations of categorical features
and discretized continuous features.  But it seems universally the case that
the negative class overwhelms the positive class in every region of the
feature space.  All there is to capture here is these localized
variations in the proportion of positives.  One should not hope for proper
separation of statisticall cells where there are more positives than
negatives.

So, this lead me to conclude that methods based on discriminant functions,
linear or otherwise, are not well suited for this classification problem.

Instead, I chose to use a variation of k nearest neighbor, thus essentially
using proximity to known positive datapoints as a guide in assessing the
likelihood that a new and previously unseen datapoint will be a positive.

The standard use of k nearest neighbor would look at an unseen datapoint,
find the k nearest neighbors, and use a majority vote to decide the class
of the new datapoint: In our case, since pretty much every region of the
space is more densely populated by negative datapoints than positive
datapoints, this would necessarily lead to an overwhelming proportion of
datapoints being classed as negative.  It makes sense to do that, when
evaluating on the basis of accuracy, using a completely symmetric cost
for errors pertaining to positives being incorrectly classified as negatives
vs negatives being incorrectly classified as positives.  In our case, this
would lead to good precision at the cost of bad recall.  But based on
the exploration stage of this project, I have come to expect that
optimal f-measure will rather come about by sacrificing some precision
in favor of recall.

So, the standard use of the k nearest neighbor method needs some tweaking.
In particular, one could relax the majority voting threshold.  Given that
there are so few positives in the data, even seeing maybe one or two
positives among the seven nearest neighbors might be enough to justify
classifying the point as a positive.  -- But there needs to be a
theoretically well-motivated and principled way of doing that, otherwise
the nearest neighbor idea just becomes meaningless.

The second central difficutly one faces here, is how to properly integrate
evidence from the categorical variables with evidence from the continuous
variables, since most machine learning methods are primarily designed to
work in continuous spaces (k-nearest-neighbor being one of them), perhaps
allowing for binary features as a kind of an afterthought (having dimensions
with values of zero or one, for instance), or they are primarily designed
to work on categorical features, such as decision trees, allowing for
continuous valued features in some more or less clumsy way, for example
allowing the decision tree to do threshold comparison queries.

What is needed is an overarching theoretical framework that can be applied
to continuous-valued features as well as categorical features, and the
framework of Bayesian statistical inference provides just that.

Without further ado, let me present the construction, I have come up with,
which is implemented in class `BKNNModel`.

Given some values $\langle \mathrm{C}, \mathrm{B}_2, \mathrm{B}_4, \mathrm{B}_8 \rangle$
for the discrete valued-features
$\langle \mathbf{C}, \mathbf{B}_2, \mathbf{B}_4, \mathbf{B}_8 \rangle$,
the Bayesian decision rule would imply that the predicted class
label $\hat{\mathrm{y}}$ should be
$$\hat{\mathrm{y}}
  =
  \textrm{argmax}_{y}
  \big\lbrace
  \mathbb{P}( \mathbf{y} = y )
  \cdot
  \mathbb{P}( \mathbf{C} = \mathrm{C} | \mathbf{y} = y  )
  \cdot
  \mathbb{P}( \mathbf{B}_2 = \mathrm{B}_2 | \mathbf{y} = y  )
  \cdot
  \mathbb{P}( \mathbf{B}_4 = \mathrm{B}_4 | \mathbf{y} = y )
  \cdot
  \mathbb{P}( \mathbf{B}_8 = \mathrm{B}_8 | \mathbf{y} = y )
  \rbrace.$$

This decision rule is based on an assumption of pairwise stochastic
independence among the features whose likelihoods are being multiplied
here: Through our feature engineering we have already done our best
to ensure that this assumption is as valid as we can make it.

There is only one missing ingredient, which is the evidence from the
continuous-valued features.  This is done through a an approach similar
to $k$-nearest neighbors.  The way this works for $k$ = 7, is as follows.

As part of the training phase of the modelling, the training data
is simply stored as part of the model, together with the
classlabels.

Now, when called upon to make a classification for a previously unseen
datapoint with values
$\vec{\mathrm{x}} = \langle \mathrm{X}_3, \mathrm{X}_5, \mathrm{X}_8 \rangle$
for the discrete valued-features
$\langle \mathbf{X}_3, \mathbf{X}_5, \mathbf{X}_8 \rangle$,
we simply look through the datapoints stored as part of the training
procedure, and identify the 7 nearest positive datapoints
$\lbrace x^{(+)}_1, x^{(+)}_2, \ldots, x^{(+)}_7 \rbrace$.  Assume this set is
sorted by distance, so that $x^{(+)}_7$ is the one which is furthest from
$\mathrm{x}$.  Let $\mathrm{D} = \mathrm{d}( \mathrm{x}, x^{(+)}_7 )$ be the
distance between $\mathrm{x}$ and $x^{(+)}_7$.

Next, we enumerate the set
$\lbrace x^{(-)}_1, x^{(-)}_2, \ldots, x^{(-)}_Q \rbrace$
of negative datapoints for which
$\mathrm{d}( \mathrm{x}, x^{(-)}_j ) \leq \mathrm{D}$,
i.e. we look for the negative datapoints which are no further away from
$x$ than the seventh-closest positive datapoint.

The number $Q$ of such datapoints is the statistic we're interested in.

The idea behind this procedure is as follows: We want to ensure that
the statistics going into the classifier are always derived from statistical
cells large enough to generalize and reduce the impact of noise, even though
there are regions in this space that are more densely and regions that are
less densely populated.  So it makes sense to allow the threshold distance
to vary in this way.

We can turn this statistic $Q$ into a pair of probabilities for our Bayesian
classifier.  All we need is the total number $\mathrm{N}_{(+)}$ of positive
datapoints in the training sample, and the total of number $\mathrm{N}_{(-)}$
of negative datapoints in the training sample:
First note that
$$\mathbb{P}\big(
     \mathrm{d}( \mathrm{x}, \mathbf{X} ) \leq \mathrm{D} | \mathbf{y} = 1
  \big)
     = \frac{\mathrm{7}}{\mathrm{N}_{(+)}},$$
by definition of $\mathrm{D}$.  We can then derive a comparable statistic for
the other class, which is
$$\mathbb{P}\big(
     \mathrm{d}( \mathrm{x}, \mathbf{X} ) \leq \mathrm{D} | \mathbf{y} = 0
  \big)
     = \frac{Q}{\mathrm{N}_{(-)}}.$$

And this is something we can easily integrate into our Bayesian classifier, by
defining the decision rule as follows:
$$\hat{\mathrm{y}}
  =
  \textrm{argmax}_{y}
  \big\lbrace
  \mathbb{P}( \mathbf{y} = y )
  \cdot
  \mathbb{P}( \mathbf{C} = \mathrm{C} | \mathbf{y} = y  )
  \cdot
  \mathbb{P}( \mathbf{B}_2 = \mathrm{B}_2 | \mathbf{y} = y  )
  \cdot
  \mathbb{P}( \mathbf{B}_4 = \mathrm{B}_4 | \mathbf{y} = y )
  \cdot
  \mathbb{P}( \mathbf{B}_8 = \mathrm{B}_8 | \mathbf{y} = y )
  \cdot
  \mathbb{P}\big(
      \mathrm{d}( \mathrm{x}, \mathbf{X} ) \leq \mathrm{D} | \mathbf{y} = y
    \big)
  \rbrace.$$

Since there are only two classes, i.e. two values for $y$, those values
being 0 and 1, we can apply some transformations that are quite commonplace
when dealing with Bayesian decision rules for binary decisions.
First, we apply an abbreviated notation,
writing $\mathbb{P}_1( \mathrm{B} )$
as an abbreviateion for $\mathbb{P}( \mathbf{B} = \mathrm{B} | \mathbf{y} = 1 )$,
and $\mathbb{P}_0(\cdot)$
as an abbreviation for $\mathbb{P}( \cdot | \mathbf{y} = 0 )$ and
writing $\mathrm{P}_1$ instead of $\mathbb{P}( \mathbf{y} = 1 )$ and
$\mathrm{P}_0$ instead of $\mathrm{P}_0$

Then, we restate the above rule by noticing that we decide
$\hat{\mathrm{y}} = 1$ iff
$$
  \frac{
    \mathrm{P}_1
  }{
    \mathrm{P}_0
  }
  \cdot
  \frac{
    \mathbb{P}_1( \mathrm{C} )
  }{
    \mathbb{P}_0( \mathrm{C} )
  }
  \cdot
  \frac{
    \mathbb{P}_1( \mathrm{B}_2 )
  }{
    \mathbb{P}_0( \mathrm{B}_2 )
  }
  \cdot
  \frac{
    \mathbb{P}_1( \mathrm{B}_4 )
  }{
    \mathbb{P}_0( \mathrm{B}_4 )  
  }
  \cdot
  \frac{  
    \mathbb{P}_1( \mathrm{B}_8 )
  }{
    \mathbb{P}_0( \mathrm{B}_8 )
  }
  \cdot
  \frac{  
    \mathbb{P}_1\big(
        \mathrm{d}( \mathrm{x} ) \leq \mathrm{D}
      \big)
  }
  {
    \mathbb{P}_0\big(
        \mathrm{d}( \mathrm{x} ) \leq \mathrm{D}
      \big)  
  }
  >
  1,
$$
and then, equivalently, by taking logs,
$$
  \log\Big(\frac{
    \mathrm{P}_1
  }{
    \mathrm{P}_0
  }
  \Big) +
  \log\Big(\frac{
    \mathbb{P}_1( \mathrm{C} )
  }{
    \mathbb{P}_0( \mathrm{C} )
  }
  \Big) +  
  \log\Big(\frac{
    \mathbb{P}_1( \mathrm{B}_2 )
  }{
    \mathbb{P}_0( \mathrm{B}_2 )
  }
  \Big) +
  \log\Big(\frac{
    \mathbb{P}_1( \mathrm{B}_4 )
  }{
    \mathbb{P}_0( \mathrm{B}_4 )  
  }
  \Big) +
  \log\Big(\frac{  
    \mathbb{P}_1( \mathrm{B}_8 )
  }{
    \mathbb{P}_0( \mathrm{B}_8 )
  }
  \Big) +
  \log\Big(\frac{  
    \mathbb{P}_1\big(
        \mathrm{d}( \mathrm{x} ) \leq \mathrm{D}
      \big)
  }
  {
    \mathbb{P}_0\big(
        \mathrm{d}( \mathrm{x} ) \leq \mathrm{D}
      \big)  
  }
  \Big)
  >
  0.
$$

Next, we generalize this to the family of decision rules which,
for some threshold $\theta$, decide $\hat{\mathrm{y}} = 1$ iff
$$
  \log\Big(\frac{
    \mathbb{P}_1( \mathrm{C} )
  }{
    \mathbb{P}_0( \mathrm{C} )
  }
  \Big) +
  \log\Big(\frac{
    \mathbb{P}_1( \mathrm{B}_2 )
  }{
    \mathbb{P}_0( \mathrm{B}_2 )
  }
  \Big) +
  \log\Big(\frac{
    \mathbb{P}_1( \mathrm{B}_4 )
  }{
    \mathbb{P}_0( \mathrm{B}_4 )  
  }
  \Big) +
  \log\Big(\frac{  
    \mathbb{P}_1( \mathrm{B}_8 )
  }{
    \mathbb{P}_0( \mathrm{B}_8 )
  }
  \Big) +
  \log\Big(\frac{  
    \mathbb{P}_1\big(
        \mathrm{d}( \mathrm{x} ) \leq \mathrm{D}
      \big)
  }
  {
    \mathbb{P}_0\big(
        \mathrm{d}( \mathrm{x} ) \leq \mathrm{D}
      \big)  
  }
  \Big)
  >
  \theta.
$$

In the above derivation of this Bayesian decision rule, I have not taken into
account the effect of asymmetric error costs of false negatives vs false
positives, but it is in fact easy to show that they factor into the decision
rule in the same way as the ratio of priors.  In the above formulation,
all of these aspects would be incorporated into the decision threshold
$\theta$.  Rather than deriving this threshold analytically, however, my
implementation of this classifier treats this as an optimization problem,
setting $\theta$ in such a way as to maximize the F-score obtained on the
training sample.


Results, Conclusions, Future Work
=================================

I tried two variations of this classifier: One using the
`HomebrewContinuousFrontend` as described above, the other using
Kernel PCA as implemented in [scikit-learn] with cosine kernel, to
preprocess the continuous features down into three dimensions.

The evaluation methodology was to use standard metrics and the usual
separation of training data vs development data: So I separated the
training data provided into an 85% portion used to train a model,
and I then applied the model to the remaining 15% of the data to deal
with the effects of data snooping bias.

The results obtained were as follows:

With homebrew (on development data):

~~~~~~~
fscore = 0.1886
precision = 0.1254
recall = 0.3805
true_positives = 3250
false_positives = 22668
true_negatives = 119049
false_negatives = 5291  
~~~~~~~

With Kernel PCA (on development data):

~~~~~~~
fscore = 0.2422
precision = 0.1674
recall = 0.4375
true_positives = 3737
false_positives = 18582
true_negatives = 123135
false_negatives = 4804  
~~~~~~~

So, Kernel PCA seems to perform better on both precision and recall,
and hence on f-measure.

Looking at a result like that, it is always worthwhile to also check the
result obtained when applying the model back to the data it was trained
on to check for overfitting

With Kernel PCA (on training data):

~~~~~~~
fscore = 0.2411
precision = 0.1668
recall = 0.4342
true_positives = 20974
false_positives = 104739
true_negatives = 696622
false_negatives = 27332
~~~~~~~

If the result as obtained on training data had been much better, then
overfitting would have been a possible problem to look into.  This problem
is especially common for very high-dimensional techniques such as
nearest neighbor methods.  In this context it is worthwhile to also
note that, for my implementation of nearest neighbor, I put in place some
logic to prevent any points from being counted into either the 7 nearest
positive neighbors or the corresponding number of negatives if that point
is in fact identical to the point being queried.  Otherwise there would
be a systematic bias, especially among the positives, when applying the
model back to its own training data.

But with these numbers, it seems that overfitting is not an issue, since the
model as tested on development data scores slightly better on both precision
and recall, where one would normally expect the model to perform at least
slighly worse on development data.  This could be purely a coincidence, or
there might be an issue in that the procedure described above to avoid
overfitting actually overcompensates for the issue to a small extent, by
not counting points appearing in a small region around each training data
point, even though another point could have existed in that region as a
matter of pure coincidence.  These small regions result from the fact that
the points in that region would all be represented in the CSV file in the
same way, given that it uses only a handful of digits.  -- In any case the
positive difference in scores seen here seems small enough in magnitude so
that it would have been insignificant in comparison to the negative
difference that would have resulted if overfitting had been a serious
issue here.

A few comments are in order about why Kernel PCA performed so much better
than the homebrew method:  From preliminary experiments during the
exploration stage of this project, it turned out that the use of regular
PCA (as opposed to Kernel PCA), as well as Kernel PCA with different
choices of kernels performed comparably or slightly worse than the
homebrew method.  So there must be something to the cosine kernel
representation in particular that helps in making the data more separable.

The defining characteristic of the cosine kernel is the fact that it
compares data points in terms of their angles, rather than length.
This stems originally from the field of information retrieval, where
documents are considered similar if keywords appear in those documents
in the same proportions, disregarding the length of the document.
So if we have one document where the keyword "risk" is mentioned 100
times, and the keyword "reputational" is mentioned 20 times, it is very
similar to a document where the keyword "risk" is mentioned 10 times
and the keyword "reputational" is mentioned twice, since the proportions
are the same, and the difference in the absolute numbers is likely the
result of differing overall document lengths, whereas a document
that mentions "risk" 100 times and "reputational" only twice would be
considered more dissimilar.  (The first two documents are likely about
"reputational risk", the last of the documents is likely about "risk",
and the two mentions of "reputational" might be coincidental).

Given these results, one might also want to revisit the construction of the
homebrew feature engineering method:  For example, the fact that the feature
engineering eliminates one of the two very large clusters of mutually
correlated features would need to be re-checked, by overriding that behaviour
and checking the effect on the final f-measure.  One might also want to try
out deactivating the sign-flipping behaviour, etc.  But then, finally, there
is the possibility that the idea of creating sums across clusters of mutually
correlated features simply isn't helpful given the nature of the phenomenon
underlying the data.

For the purposes of the present project, we simply pick Kernel PCA as the
better of the two alternatives, and use that as the basis for the submitted
model decisions.


Concluding Remarks
==================

So, this concludes my report on the approach I took to the algorithm
challenge.  As I've pointed out before, I've tried to keep this document
as brief as possible, by merely describing the components that ended up
being the solution I ultimately submitted.  Essentially this is the kind
of thing someone would want to read, if they were interested only in finding
out what it is that my code actually does, without wanting to form an
opinion on whether that approach is actually the best (or even a good)
approach to the problem at hand.  This also explains, why this document
does not have any plots or tabulations relating to the effect of different
paramter settings, etc. etc.  -- If you are interested in that part,
check out the document `EXPLORATION`.


[richard.bergmair.eu]: http://richard.bergmair.eu/
[some slideshow]: http://www.people.fas.harvard.edu/~junliu/Workshops/workshop2007/talkSlides/ChristianRobert_knn.pdf
[Gsellmann's Weltmaschine]: https://www.youtube.com/watch?v=9RKlJ2oBROA&NR=1
[this comment here]: https://github.com/Segment-of-One/recruitment_challenge/issues/3
[scikit-learn]: http://scikit-learn.org/
[Kernel PCA]: http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.KernelPCA.html
[entropy]: https://en.wikipedia.org/wiki/Entropy_(information_theory)
[mutual information]: https://en.wikipedia.org/wiki/Mutual_information
[correlation]: https://en.wikipedia.org/wiki/Total_correlation

