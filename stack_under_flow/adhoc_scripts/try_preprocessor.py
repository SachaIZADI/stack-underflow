from stack_under_flow.model.preprocessing import Preprocessor
import json

def main():
    preprocessor = Preprocessor(word2vec_model_src="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/word2vec.model")
    with open("/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data/data_python.json", "r") as f:
        json_data = json.loads(f.read())

    text = json_data[0]["answer_body"]
    x_str = preprocessor.transform([text], vectorize=False)
    x = preprocessor.transform([text])

    print("preprocessed_text:", x_str)

    print("len(x):", len(x), len(x) == 1)
    print("len(x[0]):", len(x[0]), len(x[0])==len(x_str[0]))
    print("x[0][0].shape:", x[0][64].shape)

    print(x[0][0][0].shape)

if __name__=="__main__":
    main()