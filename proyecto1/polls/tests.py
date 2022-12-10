import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        future_questions = Question(question_text="¿Cual es el pais que más estudia en Platzi?", pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertIs(future_questions.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        past_questions = Question(question_text="¿Cual es el pais que más estudia en Platzi?", pub_date=timezone.now() - datetime.timedelta(days=1))
        self.assertIs(past_questions.was_published_past(), False)

    def test_was_published_recently_with_actual_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        actual_questions = Question(question_text="¿Cual es el pais que más estudia en Platzi?", pub_date=timezone.now())
        self.assertIs(actual_questions.was_published_actual(), True)

def create_question(question_text, days):
    """
    Create a Question with the given "question_text" and published the given number of days offset to now (Negative for questions published in the past, positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTets(TestCase):

    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_questions(self):
        """
        Question with a pub_date in the future aren't displayed on the index page
        """
        create_question("Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_past_questions(self):
        """
        Question with a pub_date in the past are displayed on the index page
        """
        question = create_question("Past Question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
        self.assertQuerysetEqual

    def test_future_and_past_questions(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )


    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        past_question_1 = create_question(question_text="Past question 1", days=-30)
        past_question_2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question_1, past_question_2]
        )

    def test_two_future_questions(self):
        """
        The questions index page don't display multiple questions in the future
        """
        future_question_1 = create_question(question_text="Future question 1", days=30)
        future_question_2 = create_question(question_text="Future question 2", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )

class QuestionDetailViewTests(TestCase):
    
    def test_future_questions(self):
        """The detail of a question with a pub date in the future returns a 404 error not found
        """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:details", args=(future_question.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_questions(self):
        """The detail of a question with a pub date in the past displays the question's text
        """
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:details", args=(past_question.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

class QuestionAnswersViewChoices(TestCase):

    def test_choices_for_questions(self):
        question = create_question(question_text="Past question", days=-30)
        with self.assertRaises(Exception):
            question.save 