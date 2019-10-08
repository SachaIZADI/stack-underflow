from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import StandardScaler
import numpy as np

from stack_under_flow.model.preprocessing import Preprocessor

from typing import List, Iterable


class Classifier(BaseEstimator, TransformerMixin):

    def __init__(self, scaler_model_src: str = None, classifier_model_src: str = None):
        # TODO load model
        if scaler_model_src is None:
            self.scaler = StandardScaler()
        else:
            raise NotImplementedError
        if classifier_model_src is None:
            self.classifier = MultinomialNB()
        else:
            raise NotImplementedError

    def fit(self, X: np.array, y: np.array):
        X_scaled = self.scaler.fit_transform(X)
        self.classifier.fit(X_scaled, y)
        return self

    def transform(self, X: np.array):
        X_scaled = self.scaler.transform(X)
        return self.classifier.predict(X_scaled)


class ClassifierPipeline:

    def __init__(
            self,
            word2vec_model_src: str,
            scaler_model_src: str,
            classifier_model_src: str
    ):
        self.preprocessor = Preprocessor(
            word2vec_model_src=word2vec_model_src
        )
        self.classifier = Classifier(
            scaler_model_src = scaler_model_src,
            classifier_model_src=classifier_model_src
        )

    def predict(self, X: Iterable[str]):
        return