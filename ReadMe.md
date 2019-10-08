# StackUnderflow

<img src = "/img/cli_classifier_solution.png" height="350">


## 1. Problem & context

This project is an home assignment given to me by [<img src = "/img/packetai.svg" height="20">](http://www.packetai.co/)

The problem is stated as:

We want to build a tool that scrapes the Stackoverflow website and for every question (generally a question reflects a symptom of a problem) it predicts two things:
- The root cause of the problem
- The solution (answer) of the problem

Given the following constraints:
- Build the basics of a long term project, your code needs to be easily understood and reusable.
- Code does not need to be optimal in terms of performance but needs to be fast enough to provide a good user experience.
- Code needs to be trusted: it does what it is meant to do.
- Code will be peer reviewed and released on Github.
- A few hours to develop a 1st solution.

Bonus point:
- Deploy the solution on the cloud.
- Document the code.


## 2. Modelisation & Development


### 2.1. Problem understanding and simplification

Given the constraints, I decided to focus my efforts on Questions that have an accepted answer:

<img src = "/img/answered_question.png" height="300">

The rational being that if an answer is accepted, it is more likely that it mentions a solution to the problem and/or a root cause.


I identified 3 potential approaches to solve the problem on this type of questions:

- Building a Q&A system:
    - Given a passage sentence (a StackOverFlow answer) and a question (either "How to solve the problem?" or "Why is this happening?"), extract the entities from the passage sentence.
    - That being said, we only ask 2 types of questions ("how to" and "why"), which means a Q&A system might be overkill for this problem.
    > <img src = "/img/q_a_system.jpg" height="150">
    
- Building a YOLO-like model but for NLP:
    - YOLO is a system for detecting objects in images. It both predicts the class of the object and its position (by giving a bounding box).
    - We could build a model inspired by this approach that predicts the "bounding box" (`start_at`, `end_at` indices) within the text and the class (`solution`, `root_cause`).
    - That being said, a quick look-up on Google did not give any link towards a YOLO-like model applied to NLP.

- Building a simple 3-classes classifier at the sentence level:
    - A simpler approach would be to build a classifier at the sentence level that predicts if the sentence belongs to one of the classes `solution`, `root_cause`, `other`.
    - This approach would give a full sentence as a result to the initial problem without completely filtering the sentence from the content not relevant to the solution.


### 2.2. Project structure

To develop this project I followed these steps:

| step |      functionnality      |                                                                                                        description                                                                                                       |                                                                    url                                                                    |
|:----:|:------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------:|
|   1  |        WebCrawler        | - crawler to collect questions & answers data - relies on StackOverflow API - can automatically generate an API key - useful for creating a training set                                                                 | [crawler](https://github.com/SachaIZADI/stack-underflow/blob/feature/ReadMe/stack_under_flow/crawler/stack_over_flow.py)                  |
|   2  |       Preprocessing      | - methods to preprocess the html content of an answer - cleans text (remove tags, lemmatizes, tokenizes...) - vectorizes (custom word2vec trained on the dataset)                                                        | [preprocessing](https://github.com/SachaIZADI/stack-underflow/blob/feature/ReadMe/stack_under_flow/model/preprocessing.py)                |
|   3  |      Data Labelling      | - interface (CLI) to label the data more easily                                                                                                                                                                          | [labelling](https://github.com/SachaIZADI/stack-underflow/blob/feature/ReadMe/stack_under_flow/labelling_tool/labelling_cli.py)           |
| 3bis | Unsupervised exploration | - tried (but failed) to analyze the dataset with Kmeans - aim was to identify potential clusters that would include `solution`, `root_cause` and avoid hand labelling - interactive visualizations                       | [kmeans](https://github.com/SachaIZADI/stack-underflow/blob/feature/ReadMe/stack_under_flow/adhoc_scripts/unsupervised_exploration.ipynb) |
|   4  |        Classifier        | - gradient-boosted classifier that classifies each sentence in `solution`, `root_cause` or `other` - little hyperparameter-tuning was done, but the model performance were estimated using cross-validation and hold-out | [classifier](https://github.com/SachaIZADI/stack-underflow/blob/feature/ReadMe/stack_under_flow/model/classifier.py)                      |
|   5  |         Interface        | - interface (CLI) to use the model & play with it - pass an url or a question id and visualize the results of the algorithm                                                                                              | [interface](https://github.com/SachaIZADI/stack-underflow/blob/feature/ReadMe/stack_under_flow/stack_under_flow_cli.py)                   |


A few examples of the features that were developed during this project:
- Interactive visualisation of the KMeans results. The approach did not work at the end (I identified clusters related to the technologies mentionned in the questions e.g. numpy, tensorflow, docker, etc. instead of `solution` or `root_cause`) 

![](/img/tsne.gif)

- Labelling interface
<img src = "/img/labelling.gif" height="400">

### 2.3. Results

The definition of `root_cause` and `solution` is a bit fuzzy, and while labelling the data it was not always very clear if a sentence really belonged to one class or another.
Therefore, the performance of the model depends a lot on the quality of this labelled data ...

I analyzed the performance of the model:
- with a 5-fold cross-validation using `macro` metrics,
- and split the data in 70%/30% train-test to generate a classification report and a confusion matrix

<img src = "/img/classification_result.png" height="300">

As I did not use any technique to handle the class imbalance, it appears that the most common class (`other`) is the best predicted. Performance on the `root_cause` class is acceptable, while the prediction on the `solution` class is not very powerful...
One potential explanation is that `root_cause` explanations are often longer than a simple solution and may contain more signal.

A few examples of predictions (the first 2 seem to work, the last one is a failure) using the interface: 

<img src = "/img/cli_classifier_failed.png" height="300">

<img src = "/img/cli_classifier_root_cause.png" height="300">

<img src = "/img/cli_classifier_solution.png" height="300">


## 3. How to reproduce the code
Run the tests: `PYTHONPATH=. py.test`


Under construction