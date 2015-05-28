# So1 Algorithm Team's Recruitment Challenge

Here at So1, we ("the algo" team) do your typical data-science-y things:
* We write a lot code (to make models, explore data, etc.)
* We pull our hair out when said code doesn't work
* We pull our hair out when said code works, but the models are crap
* We use git to manage our code
* We try to facilitate knowledge transfer through written media (read: we occasional write notes to each other)
 
Justifiably, 1-in-3 of our data scientists are bald, and So1 occasionally sponsors experimental hair replacement surgeries*.

However, aside from your typical data-sciencey things, we are always looking for new talent to join the team. To give you a taste of the kind of work we do here, and the way we do our work, we've made this git repo, and some fake data for you to noodle around with. Completing this challenge requires:
* command of at least one programming language (we mainly use R, but other languages are okay)
* a basic fluency in git

### Directions:
1. Fork this repo.
2. Download and unzip the [training](http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/train.tsv.gz) and [testing](http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/test.tsv.gz) data, or (if you're a CLI junkie) use
   
    ```
    wget http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/train.tsv.gz
    wget http://algo-recruitment-data.s3-website.eu-central-1.amazonaws.com/train.tsv.gz
    gunzip train.tsv.gz
    gunzip test.tsv.gz
    ```
3. Load up your favorite text editor (mine is Vim :wink:) and start playing with/modeling the data.
4. When you're done꙳, initialize a Pull Request, and we'll checkout what you've done and benchmark your predictions.
 
### What does it mean to complete this challenge?
Being able to write code, make models, and generate predictions is all well and good, but we need people who can also communicate insight. The point of this challenge is three-fold:

1. Find out how good your ML-fu is.
2. Find out how you think.
3. Find out well you can communicate what you're thinking.
 
Consequently, your deliverable is a .csv of predictions -- you're to model the "`y`" column of the training data -- and a report detailing how you arrived at your predictions. The report doesn't need to be [Pulitzer Prize](https://en.wikipedia.org/wiki/Pulitzer_Prize)-worthy, but a few lines about how,

> _...[you] tried an SVM, and logistic regression with a cross-validated thresholding parameter..._

is a one-way ticket to the trash bin. 

#### The ideal report might include:
* a (quantified) comparison of multiple models
* any insight as to why certain methods performed better than others
* graphics from any EDA that might have lead to feature-related insights
* an explanation of any feature engineering that occurred
* an analysis of the final model chosen to produce the uploaded predictions
    * model performance (perhaps as a function of certain model parameters)
    * decision boundaries or other interesting clustering results/visualizations
 

---
\* So1 doesn't actually offer experimental hair surgery as an explicit employee benefit. Maybe the German goverment might, though!
