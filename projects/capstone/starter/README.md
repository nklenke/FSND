# Casting Agency backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
This application uses a sqllite database that is created upon startup.  No setup is necessary.

## Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.y
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to run the application. 

### Get tokens and update in tests
1. Open the following link in a browser: https://nkcoffee.auth0.com/authorize?audience=actorsAndMovies&response_type=token&client_id=zpizdFNFV6UnzgsReSwZwPM1UzVM3QT3&redirect_uri=http://localhost:8100
2. 3 Users have been created with their respective roles.  Each uses the password p@$$w0rd
  a. Casting Assistant
    - Email Address: udacityFSNDCapstoneCastingAssistant@yahoo.com
    - Can view actors and movies
  b. Casting Director
    - Email Address: udacityfsndcapstonecastingdirector@yahoo.com
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
  c. Executive Producer
    - Email Address: udacityFSNDCapstoneExecutiveProducer@yahoo.com
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database
3. Once logged in, get the token parameter from the callback url
4. To run unit tests, update the token for each role in test_app.py
5. To test endpoints with [Postman](https://getpostman.com). 
    - Import the postman collection `./UdacityFSNDCapstone.postman_collection.json`
    - Navigate to the authorization tab and update the token for the respective user noted in the test name.

## Endpoints 
### GET /actors
- Returns a list of actor objects and success value
- Sample Response:
```
[
    {
        "age": 41,
        "gender": "male",
        "id": 1,
        "name": "Nick Klenke"
    },
    {
        "age": 38,
        "gender": "female",
        "id": 2,
        "name": "Jamie Klenke"
    }
]
```

### POST /actors
- Creates a new actor using the submitted name, age and gender. Returns the new actor object and success value.
- Sample Request:
```
{
    "name": "Jamie Klenke",
    "age": 38,
    "gender": "female"
}

```
- Sample Response:
```
{
    "new_actor": {
        "age": 38,
        "gender": "female",
        "id": 2,
        "name": "Jamie Klenke"
    },
    "success": true
}

```

### PATCH /actors/{actor_id}
- Updates the actor with the given id, using the submitted name, age, and/or gender. Returns the updated actor object and success value.
- Sample Request:
```
{
    "age": 39
}
```
- Sample Response:
```
{
    "actor": [
        {
            "age": 39,
            "gender": "female",
            "id": 2,
            "name": "Jamie Klenke"
        }
    ],
    "success": true
}
```

### DELETE /actors/{actor_id}
- Deletes the actor of the given ID if it exists.  Returns the id of the deleted actor and success value
- Sample Response:
```
{
  "deleted": 2,
  "success": true
}
```

### GET /movies
- Returns a list of movie objects and success value
- Sample Response:
```
[
    {
        "genre": "Comedy",
        "id": 1,
        "title": "Stepbrothers"
    },
    {
        "genre": "Action",
        "id": 2,
        "title": "Die Hard"
    }
]
```

### POST /movies
- Creates a new movie using the submitted title and genre. Returns the new movie object and success value.
- Sample Request:
```
{
    "title": "Die Hard",
    "genre": "Action"
}

```
- Sample Response:
```
{
    "new_movie": {
        "genre": "Action",
        "id": 2,
        "title": "Die Hard"
    },
    "success": true
}

```

### PATCH /movies/{movie_id}
- Updates the movie with the given id, using the submitted title and/or genre. Returns the updated movie object and success value.
- Sample Request:
```
{
    "genre": "Action/Adventure"
}
```
- Sample Response:
```
{
    "movie": [
        {
            "genre": "Action/Adventure",
            "id": 2,
            "title": "Die Hard"
        }
    ],
    "success": true
}
```

### DELETE /movies/{movie_id}
- Deletes the movie of the given ID if it exists.  Returns the id of the deleted movie and success value
- Sample Response:
```
{
  "deleted": 2,
  "success": true
}


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```
The API will return these error types when requests fail:
- 400: Bad Request
- 401: Permission Not Found
- 404: Resource Not Found
- 422: Unprocessable 
- 500: Internal Server Error

## Testing
To run the tests, run
```
pytest test_app.py
```