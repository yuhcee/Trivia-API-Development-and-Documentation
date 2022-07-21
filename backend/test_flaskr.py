import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO: DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories_success(self):
        """Test get categories success"""

        category = Category.query.first()
        res = self.client().get("/categories")
        data = json.loads(res.data)
        expected_json = {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "success": True
        }

        self.assertEqual(data, expected_json)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertDictEqual(data, expected_json)
        self.assertIn(str(category.id), data["categories"])
        self.assertTrue(data["categories"]["1"], category.type)

    def test_get_categories_failure(self):
        """Test get categories failure"""

        Category.query.delete()
        res = self.client().get('/categories')
        error_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertNotEqual(error_data["success"], True)
        self.assertEqual(error_data["message"], "resource not found")

    def test_405_get_categories_error(self):
        """Test 405 get categories error"""

        res = self.client().post('/categories')
        error_data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(error_data["success"], True)
        self.assertEqual(error_data["message"], "method not allowed")

    def test_get_paginated_questions(self):
        """Test get paginated questions"""

        total_questions = Question.query.count()
        questions_per_page = 10
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertIn("questions", data)
        self.assertTrue(data["categories"])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("question", data["questions"][1])
        self.assertNotIn("questions", data["questions"][1])
        self.assertNotEqual(data["current_category"], True)
        self.assertEqual(len(data["questions"]), questions_per_page)
        self.assertGreaterEqual(data["total_questions"], total_questions)

    def test_404_get_questions_error_requesting_beyond_valid_page(self):
        """Test 404 get questions error requesting beyond valid page"""

        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question_by_id_success(self):
        """Test delete question by id"""

        test_question_id = Question.query.first().id

        res = self.client().delete(f'/questions/{test_question_id}')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], test_question_id)
        self.assertIsNone(Question.query.get(test_question_id))

    def test_422_if_question_to_delete_does_not_exist(self):
        """Test 422 if question to delete does not exist"""

        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable entity")

    def test_search_questions_with_results(self):
        """Test search_questions_with_results"""

        res = self.client().post("/questions", json={"searchTerm": "Nigeria"})
        data = json.loads(res.data)

        self.assertIn("questions", data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])

    def test_search_questions_without_results(self):
        """Test search_questions_without_results"""

        res = self.client().post(
            "/questions", json={"searchTerm": "unkwnonw1111111111"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_create_new_question_success(self):
        """Test create new question success"""

        new_question = {
            "question": "Which continent is Nigeria located?",
            "answer": "Africa",
            "category": 3,
            "difficulty": 3
        }
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(Question.query.filter_by(
            question="Which continent is Nigeria located?").count(), 1)

    def test_422_if_question_creation_fails(self):
        """Test if question creation fails"""

        bad_question = {
            "question": "Which continent is NigeSydneyria located?",
            "answer": "NoWhere",
            "category": "Geography",
            "difficulty": 3
        }
        res = self.client().post("/questions", json=bad_question)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 422)
        self.assertNotEqual(data['success'], True)
        self.assertTrue(data['message'], "unprocessable entity")
        self.assertNotEqual(Question.query.filter_by(
            question="Which continent is NigeSydneyria located?").count(), 1)

    def test_get_questions_by_category_success(self):
        """Test get questions by category success"""

        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        # print("Science Category =>>>>", data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'],
                         Question.query.filter_by(category=3).count())
        self.assertEqual(data['current_category'],
                         Category.query.get(3).type)

    def test_get_questions_by_category_failure(self):
        """Test get questions by category failure"""

        res = self.client().get('/categories/1000000000/questions')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_question_success(self):
        """Test get quiz questions success"""

        request = {
            "previous_questions": [50, 41, 32],
            "quiz_category": {"type": "Geography", "id": "3"}
        }
        res = self.client().post('/quizzes',
                                 json=request)

        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(data), 2)
        self.assertIn("answer", data["question"])
        self.assertTrue(data['question']['id'])

    def test_get_quiz_question_failure(self):
        """Test get quiz questions failure"""

        res = self.client().post(
            '/quizzes', json={'previous_questions': "quiz_category"})
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
