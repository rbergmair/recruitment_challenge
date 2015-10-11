% How RB Figured Out His Approach to SO1's Algorithm Challenge
% Dr Richard Bergmair
% Oct-10 2015

# 0: About This Document

- There is another document (`SOLUTION`) which describes my solution to
  the SO1 algorithm challenge.  The present document (`EXPLORATION`)
  describes the thought process that got me to that solution.  This is
  the part that usually people aren't interested in.  So if you're not,
  stop reading this, and refer to the other document.
- The code that goes with this thought process is under `so1rb_explore`.
- I've decided to do this in the form of a slide show, so I can walk you
  through it, one idea at a time, using a flat structure, and associating
  images with individual ideas.
- If I were actually called upon to do a presentation, this is not how
  I would normally structure a slide show.  -- Way too much text etc.

# 1: I Separated Out Some Development Data

- I took the training data that I was provided, and split it into
  an 85% portion for actual training data, and a 15% portion for
  development data.  -- Henceforth, when I say training data, or
  make no explicit statement at all as to which portion of the data
  I'm talking about, this 85% portion is what I will be referring to.
- Throughout the rest of the exploration stage of the process as
  described in this document, I only look at training data.
  This allows me to use the development data later on to get a sense of
  where my evaluation measure is likely to end up when I submit the
  results for use on the actual test data,
  while keeping [data snooping bias] to a minimum.
  (Also see [my video lecture on methodology]).
- It seems that, with this example project, we're in the situation of
  having plenty of data, although that is obviously a very relative
  term.  -- relative to the phenomena in the data that you're trying to
  capture and the data complexity they imply.
- In a project where data is rather on the scarce side, I wouldn't give up
  on 15% of the data so easily.  I would then just use the entire training
  data for exploration, as long as I only use it to look at stuff, rather
  than to select a model from a large model space.  In order to get an
  estimate of the ultimate performance, I would then use cross-validation.
- As part of my very initial step of processing the data, I find it useful
  to reshuffle the data using a random-number generator.
- Running exploration scrips on the entirety of the data can often take
  a long time, which is a drag on my productivity, especially in the
  exploration stage.  So I often end up putting a `break` statement into
  the loop reading the data, so as to stop reading after a large enough
  dataset has been read in.
- This, obviously, is bound to go horribly wrong if the dataset
  came out of a database dump, for example, where the ordering of the data
  could be an artefact of the indexing structure or the insertion order,
  and you end up looking not at a random sample, but rather at only old
  data, or only data where certain columns have certain values, etc.
- So it's better to just reshuffle, and be on the safe side.

# 2: What's This `cid` thing?

- Since this `cid` column is the only one that, at very first sight,
  stands out, I started by counting the number of positive datapoints,
  and the total number of datapoints associated with each value for
  `cid`.
- By a positive datapoint, I mean a line in the CSV file with
  $\mathtt{y} = 1$.
- It turns out that `cid` can take on 50 different values, from 1 to 50.
- They are very unevenly populated, with
  $\mathtt{cid} = 16$ appearing 87 times and
  $\mathtt{cid} = 3$ appearing 26477 times.
- They imply different distributions for positive vs negative datapoints.
  For example $\mathtt{cid} = 50$ has 11.65% positives, while
  $\mathtt{cid} = 16$ only has 2.5% positives, so it seems quite relevant
  to the dependent variable.
- Neither the total number of data points, nor the proportion of positives
  seems to be an obvious function `cid`, neither its ordinal nor its
  cardinal value, so I'll treat it as a discrete symbol, rather than as a
  numeric value.
- It's important to make a conscious decision on that one: For example, if
  you're working on a database dump, and the data contains information
  about cars, then there could be a column `car_type`, where value 101
  means motorcycle, value 42 means sedan, value 3 means mini truck,
  and value 7 means a tractor unit for a road train.  Another column
  could be `horsepower`, which would also be a number.  Now, you could
  easily use `horsepower` as an ordinal or cardinal number, perhaps as
  a feature in a linear discriminant, but it would be complete nonsense
  to do this, with `car_type`, despite the fact that both of them,
  prima facie, look like numbers.  This is a common rookie mistake.
