from pyfiglet import figlet_format
from termcolor import colored
import click
import json
import random
from stack_under_flow.model.preprocessing import Preprocessor


def load_full_data(path_to_data_folder: str = "/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data"):

    def extract_text(tag: str):
        with open(f"{path_to_data_folder}/data_{tag}.json", "r") as f:
            json_data = json.loads(f.read())

        return [
            {
                "answer_body": data.get("answer_body"),
                "title": data.get("title"),
                "question_id": data.get("question_id")
            } for data in json_data if data.get("answer_body") is not None
        ]

    full_data = []
    for tag in [
        "anaconda", "git", "gensim", "nltk", "pycharm", "jupyter", "keras",
        "matplotlib", "numpy", "python", "pytorch", "tensorflow", "django",
        "flask", "docker", "selenium"
    ]:
        full_data.extend(extract_text(tag))

    return full_data


def sample_data_to_label(
        nb_examples: int = 10,
        path_to_data_folder: str = "/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data"):

    with open(f"{path_to_data_folder}/data_labeled.json", "r") as f:
        json_data = json.loads(f.read())
    labeled_questions = [data.get("question_id") for data in json_data]

    full_data = load_full_data(path_to_data_folder=path_to_data_folder)
    full_data_filtered = [data for data in full_data if data["question_id"] not in labeled_questions]

    sampled_data = random.choices(full_data_filtered, k=nb_examples)

    return sampled_data




@click.command()
@click.option(
    "-n", "--nb_examples",
    type=int,
    default=10,
)
@click.option(
    "-path_data", "--path_to_data",
    type=str,
    default="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data",
)
def main(path_to_data, nb_examples):
    print(colored(figlet_format("StackUnderflow \nLabellingTool"), "blue"))

    data_to_label = sample_data_to_label(
        path_to_data_folder=path_to_data,
        nb_examples=nb_examples
    )

    preprocessor = Preprocessor()
    LABEL = {1: "solution", 2: "root_cause", 3: "other"}

    for i in range(len(data_to_label)):
        example = data_to_label[i]
        sentences = preprocessor.extract_clean_sentences(example["answer_body"])
        print(colored(f"**** QUESTION: {example['title']} ****", "green"))
        labels = []

        for sentence in sentences:

            print(colored(f"{sentence}", "blue"))
            label_int = eval(input("Type -- 1='solution' -- 2='root_cause' -- 3='other'"))

            labels.append({
                "sentence": sentence,
                "label": LABEL[label_int]
            })

        data_to_label[i]["labels"] = labels

    with open(f"{path_to_data}/data_labeled.json", "r") as f:
        data_already_label = json.loads(f.read())

    full_data = []
    full_data.extend(data_already_label)
    full_data.extend(data_to_label)

    with open(f"{path_to_data}/data_labeled.json", "w") as f:
        json.dump(full_data, f)

    print(f"Data was saved to {path_to_data}/data_labeled.json")


if __name__ == "__main__":
    main()
