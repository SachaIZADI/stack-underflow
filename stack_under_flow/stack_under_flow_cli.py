from pyfiglet import figlet_format
from termcolor import colored
import click
import json
import random
from stack_under_flow.model import ClassifierPipeline
from stack_under_flow.crawler import StackOverflowCrawler
from urllib.parse import urlparse


@click.command()
@click.option(
    "-url", "--url",
    type=str,
    default=None,
)
@click.option(
    "-id", "--question_id",
    type=str,
    default=None,
)
def main(url, question_id):

    print(colored(figlet_format("StackUnderflow\nCLI"), "blue"))

    if url is None and question_id is None:
        print(colored("-url or -id should be specified", "red"))
        return

    def extract_id(url: str) -> str:
        return urlparse(url).path.replace("/questions/", "").split("/")[0]

    if question_id is None:
        question_id = extract_id(url)

    crawler = StackOverflowCrawler()

    question_data = crawler.get_questions_by_id(question_id)[0]
    question_title = question_data.get("title", None)
    answer_id = question_data.get("accepted_answer_id", None)
    if answer_id is None:
        print(colored(f"Question {question_id} has no accepted answer yet, sorry...", "red"))
        return

    answer_data = crawler.get_answer_by_id(answer_id)
    answer_body = answer_data[0]["body"]

    print(colored(f"****** QUESTION: {question_title} ******", "green"))

    classifier_pipeline = ClassifierPipeline(
        word2vec_model_src="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/word2vec.model",
        scaler_model_src="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/scaler.model",
        classifier_model_src="/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/model/gradient_boosting_classifier.model"
    )

    y = classifier_pipeline.predict([answer_body])

    COLORS = {"solution": "cyan", "root_cause": "yellow", "other": "white"}
    print("----- Legend:", colored("solution", COLORS["solution"]), "&", colored("root_cause", COLORS["root_cause"]), "-----")

    sentences = classifier_pipeline.preprocessor.extract_raw_sentences(answer_body)

    for i in range(len(y)):
        print(colored(sentences[i], COLORS[y[i]]))


if __name__ == "__main__":
    main()
