from stack_under_flow.crawler.stack_over_flow import StackOverflowDataCollector
from typing import List


def main(tags: List[str]):

    s = StackOverflowDataCollector()
    s.crawler.generate_api_key()
    print("---- Starting to collect questions")
    q = s.collect_sample_questions(tags=tags)
    print("---- Starting to collect answers to questions")
    a = s.collect_answers(clean_questions=q)

    tags_to_str = "_".join(tags)
    s.save_data(
        data=a,
        dst_file=f"/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/data/data_{tags_to_str}.json"
    )


if __name__ == "__main__":
    main(tags=["selenium"])
