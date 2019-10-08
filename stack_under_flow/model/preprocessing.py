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

    def extract_clean_sentences(self, X:Iterable[str]):
        html_2_text_vect = np.vectorize(self.html_2_text)
        expand_contraction_vect = np.vectorize(self.expand_contraction)
        get_sentences_vect = np.vectorize(self.get_sentences, otypes=[list])

        X_transformed = html_2_text_vect(X)
        X_transformed = expand_contraction_vect(X_transformed)
        X_transformed = get_sentences_vect(X_transformed)

        return X_transformed

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
            X_transformed_final = [
                np.array(
                    [x[i].sum(axis=0) for i in range(len(x))]
                ) for x in X_transformed_final
            ]

        return X_transformed_final
