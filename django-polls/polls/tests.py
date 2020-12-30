import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        published_recently() returns False for pub_date in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        published_recently() returns False for pub_date older than a day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        published_recently() returns True for pub_date within a day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.published_recently(), True)


def create_question(question_text, days):
    """
    helper to generate questions in the past and future
    """
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions, a suitable message is sent
        """
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "No Polls available")
        self.assertQuerysetEqual(res.context["latest_questions"], [])

    def test_past_questions(self):
        """
        past questions are displayed
        """
        create_question(question_text="Past question", days=-30)
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context["latest_questions"], ["<Question: Past question>"]
        )

    def test_future_questions(self):
        """
        future questions are not displayed
        """
        create_question(question_text="Future question", days=30)
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "No Polls available")
        self.assertQuerysetEqual(res.context["latest_questions"], [])

    def test_past_and_future_questions(self):
        """
        only past questions are displayed even if there are future questions as well
        """
        create_question(question_text="Future question", days=30)
        create_question(question_text="Past question", days=-30)
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context["latest_questions"], ["<Question: Past question>"]
        )

    def test_many_past_questions(self):
        """
        all past questions are displayed ordered by the latest date
        """
        create_question(question_text="Past question 1", days=-20)
        create_question(question_text="Past question 2", days=-30)
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context["latest_questions"],
            ["<Question: Past question 1>", "<Question: Past question 2>"],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_questions(self):
        """
        Future question should return 404
        """
        q = create_question(question_text="Future question", days=30)
        res = self.client.get(reverse("polls:detail", args=(q.id,)))
        self.assertEqual(res.status_code, 404)
        # self.assertQuerysetEqual(res.context["question"], [])

    def test_past_questions(self):
        """
        past question should be displayed
        """
        q = create_question(question_text="Past question", days=-30)
        res = self.client.get(reverse("polls:detail", args=(q.id,)))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, q.question_text)