- Another thing that's noteworthy here, is that the proportion of positives
  never crosses the 50% boundary.  If there were values for
  $\mathtt{cid}$ above and below 50%, then that would in and of itself
  imply a classifier that can improve over baseline in terms of
  accuracy, by looking at $\mathtt{cid}$ and nothing else.  But
  unfortunately, that's not the case here.


# 3: Looking Into Those $\mathtt{x}$'s By Way Of Plot.

![](step03.png)

- I picked two of those categories at random, in this case categories
  8 and 42.

- I picked four of the $\mathtt{x}$'s at randdom, in this case
  $\mathtt{x}_1$, $\mathtt{x}_2$, $\mathtt{x}_{99}$, and $\mathtt{x}_{100}$

- The rows, from top to bottom are $\mathtt{x}_1$ vs $\mathtt{x}_2$,
  $\mathtt{x}_1$ vs $\mathtt{x}_{99}$, $\mathtt{x}_1$ vs $\mathtt{x}_{100}$,
  $\mathtt{x}_2$ vs $\mathtt{x}_{100}$,
  and $\mathtt{x}_{99}$ vs $\mathtt{x}_{100}$,

- The left-hand column shows datapoints with
  $\mathtt{cid} = 8$, the right-hand column shows datapoints with 
  $\mathtt{cid} = 42$.

- This plot visualizes a number of phenomena:
    + distributions of points along some individual dimensions
    + correlations between some pairs of dimensions
    + check on whether these behave the same or differently for two
      different values for $\mathtt{cid}$.

- At this stage, I'm trying to start forming some opinons on where
  in my model I can or cannot make various kinds of independence
  assumptions.  There are three kinds of independence:
    + logical independence (logic and possibility theory)
    + stochastic independence (probability theory)
    + linear independence (absence of correlation in statistics)

- At this stage, I'm primarily interested in logical dependencies,
  as well as the logical structure behind stochastic and linear
  dependencies, because these are the kinds of things that dictate
  design choices that need to be made at an early stage.

- For example: the horsepower of a heavy truck as applied to a motorcycle
  is a logical impossibility.  I've
  had cases like that in data science projects in the past, and have
  approached them by splitting out variables, one variable representing the
  horsepower of a truck, with value null if the thing isn't a truck, the
  other variable representing the horsepower of a motorcycle, with value null
  if it's not a motorcycle.  -- This yields a model that makes
  apples-to-apples comparisons.  Otherwise the horsepower column would become
  to a large extent a proxy for the distinction between motorcycle and truck,
  which, however, needs to be treated as a separate piece of information.
  -- If there's a need to do this kind of feature engineering, it's important  
  to know about it early on.

- At some point, this classifier will need to be able to combine evidence
  from the discrete variable with evindence from the continuous variables.
  There are two ways of going about this:
    + One could treat them as logically dependent, meaning that you would
      train one model that captures the continuous variables and that applies
      only to datapoints with, say $\mathtt{cid} = 8$, and a completely
      separate model that applies only to datapoints with, say
      $\mathtt{cid} = 42$.
    + One could treat them as logically independent, so that you train some
      model on all data, ignoring the $\mathtt{cid}$ value, and then integrate
      the evidence from $\mathtt{cid}$ by merely shifting a decision threshold
      or a bias term, or something like that.
  Consider two examples:
    + You have a database of wine sales, with a categorical variable
      `audience`, which can take on values of `preppie` and `wino`.
      You might find a positive correlation between price and sales among
      preppies, but a negative correlation among winos.  In such a case you
      would treat price and sales as logically dependent on audience.
    + You have a database of horses, with a categorical variable `color`
      and some variables `height` and `weight`.  You might find that `color`
      does not affect the relationship between the other variables
      substantially, in the sense that, by just ignoring `color` and looking
      at all data all at once, you're still looking at a sample that is
      homogeneously behaved when it comes to describing the relationship
      between `height` and weight.
      So you would treat those as logically independent.
  Again, this distinction is a distinction you would want to know about
  early on in the process.  If there's a logical dependency you want to
  make sure, you're looking at statistically homogeneous subsets of the data
  as you go around exploring it.

- Based on this plot, I can't see any examples of $\mathtt{cid}$
  inducing logical dependencies, so I will proceed under the assumption
  that there aren't any, but I make a mental note to keep verifying this,
  since I'm only looking at a few examples here, and it's very possible
  that there are logical dependencies that I've simply missed.

