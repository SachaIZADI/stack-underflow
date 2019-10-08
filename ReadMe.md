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

|     Tag     |       Constraint      |             Impact            |                                Solution                               | Priority |
|:-----------:|:---------------------:|:-----------------------------:|:---------------------------------------------------------------------:|:--------:|
| project mgt | ~2h                   | Better done than perfect      | Simple model                                                          | High     |
| project mgt | peer-reviewed code    | Clean & functional code       | Git workflow + Limited usage of Jupyter                               | High     |
| projec  mgt | reusable code         | Clean & functional code       | Modular code + basic documentation                                    | High     |
| project mgt | trustworthy code      | Code needs to be tested       | pytest + CI/CD (GitHub actions)                                       | Medium   |
| data        | no data is provided   | Build an adhoc dataset        | Scrap StackOverFlow                                                   | High     |
| data        | no label is provided  | Supervised learning is costly | Label data by hand / Semi-supervised learning / Unsupervised learning | High     |
| data        | no data is provided   | DeepLearning is out of reach  | Simple model / or fine-tuning                                         | High     |
| hardware    | no GPU                | DeepLearning is out of reach  | Simple model (statistical learning + feature engineering)             | High     |
| model       | fast & scalable model | Optimize inference time       | Simple model (statistical learning + feature engineering)             | High     |
| production  | deployable model      | APIze the model / pipeline    | Docker + Flask + Setup a server (AWS, Heroku ...)                     | Low      |


Based on the analysis we made of the problem and given the constraints, we will:

1. Build a scrapper to extract the content of a StackOverflow question (question, answers, metadata)
2. Build a dataset of ~100's or ~1000's of questions
3. Build a 3-class classifier (`solution`, `root_cause`, `other`) at the sentence level.
    1. The model:
        - A +/- advanced model would be to use the content from **both** the sentence **and** the question to predict the class of the sentence: ![equation](https://latex.codecogs.com/gif.latex?\mathbb{P}(label=solution&space;|&space;question,&space;sentence&space;))
        - We will adopt a simpler approach and **only** use the content from the sentence: ![equation](https://latex.codecogs.com/gif.latex?\mathbb{P}(label=solution&space;|&space;sentence&space;)). Our rational is that the `solution` class could be predicted by textual elements such as {`I suggest that`, `you should do`} and that an top-voted answer is related enough to the question that we do not need to check for the relevance of the sentence with respect to the initial question.
    2. The labels:
        - First try if an unsupervised approach could yield to well identified classes that includes  (`solution`, `root_cause`), this would avoid having to manually label sentences. Otherwise we'll have to do a bit of data labelling.
    3. Extracting sentences:
        - StackOverflow answers not only contain natural language sentences, they also contain code snippets. We might have to replace all code snippets by a [CODE] token.
    4. The features:
        - We will remove the stopwords
        - Use a bag-of-words model on top of 1,2,3-grams (to capture relations such as `import library works)`
        - Train our own word embeddings
        - We also might use additional metadata (e.g. Markdown elements) as a solution.


![](/img/tsne.gif)

<img src = "/img/labelling.gif" height="400">

<img src = "/img/classification_result.png" height="250">

<img src = "/img/cli_classifier_failed.png" height="250">

<img src = "/img/cli_classifier_root_cause.png" height="250">

<img src = "/img/cli_classifier_solution.png" height="250">


## 3. How to reproduce the code
Run the tests: `PYTHONPATH=. py.test`


Under construction