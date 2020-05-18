
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import datetime
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.casting_assistant = os.getenv('CASTING_ASSISTANT')
        self.casting_director = os.getenv('CASTING_DIRECTOR')
        self.executive_producer = os.getenv('EXECUTIVE_PRODUCER')

        self.database_filename = "database.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))

        #self.database_name = "casting_test"
        #self.database_path = "postgres://{}:{}@{}/{}".format(
        #    'postgres', 'willa2018', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        self.new_actor = {
            'name': 'Nick Klenke',
            'gender': 'Male',
            'role': 'Programmer'
        }

        self.new_movie = {
            'title': 'New Movie',
            'release_date' : datetime.date(2020, 5, 18),
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db_drop_and_create_all()

    def tearDown(self):
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 200)
    
    def test_fetch_all_actors_casting_assistant_first(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    '''
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_get_paginated_questions_invalid_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_question(self):
        question = Question(
            question='test question',
            answer='test answer',
            difficulty=1,
            category=1)
        question.insert()
        question_id = question.id

        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        question = Question.query.filter(
            Question.id == question.id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)

    def test_404_delete_question_invalid_id(self):
        response = self.client().delete('/questions/zzzzz')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_question_new(self):
        new_question = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 1,
            'category': 1
        }

        total_questions_before = len(Question.query.all())
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_after, total_questions_before + 1)

    def test_422_post_question_new_missing_data(self):
        new_question = {
            'question': 'test question',
            'answer': 'test answer',
            'category': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    def test_post_question_search(self):
        search_data = {'searchTerm': 'a'}
        response = self.client().post('/questions', json=search_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_404_post_question_search(self):
        search_data = {'searchTerm': 'zzzzz'}
        response = self.client().post('/questions', json=search_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_get_questions_per_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_per_category(self):
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_get_quiz_questions(self):
        request_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 5}}
        response = self.client().post('/quizzes', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_get_quiz_questions(self):
        request_data = {'previous_questions': []}
        response = self.client().post('/quizzes', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")
    '''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()