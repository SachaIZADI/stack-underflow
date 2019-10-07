from stack_under_flow.model.preprocessing import Preprocessor
import json

def main():

    def extract_text(tag: str):
        with open(
                f"/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data/data_{tag}.json",
                "r") as f:
            json_data = json.loads(f.read())

        return [data.get("answer_body") for data in json_data if data.get("answer_body") is not None]

    full_text = []
    for tag in [
        "anaconda", "git", "gensim", "nltk", "pycharm", "jupyter", "keras",
        "matplotlib", "numpy", "python", "pytorch", "tensorflow", "django",
        "flask", "docker", "selenium"
    ]:
        full_text.extend(extract_text(tag))
    print("---- Nb of documents:", len(full_text))

    print("---- Preprocessing the data & training Word2Vec embeddings")
    preprocessor = Preprocessor()
    preprocessor.fit(X=full_text)
    preprocessor.save_Word2Vec(dst_file="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/word2vec.model")
    print("---- Word2Vec embeddings saved")

if __name__ == "__main__":
    main()