- The plots show that some pairs of continuous dimensions are
  correlated as is the case with $\mathtt{x}_1$ vs $\mathtt{x}_2$,
  whereas others aren't.  I make a mental note of that.

- The second and fifth row clearly exhibit a noteworthy phenomenon:
  These are actually binary features!

- If I had been really lucky here, some of those plots would have already
  displayed the positives and negatives in different regions of the space,
  implying the possibility of separation.  Unfortunately, in all the
  examples displayed here, the positives seem firmly embedded inside the
  negatives, and there is no obvious way here to separate them.

# 4: Discretization Test

- So, let's sort out these binary features then.
- There's a bigger phenomenon possibly at play here, which is discretization.
- Thinking of our road vehicle database again: There could be a feature such
  as `number_of_doors`, which permits only a fairly small range of
  integer possibilities.  This would probably induce a qualitiative rather
  than a quantitative distinction, so one would have to think about whether
  to treat each discretized variable as a discrete symbol or as a numeric
  value, etc.
- So I wrote a script, which, for each of the $\mathtt{x}$'s
  records its unique values, stopping the recording after having seen 500
  different values.  It then outputs the number of unique values seen for
  each dimension, including, for dimensions with fewer than 5 values,
  the actual values themselves.
- It turns out that there is a set of 30 binary features.
- Among the remaining 70, they all have more than 500 distinct values,
  so none of them exhibit any signs of quantizatin or discretization,
  and can therefore be treated as continuous and numeric in nature.

# 5: Logical Dependencies Among Binary Features

- Having made this discovery that there are 30 binary features in the data,
  the next thing to do is to look for logical dependencies among them.
- If they were logically independent, there would be
  $2^{30} \approx 1\mathrm{G}$ different combinations.  Obviously they
  can't all be exhibited in a dataset of only $\approx 850\mathrm{k}$
  datapoints, but you would still expect a whole lot of combinations to
  show up.
- If there were logical dependencies among them, then that number could
  be a lot smaller.
- So, I wrote a script to count the number of unique combinations of values
  for binary features, and it turns out that there are only 367.
- This means that the binary features are strongly constrained by a rich
  set of logical dependencies that exist among them.  So I make a mental
  note of that.
- I also tried this in combination with $\mathtt{cid}$.
  With 367 values for the binary features, and 50 values for $\mathtt{cid}$,
  you'd expect $50 * 367 = 18350$ combinations, and the script has actually
  seen $18349$ of those, so $\mathtt{cid}$ does not seem to participate
  in the system of pairwise mutual dependencies that exist among the binary
  features, but rather seems logically independent.
- It's perfectly possible that, among those 367 combinations of values
  for the binary features, there's further internal structure.  For example
  if there were a binary
  feature that was nearly independent of the others, it might well be that
  the 367 combinations break apart into a set of 183 combinations for the
  other features, plus the value zero for the independent one, plus a set
  of 184 combinations for the other features, plus the value one for
  the independent one.  But for now, I don't yet need to know all of that
  in detail.
- As before in step 2, I looked at the total number of datapoints obtained
  for each combination, as well as the ratio of positives, and am finding
  that the numbers vary wildly.  This implies that the binary features do
  have positive information content with regard to the dependent variable
  $\mathrm{y}$.
- But, again, the ratio of positives, even for these fine-grained combinations
  of binary feature values never crosses the 50%-line, except for very very
  small cells.  So there isn't yet an obvious way to construct a classifier
  here.
- The script operates by representing each combination of binary features
  in a single integer, using some bit-arithmetic.  I use hex numbers to
  then display that integer.
- Interestingly, it is the combination of binary features
  equalling `0x3fffffff`, i.e. the combination for which every binary
  feature has value one, which has the largest total number of datapoints
  in it (that number being 72215).
- One can further combine that with the category, to obtain the combination
  with category $14$ (denoted `0xe.0x3fffffff`) as the most frequent one.
- The combination `0x3fffffff` also exhibits a fairly high density of
  positive datapoints, at 10%.  Only one other combination has an even
  higher density of positives. That is `0x3dfe7f5f`, which as 12%.
- It might well be that every one of the binary features, more or less,
  has the effect of accumulating additional evidence in support of a
  positive decision.  I'll make a mental note of that.  The Bayesian method
  should be able to assign weights appropriately.
