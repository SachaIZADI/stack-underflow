from stack_under_flow.crawler import StackOverflowCrawler, StackOverflowDataCollector

class TestStackOverflowCrawlers:

    def test_get_question_by_id(self):
        s = StackOverflowCrawler()
        res = s.get_questions_by_id(id=31323499)
        assert res[0]["is_answered"] is True

    def test_get_answer_by_id(self):
        s = StackOverflowCrawler()
        res = s.get_answer_by_id(id=31323566)
        assert res[0]["body"].startswith("<p>This might happen inside scikit, and it depends on what you're doing.")

    def test_get_sample_questions(self):
        s = StackOverflowCrawler()
        res = s.get_sample_questions(tags=["python", "java"])
        assert len(res) > 0


    # TODO: StackOverflowDataCollector
    """
    s= StackOverflowDataCollector()
    q = s.collect_sample_questions(tags=["python"])
    a = s.collect_answers(clean_questions=q)
    """

