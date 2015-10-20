# RB's Approach to So1's Recruitment Challenge

Just a few comments as a point of departure in working with this repository:

There are four parts to this archive:
1. `predictions.tsv.gz` is the file containing the model predictions for
   my submission.
2. `so1rb_doc` contains the documentation
3. `so1rb` is a reusable python package including a set of scripts for
   fitting a model and running it on data.
4. `so1rb_explore` is a sequence of self-contained python scripts that I
   used to explore the data.

### Documentation

* `so1rb_doc/SOLUTION.html` is a description of what's under `so1rb`,
  with a description of what it is the code does, without, however,
  going into detail on why I believe that solution is the right
  solution to the problem.
* `so1rb_doc/EXPLORATION.html` describes the process of how I explored the
  data which informed the solution I came up with.

### Software Prerequisites

I'm listing the versions I used for development and testing.  It probably
works with other versions, too, but there are no guarantees, obviously.

1. [Python] 3.4.2
2. [kyotocabinet] 1.2.76
   plus [kyotocabinet-python] 1.22
3. [leveldb] 0.193
   plus [plyvel] 0.9
4. [numpy] 1.9.0
5. [scikit-learn] 0.15.2

For `so1rb_explore` you will also need

6. [matplotlib] 1.4.0

### Getting Started Running the Software

There is a script to generate a zip file for each of `so1rb` and
`so1rb_explore`.

    ```
    pack.sh
    ```

You can then conveniently run the zip file from python:

    ```
    python3 so1rb_explore.zip step01_separate_dev_data /dta/so1
    python3 so1rb.zip so1rb01_separate_dev_data /dta/so1
    ```

The first argument is always the path to a directory where the scripts
will read input files and write output files.

For the scripts in `so1rb_explore`, this is the only argument required,
everything else being hardcoded.

# So1 Algorithm Team's Recruitment Challenge

Here at So1, we ("the algo" team) do your typical data-science-y things:
* We write a lot code (to make models, explore data, etc.)
* We pull our hair out when said code doesn't work
* We pull our hair out when said code works, but the models are crap
* We use git to manage our code
* We try to facilitate knowledge transfer through written media (read: we occasional write notes to each other)
 
Justifiably, 1-in-3 of our data scientists are bald, and So1 occasionally sponsors experimental hair replacement surgeries*.

However, aside from your typical data-sciencey things, we are always looking for new talent to join the team. To give you a taste of the kind of work we do here, and the way we do our work, we've made this git repo, and some fake data for you to noodle around with. Completing this challenge requires:
* Command of at least one programming language (we mainly use R, but other languages are okay)
* A basic fluency in git

### Directions:
1. Fork this repo.
2. Download and unzip the [training](http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/train.tsv.gz) and [testing](http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/test.tsv.gz) data, or (if you're a CLI junkie) use
   
    ```
    wget http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/train.tsv.gz
    wget http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/test.tsv.gz
    gunzip train.tsv.gz
    gunzip test.tsv.gz
    ```
3. Load up your favorite text editor (mine is Vim :wink:) and start playing with/modeling the data.
4. When you're done, initialize a _[Pull Request](https://github.com/Segment-of-One/recruitment_challenge/pulls)_, and we'll checkout what you've done and benchmark your predictions.

Per usual github etiquette, if you spot any issues with the data, or need any clarifications, raise an _[issue](https://github.com/Segment-of-One/recruitment_challenge/issues)_.

### What does it mean to complete this challenge?
Being able to write code, make models, and generate predictions is all well and good, but we need people who can also communicate insight. The point of this challenge is three-fold:

1. Find out how good your ML-fu is
2. Find out how you think
3. Find out well you can communicate what you're thinking
 
Consequently, your deliverables are
* A gzip'd .csv (or .tsv) of (binary) predictions containing columns named `id` and `y`
  * At the risk of being pedantic, your `y` should come from data provided in the `id` row of `test.tsv`
  * We will be evaluating their [`F1`-score](https://en.wikipedia.org/wiki/F1_score)
* A report detailing how you arrived at your predictions
  * While other data scientists are your intended audience, assume that they have no interest in seeing code
    snippets, in here
  * Your report should contain complete sentences (and graphics, if you're inclined)
 
The report doesn't need to be [Pulitzer Prize](https://en.wikipedia.org/wiki/Pulitzer_Prize)-worthy, but a few lines about how,

> _...[you] tried an SVM, and logistic regression with a cross-validated thresholding parameter..._

is a one-way ticket to the trash bin. 

#### The ideal report might include:
* A (quantified) comparison of multiple models
* Any insight as to why certain methods performed better than others
* Graphics from any EDA that might have lead to feature-related insights
* An explanation of any feature engineering that occurred
* An analysis of the final model chosen to produce the uploaded predictions
    * Model performance (perhaps as a function of certain model parameters)
    * Decision boundaries or other interesting clustering results/visualizations
 
_In case you're interested_, you can see how well you stack up [against previous participants](https://github.com/Segment-of-One/recruitment_challenge/wiki/Leader-Board).

[Python] https://www.python.org/downloads/
[kyotocabinet] http://fallabs.com/kyotocabinet/pkg/
[kyotocabinet-python] http://fallabs.com/kyotocabinet/pythonpkg/
[leveldb] https://github.com/google/leveldb
[plyvel] https://pypi.python.org/pypi/plyvel
[numpy] https://github.com/numpy/
[scikit-learn] https://pypi.python.org/pypi/scikit-learn/0.15.2
[matplotlib] http://sourceforge.net/projects/matplotlib/

---
\* So1 doesn't actually offer experimental hair surgery as an explicit employee benefit. Maybe the German goverment might, though!
