from sklearn.base import BaseEstimator, TransformerMixin
import re
from bs4 import BeautifulSoup
import gensim
from typing import List, Iterable
import numpy as np
import nltk



class Preprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, word2vec_model_src: str = None):
        self.code_token = {
            "short": "$shortcode$",
            "long": "$longcode$"
        }
        self.url_token = "$url$"
        self.contraction_list = {
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he would",
            "he'd've": "he would have",
            "he'll": "he will",
            "he'll've": "he will have",
            "he's": "he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how is",
            "i'd": "i would",
            "i'd've": "i would have",
            "i'll": "i will",
            "i'll've": "i will have",
            "i'm": "i am",
            "i've": "i have",
            "isn't": "is not",
            "it'd": "it had",
            "it'd've": "it would have",
            "it'll": "it will",
            "it'll've": "it will have",
            "it's": "it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she would",
            "she'd've": "she would have",
            "she'll": "she will",
            "she'll've": "she will have",
            "she's": "she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so is",
            "that'd": "that would",
            "that'd've": "that would have",
            "that's": "that is",
            "there'd": "there had",
            "there'd've": "there would have",
            "there's": "there is",
            "they'd": "they would",
            "they'd've": "they would have",
            "they'll": "they will",
            "they'll've": "they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we had",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'll": "what will",
            "what'll've": "what will have",
            "what're": "what are",
            "what's": "what is",
            "what've": "what have",
            "when's": "when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where is",
            "where've": "where have",
            "who'll": "who will",
            "who'll've": "who will have",
            "who's": "who is",
            "who've": "who have",
            "why's": "why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'alls": "you alls",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you had",
            "you'd've": "you would have",
            "you'll": "you you will",
            "you'll've": "you you will have",
            "you're": "you are",
            "you've": "you have"
        }

        if word2vec_model_src is None:
            self.word2vec_model = None
        else:
            self.word2vec_model = gensim.models.Word2Vec.load(word2vec_model_src)

    # --------------------------

    def html_2_text(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        code_snippets = soup.find_all("code")
        for snippet in code_snippets:
            if snippet.text.count("\n") == 0:
                snippet.string = self.code_token["short"]
            else:
                snippet.string = self.code_token["long"]

        text_from_html = soup.text

        text_from_html = re.sub(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            self.url_token,
            text_from_html
        )
        return text_from_html.lower()

    # --

    def expand_contraction(self, text: str) -> str:
        c_re = re.compile('(%s)' % '|'.join(self.contraction_list.keys()))

        def replace(match):
            return self.contraction_list[match.group(0)]

        return c_re.sub(replace, text.lower())

    # --

    def get_sentences(self,
                      document: str,
                      remove_punctuation: bool = True,
                      lemmatize: bool = True) -> List[str]:

        sentences = gensim.summarization.textcleaner.get_sentences(document)

        def merge_sentence_with_code_snippet(sentences):
            sentences_copy = list(sentences)
            for i in range(1, len(sentences_copy)):
                if sentences_copy[i] in self.code_token.values():
                    sentences_copy[i-1] = " ".join([sentences_copy[i-1], sentences_copy[i]])
            return list(filter(lambda elt: elt not in self.code_token, sentences_copy))

        sentences = merge_sentence_with_code_snippet(sentences)

        if remove_punctuation:
            sentences = [re.sub('[!?.,:;\-\(\)\'\"#*]', ' ', sentence) for sentence in sentences]

        if lemmatize:
            def full_lematize(word: str) -> str:
                lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
                word = lemmatizer.lemmatize(word, "v")
                word = lemmatizer.lemmatize(word, "a")
                word = lemmatizer.lemmatize(word)
                return word
            sentences = [
                " ".join([full_lematize(word) for word in sentence.split()])
                for sentence in sentences
            ]
        return list(sentences)

    # --

    def get_tokens_from_sentence(self, sentence: str):
        return sentence.split()

    def get_tokens_from_sentences(self, sentences: Iterable[str]):
        get_tokens_from_sentence_vect = np.vectorize(self.get_tokens_from_sentence, otypes=[list])
        return list(get_tokens_from_sentence_vect(sentences))

    # --------------------------

    def train_Word2Vec(self, sentences: List[str]):

        model = gensim.models.Word2Vec(
            sentences,
            sg=0,
            size=100,
            window=15,
            min_count=2,
            workers=2,
            iter=50)

        return model

    # --

    def save_Word2Vec(self, dst_file: str):
        self.word2vec_model.save(dst_file)

    # --

    def vectorize_word(self, word: str) -> np.array:
        if word not in self.word2vec_model.wv:
            return
        else:
            return self.word2vec_model.wv[word]

    # --

    def vectorize_words(self, words: List[str]):
        return np.array([self.vectorize_word(word) for word in words if self.vectorize_word(word) is not None])

    # --------------------------

    def fit(self, X: Iterable[str], y=None):

        html_2_text_vect = np.vectorize(self.html_2_text)
        expand_contraction_vect = np.vectorize(self.expand_contraction)
        get_sentences_vect = np.vectorize(self.get_sentences, otypes=[list])
        get_tokens_from_sentences_vect = np.vectorize(self.get_tokens_from_sentences, otypes=[list])

        X_transformed = html_2_text_vect(X)
        X_transformed = expand_contraction_vect(X_transformed)
        X_transformed = get_sentences_vect(X_transformed)
        X_transformed = get_tokens_from_sentences_vect(X_transformed)

        X_transformed_reshaped = []
        for i in range(X_transformed.shape[0]):
            X_transformed_reshaped.extend(X_transformed[i])

        word2vec_model = self.train_Word2Vec(X_transformed_reshaped)
        self.word2vec_model = word2vec_model

        return self


    def transform(self, X: Iterable[str], y=None, vectorize=True, reducer="mean"):

        if reducer not in {"mean", None}:
            raise NotImplementedError('Only reducer="mean" is implemented so far')

        html_2_text_vect = np.vectorize(self.html_2_text)
        expand_contraction_vect = np.vectorize(self.expand_contraction)
        get_sentences_vect = np.vectorize(self.get_sentences, otypes=[list])
        get_tokens_from_sentences_vect = np.vectorize(self.get_tokens_from_sentences, otypes=[list])

        X_transformed = html_2_text_vect(X)
        X_transformed = expand_contraction_vect(X_transformed)
        X_transformed = get_sentences_vect(X_transformed)
        X_transformed = get_tokens_from_sentences_vect(X_transformed)

        if not vectorize:
            return X_transformed

        X_transformed_final = []

        for x_document in X_transformed:

            X_transformed_final.append(
                [self.vectorize_words(x_sentence) for x_sentence in x_document]
            )

        if reducer is not None:
            X_transformed_final = [np.array([x[i].sum(axis=0) for i in range(len(x))]) for x in X_transformed_final]


        return X_transformed_final



"""
if __name__ == "__main__":

    preprocessor = Preprocessor()
    html_doc = "<p>I am trying to reconcile my understand of LSTMs and pointed out here in <a href=\"http://colah.github.io/posts/2015-08-Understanding-LSTMs/\" rel=\"noreferrer\">this post by Christopher Olah</a> implemented in Keras. I am following the <a href=\"http://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/\" rel=\"noreferrer\">blog written by Jason Brownlee</a> for the Keras tutorial. What I am mainly confused about is, </p>\n\n<ol>\n<li>The reshaping of the data series into <code>[samples, time steps, features]</code> and,</li>\n<li>The stateful LSTMs </li>\n</ol>\n\n<p>Lets concentrate on the above two questions with reference to the code pasted below:</p>\n\n<pre><code># reshape into X=t and Y=t+1\nlook_back = 3\ntrainX, trainY = create_dataset(train, look_back)\ntestX, testY = create_dataset(test, look_back)\n\n# reshape input to be [samples, time steps, features]\ntrainX = numpy.reshape(trainX, (trainX.shape[0], look_back, 1))\ntestX = numpy.reshape(testX, (testX.shape[0], look_back, 1))\n########################\n# The IMPORTANT BIT\n##########################\n# create and fit the LSTM network\nbatch_size = 1\nmodel = Sequential()\nmodel.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True))\nmodel.add(Dense(1))\nmodel.compile(loss='mean_squared_error', optimizer='adam')\nfor i in range(100):\n    model.fit(trainX, trainY, nb_epoch=1, batch_size=batch_size, verbose=2, shuffle=False)\n    model.reset_states()\n</code></pre>\n\n<p>Note: create_dataset takes a sequence of length N and returns a <code>N-look_back</code> array of which each element is a <code>look_back</code> length sequence.    </p>\n\n<h1>What is Time Steps and Features?</h1>\n\n<p>As can be seen TrainX is a 3-D array with Time_steps and Feature being the last two dimensions respectively (3 and 1 in this particular code). With respect to the image below, does this mean that we are considering the <code>many to one</code> case, where the number of pink boxes are 3? Or does it literally mean the chain length is 3 (i.e. only 3 green boxes considered). <a href=\"https://i.stack.imgur.com/kwhAP.jpg\" rel=\"noreferrer\"><img src=\"https://i.stack.imgur.com/kwhAP.jpg\" alt=\"enter image description here\"></a></p>\n\n<p>Does the features argument become relevant when we consider multivariate series? e.g. modelling two financial stocks simultaneously? </p>\n\n<h1>Stateful LSTMs</h1>\n\n<p>Does stateful LSTMs mean that we save the cell memory values between runs of batches? If this is the case, <code>batch_size</code> is one, and the memory is reset between the training runs so what was the point of saying that it was stateful. I'm guessing this is related to the fact that training data is not shuffled, but I'm not sure how.</p>\n\n<p>Any thoughts?\nImage reference: <a href=\"http://karpathy.github.io/2015/05/21/rnn-effectiveness/\" rel=\"noreferrer\">http://karpathy.github.io/2015/05/21/rnn-effectiveness/</a></p>\n\n<h2>Edit 1:</h2>\n\n<p>A bit confused about @van's comment about the red and green boxes being equal. So just to confirm, does the following API calls correspond to the unrolled diagrams? Especially noting the second diagram (<code>batch_size</code> was arbitrarily chosen.):\n<a href=\"https://i.stack.imgur.com/sW207.jpg\" rel=\"noreferrer\"><img src=\"https://i.stack.imgur.com/sW207.jpg\" alt=\"enter image description here\"></a>\n<a href=\"https://i.stack.imgur.com/15V2C.jpg\" rel=\"noreferrer\"><img src=\"https://i.stack.imgur.com/15V2C.jpg\" alt=\"enter image description here\"></a></p>\n\n<h2>Edit 2:</h2>\n\n<p>For people who have done Udacity's deep learning course and still confused about the time_step argument, look at the following discussion: <a href=\"https://discussions.udacity.com/t/rnn-lstm-use-implementation/163169\" rel=\"noreferrer\">https://discussions.udacity.com/t/rnn-lstm-use-implementation/163169</a></p>\n\n<h2>Update:</h2>\n\n<p>It turns out <code>model.add(TimeDistributed(Dense(vocab_len)))</code> was what I was looking for. Here is an example: <a href=\"https://github.com/sachinruk/ShakespeareBot\" rel=\"noreferrer\">https://github.com/sachinruk/ShakespeareBot</a></p>\n\n<h2>Update2:</h2>\n\n<p>I have summarised most of my understanding of LSTMs here: <a href=\"https://www.youtube.com/watch?v=ywinX5wgdEU\" rel=\"noreferrer\">https://www.youtube.com/watch?v=ywinX5wgdEU</a></p>\n"
    print(preprocessor.transform(html_doc))
"""