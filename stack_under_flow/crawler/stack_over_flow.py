import requests
from typing import List
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
from urllib.parse import urlparse, parse_qs


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

    def generate_api_key(
            self,
            path_to_chrome_driver: str = '/Users/sachaizadi/Documents/Projets/stack_under_flow/stack_under_flow/crawler/chromedriver'
    ):

        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        caps["goog:loggingPrefs"] = {"performance": "ALL"}

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(
            desired_capabilities=caps,
            executable_path=path_to_chrome_driver,
            chrome_options=chrome_options
        )
        driver.get("https://api.stackexchange.com/docs/answers-by-ids#order=desc&sort=activity&ids=31323566&site=stackoverflow&run=true")
        browser_logs = driver.get_log('performance')
        driver.quit()

        def extract_key(logs: dict) -> str:
            for log in logs:

                message = json.loads(log["message"])["message"]

                params = message.get("params")
                if params is None:
                    continue

                req = params.get("request")
                if req is None:
                    continue

                url = req.get("url")
                if url is None:
                    continue

                if url.startswith("https://api.stackexchange.com/2.2/sites?") and "key=" in url:
                    parsed = urlparse(url)
                    key = parse_qs(parsed.query).get('key')
                    if key is not None:
                        return key[0]

            return None

        new_api_key = extract_key(logs=browser_logs)

        if new_api_key is not None:
            self.api_key = new_api_key


    def search_question_by_tag(self, tag: str) -> List[dict]:
        search_url = f"https://api.stackexchange.com/2.2/search?order=desc&sort=votes&tagged={tag}&site=stackoverflow&filter=!9Z(-wwYGT"
        res = requests.get(search_url, params={"key": self.api_key})
        res_json = res.json()
        self.quota = self.get_quota(res_json)
        return res_json["items"]

    def get_questions_by_id(self, id: int) -> dict:
        question_url = f"https://api.stackexchange.com/2.2/questions/{id}?order=desc&sort=activity&site=stackoverflow&filter=!9Z(-wwYGT"
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


class StackOverflowDataCollector:

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.crawler = StackOverflowCrawler(api_key=api_key)

    def collect_sample_questions(self, tags: list):
        raw_questions = self.crawler.get_sample_questions(tags=tags, is_answered=True)
        clean_questions = [
            {
                "title": raw_question.get("title", None),
                "question_body": raw_question.get("body", None),
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
                    "answer_body": raw_answer_data[0]["body"]
                })

            complete_data.append(data)
        return complete_data

    @staticmethod
    def save_data(data: List[dict], dst_file: str):

        if not dst_file.endswith(".json"):
            raise NotImplementedError("Only JSON output format is currently supported")

        with open(dst_file, 'w') as f:
            json.dump(data, f)

        print(f"Data was saved to {dst_file}")
