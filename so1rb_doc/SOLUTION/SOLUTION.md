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
end up hallucinating complexity where non exists, then that's just as weak.
(See [Gsellmann's Weltmaschine]).  Okay, so that's that.

Solution vs. Exploration
------------------------

In this document, I will outline the solution to the SO1 algorithm challenge
that I came up with.  The purpose of the present document (`SOLUTION`) is to
tell you where that solution is located, and give you directions on how to get
there most efficiently, starting from first principles.  -- There is a separte
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
* $\mathrm{cid}$ (which is also called $\mathtt{cid}$ in the data) is
  a number in the range $[1,30]$.
  In combination with [this comment here], according to which this feature
  "somewhat structures the data", I'm assuming that the abbreviation is for
  "category id", and that the feature is not to be interpreted as a number,
  neither ordinal nor cardinal, but rather as a discrete symbol.
* Among the columns called $\mathtt{x}_1 \ldots \mathtt{x}_{100}$ in the data,
  there are 70 continuous-valued numeric columns, and 30 columns with
  values `0` or `1`.
  In what follows, I'll reindex these, so that
  $\mathrm{x}_i$ is the $i$-th of the continuous-valued features, and
  $\mathrm{b}_j$ is the $j$-th of the binary features.

The module `so1rb/so1rb_data/da_read.py` implements a reader that reads this
data format.

Throughout the rest of this section, I will describe the modules
under `so1rb_frontend`.  These are classes derived from `Frontend`,
and they all serve the purpose of preprocessing the data so as to
present it to the core classification algorithm in a suitable representation.

There are two stages to this:

* Decorrelation (= orthogonalization): So as to transform the data into
  a space in which features are as close as possible to pairwise mutually
  independent.
* Feature selection: So as to identify and remove any components in the
  decorrelated (orthogonalized) space, that are unrelated to the dependent
  variable $\mathrm{y}$.

Within the Decorrelation stage:

* `CategoricalFrontend` is a structural placeholder (i.e. dummy class) that
  passes through the value of $\mathrm{cid}$ unchanged.
* `BinaryFrontend` uses the correlation structure among binary features to
  create categorical variables grouping together clusters of binary features
  that are strongly correlated with each other, but uncorrelated to features
  in other clusters.
* `HomebrewContinuousFrontend` applies the same idea to continuous variables.
  It uses the correlation structure among continuous features to create a
  smaller number of continuos features representing averages across clusters
  of continuous features that are strongly correlated with each other, but uncorrelated to features in other clusters.
* `KPCAContinuousFrontend` is a (more or less) drop-in replacement for
  `HomebrewContinuousFrontend` that instead uses [scikit-learn]'s
  [Kernel PCA] method to digest the continuous features into a set of
  three continuous features.

Within the Feature Selection stage:

* `FeatureDiscretizer` turns the continuous-values features which are the
  output of `HomebrewContinuousFrontend` into categorical variables by
  bucketizing them into 32 buckets of equal probabilitistic mass, i.e.
  first to third percentile, fourth to sixth percentile, etc.
  This is not used for classification, but only as a preprocessing step
  for the `FeatureSelector` (described below), and to speed up lookups
  for k-nearest-neighbor, but indexing on descretized values.
* `FeatureSelector` uses categorical features, including discretized
  continuous features, to look at the correlation structure and eliminate
  features that seem unrelated to the dependent variable $\mathrm{y}$.

The following schematic shows how those might interact with each other,
in an example-setting in which there are only 10, instead of 100, features.

<div style="width:25em">
![Fig1](Fig1.svg)
</div>

In what follows, I'll cover each of the frontend components in turn,
describing how they work, and what benefit they achieve in terms of
orthogonalization and dimensionality reduction.

`BinaryFrontend`
----------------
asdf




















[richard.bergmair.eu]: http://richard.bergmair.eu/
[some slideshow]: http://www.people.fas.harvard.edu/~junliu/Workshops/workshop2007/talkSlides/ChristianRobert_knn.pdf
[Gsellmann's Weltmaschine]: https://www.youtube.com/watch?v=9RKlJ2oBROA&NR=1
[this comment here]: https://github.com/Segment-of-One/recruitment_challenge/issues/3
[scikit-learn]: http://scikit-learn.org/
[Kernel PCA]: http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.KernelPCA.html

