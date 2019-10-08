from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

from stack_under_flow.model.preprocessing import Preprocessor

from typing import List, Iterable


class Classifier(BaseEstimator, ClassifierMixin):

    def __init__(self, scaler_model_src: str = None, classifier_model_src: str = None):

        if scaler_model_src is None:
            self.scaler = StandardScaler()
        else:
            self.scaler = joblib.load(scaler_model_src)

        if classifier_model_src is None:
            self.classifier = GradientBoostingClassifier()
        else:
            self.classifier = joblib.load(classifier_model_src)

    def fit(self, X: np.array, y: np.array):
        X_scaled = self.scaler.fit_transform(X)
        self.classifier.fit(X_scaled, y)
        return self

    def predict(self, X: np.array):
        X_scaled = self.scaler.transform(X)
        return self.classifier.predict(X_scaled)

    def predict_proba(self, X: np.array):
        X_scaled = self.scaler.transform(X)
        return self.classifier.predict_proba(X_scaled)


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
            scaler_model_src=scaler_model_src,
            classifier_model_src=classifier_model_src
        )

    def predict(self, X: Iterable[str], with_proba=False):

        X_transformed = self.preprocessor.transform(X)
        # TODO: remove this patch
        try:
            y_pred = self.classifier.predict(X_transformed)
        except:
            y_pred = self.classifier.predict(X_transformed[0])

        if with_proba:
            try:
                proba_pred = self.classifier.predict_proba(X_transformed)
            except:
                proba_pred = self.classifier.predict_proba(X_transformed[0])

            return y_pred, proba_pred

        return y_pred
