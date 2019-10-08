from stack_under_flow.model.preprocessing import Preprocessor
from stack_under_flow.model.classifier import Classifier

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_validate, train_test_split
import joblib

import json
import numpy as np
import collections


def main():
    with open(f"/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data/data_labeled.json", "r") as f:
        labeled_data_json = json.loads(f.read())

    labeled_data = [{
        "sentence": example["sentence"],
        "label": example["label"],
    } for data in labeled_data_json for example in data["labels"]]

    X_str = np.array([example["sentence"] for example in labeled_data])
    y = np.array([example["label"] for example in labeled_data])

    print("\n")
    print(collections.Counter(y))
    print("\n")

    preprocessor = Preprocessor(
        word2vec_model_src="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/word2vec.model"
    )

    X = preprocessor.transform(X_str)

    to_remove = [i for i in range(len(X)) if X[i].shape != (1, 100)]
    X = np.vstack([X[i] for i in range(len(X)) if i not in to_remove])
    y = np.array([y[i] for i in range(len(y)) if i not in to_remove])

    # Cross validation
    classifier = Classifier()

    metrics = ['f1_macro','accuracy','precision_macro','recall_macro']
    scores = cross_validate(classifier, X, y, cv=5, scoring=metrics)
    for metric in metrics:
        print(f"{metric}: {round(np.mean(scores[f'test_{metric}']),3)} +/- {round(np.std(scores[f'test_{metric}']),3)}")
    print("\n")

    # Hold-out
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3
    )
    classifier = Classifier()

    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    print(classification_report(y_test, y_pred))

    print(confusion_matrix(y_test, y_pred))

    # Final training
    classifier = Classifier()
    classifier.fit(X, y)

    joblib.dump(
        classifier.classifier,
        "/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/gradient_boosting_classifier.model"
    )

    joblib.dump(
        classifier.scaler,
        "/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/scaler.model"
    )


if __name__ == "__main__":
    main()