- In combination with category values, the density of positives can go
  even higher: `0xe.0x3fffffff` has as many as 16% (total number of data
  points 2436).
- Combination `0x18.0x1fd57fcf` has as many as 50% positives, but is only
  thinly populated (10 data points).
- So, I should look at those in more detail.

# 6: Another Plot Seems Called for

![](step06.png)

- So, I re-did the plot from step 3, this time removing the binary features,
  and looking at combination `0xe.0x3fffffff` on the left-hand side, and
  `0x18.0x1fd57fcf` on the right hand side, rather than the arbitrarily
  chosen categories 8 and 42.
- The larger density of positives, in relation to the entirety of the dataset
  is clearly visible here, but other than that, no real patterns seem to
  emerge.
- Regarding combination `0x18.0x1fd57fcf`, it seems likely that the unusually
  large proportion of positives is a selection-bias artefact resulting from
  the fact that it's so thinly populated, so I'll file this under dead end.
- Once again, there isn't an obvious way here, to separate the positives from
  the negatives.

# 7: Construct Some Subsamples

- Having looked into the categorical and binary features a little, it's now
  time to turn attention to the continuous variables.
- I started by slicing the data in various ways to obtain some meaningfully
  constructed samples that would allow some conclusions to be drawn that
  are universally true about the structure of the space induced by the
  continuous variables, even given that I'm not entirely sure if those
  variables are logically dependent on the category and/or the combination
  of binary features.
- So I constructed four subsamples:
   - A sample across everything, capping at 10000 data points
     (`all`).
   - The category `0xe`, across all combinations of binary features,
     capping at 10000 data points (`catplane`).
   - The binary combination `0x3fffffff`, across all categories,
     capping at 10000 data points (`binplane`).
   - The combination `0xe.0x3fffffff`
     (`data`).  There are only 2436 data points
     there in total, so no capping is needed.
- In what follows, I will study the continuous variables in detail.
- In each step, I'll start by looking at `data`.
- If that leads me to any particular conclusion, I will double-check
  that conclusion against the other subsamples.  If the conclusion is
  still justified in the other subsamples, it'll be safe to assume
  that it's universally valid.
- If every conclusion is either universally valid or never valid, but
  never valid in one subsample and not in another, I'll proceed on the
  assumption that the continuous dimensions are logically independent
  from the discrete ones.  

# 8: Try Some 2d-Projections

- As far as the classification problem is concerned, the key will be to
  find some kind of an n-dimensional projection of this 70-dimensional
  space that allows for a good separation.
- To that end, I started with what you might call a brute-force search
  for such a projection.
- With 70 individual dimensions, there are 2415 pairs of dimensions.
- For each pair, I look through each data point.
- I discretize the continuous values into one of 7 range-buckets, each
  of which is constructed so as to hold an equal number of points
  (i.e. septiles).
- So given a pair of dimensions and a data point, the data point can
  fall into one of 49 cells (one of 7 septiles in on dimension, and
  another one of 7 septiles in the other dimension).
- For each pair of dimensions, I record the maximum proportion of
  positive datapoints observed in any one cell.
- While I was at it, I also recorded the shift in median among positive
  versus negative data points, along each dimension.
- For subsample `data`, the largest proportion was observed for the
  combination of dimensions 10 and 63, where there was a cell with 65%
  positive datapoints.
  But that contained only 0.7% of the data points, so it might just
  be a coincidence that the cell happened to be at a thinly populated edge.
- In total, there were only 42 (out of 2415) combinations of features
  that had a cell with more than 50% positive datapoints.
- For subsamples `binplane`, `catplane`, and `all` there were no pairs
  of dimensions yielding any cells with more than 50% positive datapoints
  at all.
- Shifts in medians seemd low across the board, so nothing much
  interesting there either.

# 9: Look At That In A Plot

![](step09.png)

- Just to be thorough, I decided to plot dimension 10 vs 63
  for subsample `data`
  (which was the combination that looked remotely like the most interesting).
- So, nothing there.

# 10: Try Some Sums

![](step10.png)

- Next, I thought I'd look at whether there is more information in the
  sum of the continuous dimensions than there is in the individual dimensions.
- An example of such a scenario would be, when each of the individual
  70 dimensions is the return on a different stock, and the dependent
  variable is dependent on the move of the stock market as a whole, but not
  on the move of any individual stock.
