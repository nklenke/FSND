import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Movie, Actor, db, db_drop_and_create_all
from auth import AuthError, requires_auth

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  db_drop_and_create_all()

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
      response.headers.add('Access-Control-Allow-Origin', '*')
      return response

  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(payload):
      actors = Actor.query.all()
      actors = [actor.to_dict() for actor in actors]
      return jsonify(actors)

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
      req = request.get_json()
      
      if req is None:
          abort(400)
      
      name = req['name']
      age = req['age']
      gender = req['gender']

      if name is None:
          abort(400)
      try:
          actor = Actor()
          actor.name = name
          actor.age = age
          actor.gender = gender
          
          print(actor)
          actor.insert()
          new_actor = actor.to_dict()

          return jsonify({
              'success': True,
              'new_actor': new_actor
          }), 200
      except Exception:
          abort(422)

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):
      actor = Actor.query.filter(Actor.id == id).one_or_none()

      if actor is None:
          abort(404)

      req = request.get_json()
      if req is None:
          abort(400)

      name = req.get('name')
      age = req.get('age')
      gender = req.get('gender')
    
      try:
          if name:
              actor.name = name

          if age:
              actor.age = age

          if gender:
              actor.gender = gender

          actor.update()

          updated_actor = [actor.to_dict()]

          return jsonify({
              'success': True,
              'actor': updated_actor
          }), 200

      except Exception:
          abort(422)

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
      actor = Actor.query.filter(Actor.id == id).one_or_none()

      if actor is None:
          abort(404)

      actor.delete()

      return jsonify({
          'success': True,
          'delete': id,
      }), 200

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
      movies = Movie.query.all()
      movies = [movie.to_dict() for movie in movies]
      return jsonify(movies)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
      req = request.get_json()

      if req is None:
          abort(400)
        
      title = req.get('title')
      genre = req.get('genre', None)

      if title is None:
          abort(400)
      try:
          movie = Movie(title=title, genre=genre)
          movie.insert()
          new_movie = movie.to_dict()

          return jsonify({
              'success': True,
              'new_movie': new_movie
          }), 200
      except Exception:
          abort(422)

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, id):
      movie = Movie.query.filter(Movie.id == id).one_or_none()

      if movie is None:
          abort(404)

      req = request.get_json()
      if req is None:
          abort(400)

      title = req.get('title')
      genre = req.get('genre')

      try:
          if title:
              movie.title = title

          if genre:
              movie.genre = genre

          movie.update()

          updated_movie = [movie.to_dict()]

          return jsonify({
              'success': True,
              'movie': updated_movie
          }), 200

      except Exception:
          abort(422)

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
      movie = Movie.query.filter(Movie.id == id).one_or_none()

      if movie is None:
          abort(404)

      movie.delete()

      return jsonify({
          'success': True,
          'delete': id
      }), 200

  # Error Handling
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)