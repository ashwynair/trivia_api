# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

*Note: Please ensure you have the postgres role available.*

```bash
createdb trivia
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks Completed

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Documentation
```

Note: All endpoints below will contain the "success": True key-value pair.

Endpoints
GET '/api/categories'
GET '/api/questions'
DELETE '/api/questions/<int:question_id>'
POST '/api/questions'
GET '/api/categories/<int:category_id>/questions'
POST '/api/quizzes'

GET '/api/categories'
- Fetches a dictionary of categories in which the keys are the ids 
and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a key called categories, that contains an object of id: category_string key:value pairs. 

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

GET '/api/questions'
- Fetches a dictionary containing an array of questions, the total no. of questions and categories
- Request Arguments: None
- Returns: JSON object with 5 keys: categories (same object as /api/categories), current_category (set to null), 
questions (array of objects for each question), success (set to true)
and total_questions (length of array of questions).

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
  ], 
  "success": true, 
  "total_questions": 1
}

DELETE '/api/questions/<int:question_id>'
- Deletes a user-specified question
- Request Arguments: question_id (ID of a question)
- Returns: JSON object with 2 keys: success (set to True), deleted_question (ID of question deleted)

{
  "success": True,
  "deleted_question": 2
}

POST '/api/questions'
- Either returns all questions based on searched term or adds a question
- Request Arguments: None
- Returns: 
  - If search: Returns questions based on search term
  - If adding question: Returns JSON object confirming question was added

GET '/api/categories/<int:category_id>/questions'
- Fetches a dictionary containing all questions based on the category selected
- Request Arguments: category_id (ID of category for question)
- Returns: questions, the category ID and number of questions

{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
  ], 
  "total_questions": 1
}

POST '/api/quizzes'
- POST method for quiz to return a random question not previously shown within the quiz
- Request Arguments: None
- Returns: 
  - If search: Returns questions based on search term
  - If adding question: Returns JSON object confirming question was added

{
  'id': 1,
  'question': "What is the heaviest organ in the human body?",
  'answer': "The Liver",
  'category': 1,
  'difficulty': 4
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```