- In this case, each stock would be correlated with the market move, so its
  return would be the market return, plus a noise term.
- By averaging across the values, the noise terms cancels out,
  and the average ends up capturing the market move.
- I distinguished between dimensions, based on the sign of the shift
  in class median between the red vs blue points.
  I summed up the dimensions where that sign was positive to obtain an
  x-value, and the dimensions where that sign was negative to obtain a
  y-value.  In addition, I weighted the values by the magnitude of the
  median-shift, so as to amplify the effect from those dimensions which
  have good separations.
- The result can be seen above.  The four plots are the ones obtained for
  the four subsamples.  In all four cases, it can be seen that no
  separation emerges.  So, that's another dead end.

# 11: Test For Centre Embedding

- In step 8, I already did a brute force search for a pair of two dimensions,
  whose values yield a good separation in some region of the resulting
  two dimensional space.
- But just because, there isn't a set of two such dimensions, it doesn't
  mean that there couldn't be a higher-dimensional projection that creates
  good separation.
- For example: Imagine a donut and a cherry which is in the hole in the
  middle of the donut.  The donut and the cherry are two different classes
  of data points.
- Looking at it in a 2d-projection from the top, it's easy to separate them
  (for example, using polar coordinates).
- Looking at it in any 1d-projection, it becomes impossible to separate them.
- That phenomenon could exist in a higher-dimensional variety.  For example,
  given a cocktail cherry inside a coconut, any 2d-projection is now bound
  to fail, but you can still separate them in the 3d-representation.
- The problem is, we can't really reiterate the study from step 8 in
  higher-dimensional spaces, since it would very quickly become
  computationally very expensive.
- But we're lucky, we might be looking at a situation where there is a
  high-dimensional projection that achieves the separation, subject to the
  additional constraint that the cell of interest is always the one in the
  centre.  -- This is somewhat suggested by the fact that every
  2d-projection I've looked at so far seems to have the positives embedded
  in the centre of the negatives, so that might be universally true.
- So I wrote another script, based on the one from step 8, looking not only
  at pairs, but also at sets of three and four dimensions, which computes the
  proportion of positives among those points which fall in the central
  septile in every one of those dimensions.
- The following observations relate to subsample `data`.
- The best single dimension achieves proportion at most 22%.
- The best pair of dimensions achieves 36%.
- The best set of three dimensions achieves 60%, but that cell only contains
  10 data points.
- The best set of four dimensions achieves 50%.
- The fact that it tails off after three suggests that there's little point
  to continuing to look for central embedding in higher-dimensional spaces.
- Reiterating the experiment with `all_data`, capping at 2500 datapoints,
  the progression is 8%, 17%, 50%, 33%.
- So, that's one more dead end.

# 12: Start Thinking Outside The Box

![](step12.png)

- In my desperation, I started taking some long shots, at this point.
- What if the value of $\mathtt{cid}$ indicates one dimension as being
  "relevant", whereas the others are just noise?
- The histogram of relevant values are in the plot above.
- On the left hand side, the assumption is that the index is across
  all $\mathtt{x}$'s, on the right hand side, just across the continuous
  ones.
- The spike in the middle, on the left hand side is due to the fact
  that zeroes and ones are a lot more frequent, due to the binary
  features playing into this.  
- No separation.  Another day older and deeper in debt.
- But the idea was not as far fetched, as it may have sounded.  This kind
  of data could come about, when the dimensions record, for example,
  signals from different sensors, but they are not meaningful at all
  times.  For example, if they are cameras, and only one of them has
  the lens-cap off at any one time, and $\mathtt{cid}$ records which one,
  then this would be that type of scenario.

# 13: Explore This Further

![](step13.png)

- I hallucinated some patterns there, that I will not even go into.
- In order to make completely sure, I compared the histogram that
  results from picking the dimension picked out by $\mathtt{cid}$
  (left) against a randomly chosen dimension (right).
- I did this without any filtering (top), and filtering out the
  zeroes and ones (bottom).
- So that's what this is.
- Nothing here.




[data snooping bias]: https://en.wikipedia.org/wiki/Data_dredging
[my video lecture on methodology]: http://www.utopia-refraktor.com/en/blog/tech-talks/machine-learning/2015/01/evaluation-methodology