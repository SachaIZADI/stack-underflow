from stack_under_flow.model.preprocessing import Preprocessor
import json


def main():
    preprocessor = Preprocessor(word2vec_model_src="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/word2vec.model")
    with open("/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data/data_python.json", "r") as f:
        json_data = json.loads(f.read())

    text = [json_data[0]["answer_body"], json_data[1]["answer_body"]]
    x_str = preprocessor.transform(text, vectorize=False)
    x = preprocessor.transform(text)

    print("preprocessed_text:", x_str)
    print(f"len(x)={len(x)}  ", f"x[0].shape={x[0].shape}  ", f"x[1].shape={x[1].shape}  ")

if __name__=="__main__":
    main()
