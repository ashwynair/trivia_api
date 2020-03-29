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
            'localhost:5432',
            self.database_name
        )
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

    def test_get_questions(self):
        """Test for retrieving questions"""
        res = self.client().get('/api/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data)

    def test_get_categories(self):
        """Test for retrieving categories"""
        res = self.client().get('/api/categories')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data)

    def test_500_delete_nonexistent_question(self):
        """Test for deleting nonexistent question"""
        res = self.client().delete('/api/questions/5000')
        self.assertEqual(res.status_code, 500)
        data = json.loads(res.data)
        self.assertFalse(data["success"])

    def test_questions_with_search(self):
        """Test for retrieving questions with search term"""
        res = self.client().post('/api/questions', json={"searchTerm": "a"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_add_new_question_success(self):
        """Test for adding questions"""
        res = self.client().post('/api/questions', json={
            "question": "This is a question",
            "answer": "This is the answer",
            "category": 1,
            "difficulty": 2
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])

    def test_422_add_new_question(self):
        """Test for adding question without answer"""
        res = self.client().post('/api/questions', json={
            "question": "This is a question",
            "category": 1,
            "difficulty": 2
        })
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)
        self.assertFalse(data["success"])

    def test_get_questions_by_category(self):
        """Test for adding question without answer"""
        res = self.client().get('/api/categories/1/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_404_get_question_by_category(self):
        """Test for adding question without answer"""
        res = self.client().get('/api/categories/101/questions')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertFalse(data["success"])

    def test_quiz_questions(self):
        """Test for adding question without answer"""
        res = self.client().post('/api/quizzes', json={
            "previous_questions": [],
            "quiz_category": {
                "id": 1
            }
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
