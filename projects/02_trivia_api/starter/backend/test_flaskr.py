import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from os import environ as env
from dotenv import load_dotenv


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.db_path = "postgres://{}:{}@{}/{}".format(env['DB_USER'], env['DB_PASSWORD'], env['DB_HOST'], env['TEST_DB_NAME'])
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.question_bad_data = {
            # bad data with question field containing spaces, this will be rejected
            "question" : " ",
            "answer" : "bad data",
            "difficulty" : 1,
            "category" : 0
        }

        self.question_good_data = {
            "question" : "Is this unit test data? ",
            "answer" : "Yes",
            "difficulty" : 1,
            "category" : 1
        }

        self.search_term_ok = {
            "searchTerm": "a"
        }

        self.search_term_return_empty = {
            "searchTerm": "1234567890"
        }

        self.quiz_category_specific =  {
            # passing a list of previous_questions and a specific quiz category
            "previous_questions" :[1, 2, 3],
            "quiz_category":{"id":5, "type":"Entertainment"}
        }

        self.quiz_category_all  =  {
            # passing a quiz category id of zero, which should get ALL questions from EVERY category
            "previous_questions" :[1, 2, 3],
            "quiz_category":{"id":0}
        }



    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginate_questions_pass(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertFalse(data['current_category'])

    def test_paginate_questions_failed_404(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resources not found')

    def test_get_categories_pass(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)

    def test_get_category_questions_pass(self):
        cat = Category.query.order_by(Category.id).first()
        res = self.client().get('/categories/{}/questions'.format(str(cat.id)))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], cat.type)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_search_question_OK_200(self):
        res = self.client().post('/questions', json=self.search_term_ok)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], None)

    def test_search_question_return_empty(self):
        res = self.client().post('/questions', json=self.search_term_return_empty)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data["questions"])
        self.assertFalse(data["total_questions"])
        self.assertEqual(data["current_category"], None)

    def test_create_question_good_data_200(self):
        res = self.client().post('/questions', json=self.question_good_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)

    def test_play_quiz_category_specific(self):

        res = self.client().post('/quizzes', json=self.quiz_category_specific)
        data = json.loads(res.data)
        category_id = self.quiz_category_specific["quiz_category"]["id"]

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["question"]), 1)
        self.assertEqual(data["question"]["category"], category_id)

    def test_play_quiz_category_all(self):

        res = self.client().post('/quizzes', json=self.quiz_category_all)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["question"]), 1)
        # assert that our input JSON is passing category id value of 0 (i.e., get "ALL" categories)
        self.assertEqual(self.quiz_category_all["quiz_category"]["id"], 0)
        # assert that the response JSON's question has a "category" value NOT EQUAL to category_id value in our input json 
        self.assertNotEqual(data["question"]["category"], self.quiz_category_all["quiz_category"]["id"])

    def test_create_question_bad_data_422(self):

        res = self.client().post('/questions', json=self.question_bad_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    # this delete function attempts to delete a different question in each attempt
    def test_delete_question_success_200(self):
        question = Question.query.order_by(Question.id.desc()).first()
        question_id_to_delete = question.id
        # res = self.client().delete('/questions/{}.format(str(question_id_to_delete))')
        res = self.client().delete('/questions/{}'.format(str(question_id_to_delete)))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)

    def test_delete_question_fail_404(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resources not found')

    def test_delete_question_fail_405(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"],False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()