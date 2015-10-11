% How RB Figured Out His Approach to SO1's Algorithm Challenge
% Dr Richard Bergmair
% Oct-10 2015

# 1: Separate Development Data

- I took the training data that I was provided, and split it into
  an 85% portion for actual training data, and a 15% portion for
  development data.  -- Henceforth, when I say training data, this
  85% portion is what I will be referring to.
- Throughout the rest of the exploration stage of the process
  as described in this document, I only look at training data.
  This allows me to use the development data to get a sense of
  where my evaluation measure is likely to end up when I submit
  the results for use on the actual test data, without
  [data snooping bias] creeping into that estimate.
  (Also see [my video lecture on methodology]).
- Drink coffee

# In the evening

- Eat spaghetti
- Drink wine

# Conclusion

- And the answer is...
- $f(x)=\sum_{n=0}^\infty\frac{f^{(n)}(a)}{n!}(x-a)^n$    


[data snooping bias]: https://en.wikipedia.org/wiki/Data_dredging
[my video lecture on methodology]: http://www.utopia-refraktor.com/en/blog/tech-talks/machine-learning/2015/01/evaluation-methodology