import requests
from typing import List


class StackOverflowCrawler:

    def __init__(self, api_key: str = None):
        self.quota = None
        self.api_key = api_key

    @staticmethod
    def get_quota(res_json: dict):
        return {
            "quota_max": res_json["quota_max"],
            "quota_remaining": res_json["quota_remaining"]
        }

    def search_question_by_tag(self, tag: str) -> List[dict]:
        search_url = f"https://api.stackexchange.com/2.2/search?order=desc&sort=votes&tagged={tag}&site=stackoverflow"
        res = requests.get(search_url, params={"key": self.api_key})
        res_json = res.json()
        self.quota = self.get_quota(res_json)
        return res_json["items"]

    def get_questions_by_id(self, id: int) -> dict:
        question_url = f"https://api.stackexchange.com/2.2/questions/{id}?order=desc&sort=activity&site=stackoverflow"
        res = requests.get(question_url, params={"key": self.api_key})
        res_json = res.json()
        self.quota = self.get_quota(res_json)
        return res_json["items"]

    def get_answer_by_id(self, id: int) -> dict:
        answer_url = f"https://api.stackexchange.com/2.2/answers/{id}?order=desc&sort=activity&site=stackoverflow&filter=!9Z(-wzu0T"
        res = requests.get(answer_url, params={"key": self.api_key})
        res_json = res.json()
        self.quota = self.get_quota(res_json)
        return res_json["items"]

    def get_sample_questions(self, tags: list, is_answered: bool = True) -> List[dict]:
        sample_questions = []
        for tag in tags:
            questions = self.search_question_by_tag(tag)
            if is_answered:
                filtered_questions = [question for question in questions if question["is_answered"]]
                sample_questions.extend(filtered_questions)
            else:
                sample_questions.extend(questions)

        return sample_questions


class StackOverflowDataSet:

    def __init__(self, api_key: str = None, dst_file: str = None):
        self.api_key = api_key
        self.crawler = StackOverflowCrawler(api_key=api_key)
        self.dst_file = dst_file

    def collect_sample_questions(self, tags: list):
        raw_questions = self.crawler.get_sample_questions(tags=tags, is_answered=True)
        clean_questions = [
            {
                "title": raw_question.get("title", None),
                "link": raw_question.get("link", None),
                "question_id": raw_question.get("question_id", None),
                "accepted_answer_id": raw_question.get("accepted_answer_id", None),
            }
            for raw_question in raw_questions
        ]

        return clean_questions

    def collect_answers(self, clean_questions):
        complete_data = []
        for question_data in clean_questions:
            data = question_data.copy()
            if question_data["accepted_answer_id"] is not None:
                raw_answer_data = self.crawler.get_answer_by_id(id=question_data["accepted_answer_id"])
                data.update({
                    "answer_body": raw_answer_data["items"][0]["body"]
                })

            complete_data.append(data)

