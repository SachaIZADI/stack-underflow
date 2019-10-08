# StackUnderflow

## 1. Problem & context

This project is an home assignment given to me by [PacketAI](http://www.packetai.co/). The problem is stated as:

We want to build a tool that scrapes the Stackoverflow website and for every question (generally a question reflects a symptom of a problem) it predicts two things:
- The root cause of the problem
- The solution (answer) of the problem

Given the following constraints:
- Build the basics of a long term project, your code needs to be easily understood and reusable.
- Code does not need to be optimal in terms of performance but needs to be fast enough to provide a good user experience.
- Code needs to be trusted: it does what it is meant to do.
- Code will be peer reviewed and released on Github.
- Roughly 2 hours to develop a solution.

Bonus point:
- Deploy the solution on the cloud.
- Document the code.

This whole ReadMe details my though process about approaching this problem.


## 2. Modelisation

### 2.1. Problem understanding and simplification

The problem consists in giving an answer (solution + root cause) to any question asked on StackOverflow. There are 2 kinds of questions on StackOverflow:

1. questions that do have a full top-voted answer (solution + root cause): our problem boils down to extracting the most relevant information within the question.

2. questions that do not have any answer: our problem boils down to generating an answer to the question.

3. questions that have a partial top-voted answer (either only the solution or the root cause): our problem is a mix of the 2 of them.

4. questions that have some partial or full answers (but not a top-voted one)



For the **1st** type of questions, we forsee 3 approaches for solving the problem:
- Building a Q&A system:
    - Given a passage sentence (a StackOverFlow answer) and a question (either "How to solve the problem?" or "Why is this happening?"), extract the entities from the passage sentence.
    - That being said, we only ask 2 types of questions ("how to" and "why"), which means a Q&A system might be overkill for this problem.
    
    <img src = "/img/q_a_system.jpg" height="100">
    
- Building a YOLO-like model but for NLP:
    - YOLO is a system for detecting objects in images. It both predicts the class of the object and its position (by giving a bounding box).
    - We could build a model inspired by this approach that predicts the "bounding box" (`start_at`, `end_at` indices) within the text and the class (`solution`, `root_cause`).
    - That being said, a quick look-up on Google did not give any link towards a YOLO-like model applied to NLP.

- Building a simple 3-classes classifier at the sentence level:
    - A simpler approach would be to build a classifier at the sentence level that predicts if the sentence belongs to one of the classes `solution`, `root_cause`, `other`.
    - This approach would give a full sentence as a result to the initial problem without completely filtering the sentence from the content not relevant to the solution.


For the **2nd** type of questions, we think about 2 approaches for solving the problem:
- Learn a language model over StackOverflow and generate an answer from the blue, a bit like in [Write with Transformers](https://transformer.huggingface.co/). 
    - This would require fine tuning a BIG language model and fine-tuning it on domain specific data.
    - It is highly likely that the model will be able to generate grammatically correct sentences with zero meaning ... See the following example
    
    <img src = "/img/write_with_transformer.png" height="300">
    
- Identify a similar question asked on StackOverflow which **has** a provided answer and solve the previous 3rd or 1st cases.
    - This would require building/using a search engine to recommend the most related/similar questions.
    - Fortunately, we could try this approach by scraping the results of ready-made search engines (e.g. Google's or StackOverflow's)
    
    <img src = "/img/search_engine_so.png" height="200">
    <img src = "/img/search_engine_google.png" height="200">
    
For the **3rd & 4th** types of questions, we identify 2 approaches for solving the problem:

- Iterate through all the answers, besides the top-voted one, and apply the solution from 1st type of questions. If no `solution` or `root_cause` is found ...
- ... Apply solution for 2nd type of question and iterate through similar questions.


**Given the time constraints, we choose to focus our efforts only on the 1st type of questions.**


### 2.2. Constraints

|     Tag     |       Constraint      |             Impact            |                                Solution                               | Priority |
|:-----------:|:---------------------:|:-----------------------------:|:---------------------------------------------------------------------:|:--------:|
| project mgt | ~2h                   | Better done than perfect      | Simple model                                                          | High     |
| project mgt | peer-reviewed code    | Clean & functional code       | Git workflow + Limited usage of Jupyter                               | High     |
| project mgt | reusable code         | Clean & functional code       | Modular code + basic documentation                                    | High     |
| project mgt | trustworthy code      | Code needs to be tested       | pytest + CI/CD (GitHub actions)                                       | Medium   |
| data        | no data is provided   | Build an adhoc dataset        | Scrap StackOverFlow                                                   | High     |
| data        | no label is provided  | Supervised learning is costly | Label data by hand / Semi-supervised learning / Unsupervised learning | High     |
| data        | no data is provided   | DeepLearning is out of reach  | Simple model / or fine-tuning                                         | High     |
| hardware    | no GPU                | DeepLearning is out of reach  | Simple model (statistical learning + feature engineering)             | High     |
| model       | fast & scalable model | Optimize inference time       | Simple model (statistical learning + feature engineering)             | High     |
| production  | deployable model      | APIze the model / pipeline    | Docker + Flask + Setup a server (AWS, Heroku ...)                     | Low      |

### 2.3. Draft of a solution

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