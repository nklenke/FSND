
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import datetime
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVMVTRlV0lscHNHMEZWc1VNR2JyUyJ9.eyJpc3MiOiJodHRwczovL25rY29mZmVlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWMyZDU3ODljMDdhMTBjZTdjNmYyODQiLCJhdWQiOiJhY3RvcnNBbmRNb3ZpZXMiLCJpYXQiOjE1ODk4MjcxODMsImV4cCI6MTU4OTkxMzU4MywiYXpwIjoienBpemRGTkZWNlVuemdzUmVTd1p3UE0xVXpWTTNRVDMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.eqgsR8jbfDxxbatEoaExJ7A1DtHtmOCkqsEJiPD1eWhPMhhewRykdtnTI2deaYAN9VwQfm-sTD86kwvBAYnLAj_4BKbTaMZyepcp3gh1l7Pu5JKYfJbzp4Jfk9LsXrDNkoBXecZmFgxw0iQnZMM4-7bB8HB26eOdJrtCmx8C49y7Vd0S3Rv7kdrVkzN3y2V4CUA_1F7A-7FZ1aPhDGtEEIFeUetjb7DZN_bs4Xwd0rb9dQTNs0jXk_T0ck8Lde_J8szjh-UNQO2DiFX_gmwwG0FzoUKn1jUFWDgHgZyyEWl2m23ZU4g6Hfq6BZv7egS02IjPogNxhD_pbadPyB7GPg'
        self.casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVMVTRlV0lscHNHMEZWc1VNR2JyUyJ9.eyJpc3MiOiJodHRwczovL25rY29mZmVlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWMyZDViODljMDdhMTBjZTdjNmY0OTkiLCJhdWQiOiJhY3RvcnNBbmRNb3ZpZXMiLCJpYXQiOjE1ODk4MjcyNTEsImV4cCI6MTU4OTkxMzY1MSwiYXpwIjoienBpemRGTkZWNlVuemdzUmVTd1p3UE0xVXpWTTNRVDMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.y2TM7cjZN2v3smUfxoyxOxF9sZ5mJuMRJsbX_VgqS32hiM92sBx3RCxI6JmGUg_BYF9KqDabPxgJ7KrBaXVfabn1aR8YZUt6nAQ_NAo-XpJmSB__N-QeQ6WwYIwHxyqe_RNswO4o2BDaexOELgafxXusd6O6u5t4WA_c2Kb4awkeChwGLj282rMKEFM9BJt8cSyftWyI_gQ57ETLmnPHWq7bVn7-L4pjdXUx1J4_wjfVmVeZZrUAPLOlkli4R8Q5WzQLROvkA8iyseY2wTgA9vW3EvhXGVPxhydq5a19wtBRSJD214JM497FvNFRNEbxShaa_ldPOjY0FRDiWhhe1g'
        self.executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVMVTRlV0lscHNHMEZWc1VNR2JyUyJ9.eyJpc3MiOiJodHRwczovL25rY29mZmVlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWMyZDVkZjZhMzA1NDBjZDk4NGE3N2EiLCJhdWQiOiJhY3RvcnNBbmRNb3ZpZXMiLCJpYXQiOjE1ODk4MjczMDAsImV4cCI6MTU4OTkxMzcwMCwiYXpwIjoienBpemRGTkZWNlVuemdzUmVTd1p3UE0xVXpWTTNRVDMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.hdsEQKfu12qHqNe6qHrShJc7AOuS416TGGWHLy7bGhM9HGcxeMv2eolpPMb6zTs-uia9LIMcjXtootBgg_DQ3_KL0_iem_5bGwjsPdRq5Gs8abl_UmJNjP7_fzgc9o3fu5JPmlz1eUVOfysnAm6zTrlkRNmBSiHaw_LvJPtAIk9l2TQYElkZ7rXx01M3YulNK_IfiJ113PM89a3k6D62hPaWP-dJL7Nja458-69byDzrNNc0CEmTwcKj774p9jW-VWNEf4E4P31qIf9iXaLcsHYeA6XpaZg7Ep0GgAiwXZJFZa7vi46uPS8CoWVRoIYqKvfkbziU38_K3Kq8FIipdg'

        self.database_filename = "database.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))

        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        self.new_actor = {
            'name': 'Nick Klenke',
            'age': 41,
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'New Movie',
            'genre': 'Comedy'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            db_drop_and_create_all()

    def tearDown(self):
        pass

    def test_get_actors_casting_assistant_success(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        self.assertEqual(res.status_code, 200)
        
    def test_get_actors_missing_authorization_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertEqual(res.status_code, 401)
    
    def test_post_actor_casting_assistant_not_authorized(self):
        total_actors_before = len(Actor.query.all())
        res = self.client().post('/actors', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)}, 
                                        json=self.new_actor)
        data = json.loads(res.data)
        total_actors_after = len(Actor.query.all())

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(total_actors_before, total_actors_after)

    def test_post_actor_casting_director_success(self):
        total_actors_before = len(Actor.query.all())
        res = self.client().post('/actors', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)}, 
                                        json=self.new_actor)
        data = json.loads(res.data)
        total_actors_after = len(Actor.query.all())

        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['new_actor'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(total_actors_after, total_actors_before + 1)
    
    def test_update_actor_casting_assistant_not_authorized(self):
        res = self.client().patch('/actors/1', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)}, 
                                        json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(res.status_code, 401)
    
    def test_update_actor_casting_director_success(self):
        actor = Actor()
        actor.name = 'Dwight Schrute'
        actor.age = 50
        actor.gender = 'Male'
        actor.insert()

        update_actor = {
            'age': 51
        }

        res = self.client().patch('/actors/' + str(actor.id), headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)}, 
                                        json=update_actor)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'][0]['age'], 51)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_casting_assistant_not_authorized(self):
        actor = Actor()
        actor.name = 'Dwight Schrute'
        actor.age = 50
        actor.gender = 'Male'
        actor.insert()
        
        res = self.client().delete('/actors/' + str(actor.id), headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(res.status_code, 401)
    
    def test_delete_actor_casting_director_success(self):
        total_actors_before = len(Actor.query.all())
        
        actor = Actor()
        actor.name = 'Dwight Schrute'
        actor.age = 50
        actor.gender = 'Male'
        actor.insert()

        total_actors_after = len(Actor.query.all())
        self.assertEqual(total_actors_after, total_actors_before + 1)

        res = self.client().delete('/actors/' + str(actor.id), headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)})
        data = json.loads(res.data)

        total_actors_after = len(Actor.query.all())

        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], actor.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(total_actors_after, total_actors_before)

    def test_get_movies_casting_assistant_success(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        self.assertEqual(res.status_code, 200)
        
    def test_get_movies_missing_authorization_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertEqual(res.status_code, 401)
    
    def test_post_movie_casting_director_not_authorized(self):
        total_movies_before = len(Movie.query.all())
        res = self.client().post('/movies', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)}, 
                                        json=self.new_movie)
        data = json.loads(res.data)
        total_movies_after = len(Movie.query.all())

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(total_movies_before, total_movies_after)

    def test_post_movie_executive_producer_success(self):
        total_movies_before = len(Movie.query.all())
        res = self.client().post('/movies', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)}, 
                                        json=self.new_movie)
        data = json.loads(res.data)
        total_movies_after = len(Movie.query.all())

        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['new_movie'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(total_movies_after, total_movies_before + 1)
    
    def test_update_movie_casting_assistant_not_authorized(self):
        res = self.client().patch('/movies/1', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)}, 
                                        json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(res.status_code, 401)
    
    def test_update_movie_executive_producer_success(self):
        movie = Movie()
        movie.title = 'Action Filled Movie'
        movie.genre = 'Action'
        movie.insert()

        update_movie = {
            'genre': 'Adventure'
        }

        res = self.client().patch('/movies/' + str(movie.id), headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)}, 
                                        json=update_movie)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'][0]['genre'], 'Adventure')
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_casting_director_not_authorized(self):
        movie = Movie()
        movie.title = 'Action Filled Movie'
        movie.genre = 'Action'
        movie.insert()
        
        res = self.client().delete('/movies/' + str(movie.id), headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(res.status_code, 401)
    
    def test_delete_movie_executive_producer_success(self):
        total_movies_before = len(Movie.query.all())
        
        movie = Movie()
        movie.title = 'Action Filled Movie'
        movie.genre = 'Action'
        movie.insert()

        total_movies_after = len(Movie.query.all())
        self.assertEqual(total_movies_after, total_movies_before + 1)

        res = self.client().delete('/movies/' + str(movie.id), headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)})
        data = json.loads(res.data)

        total_movies_after = len(Movie.query.all())

        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], movie.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(total_movies_after, total_movies_before)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()