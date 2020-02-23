import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
import json

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/api/categories', methods=["GET"])
    def all_categories():
        categories = list(map(Category.format, Category.query.order_by(Category.id.asc()).all()))
        data = {}
        for category in categories:
            data.update({
                category["id"]: category["type"]
            })
        result = {
            "success": True,
            "categories": data
        }
        return jsonify(result)

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/api/questions', methods=['GET'])
    def all_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = list(map(Question.format, Question.query.all()))
        total_questions = len(questions)
        questions = questions[start:end]

        categories = all_categories().get_json()["categories"]

        result = {
            "success": True,
            "questions": questions,
            "total_questions": total_questions,
            "current_category": None,
            "categories": categories
        }
        return jsonify(result)

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error = False
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404)
            question.delete()
        except Exception:
            error = True
            db.session.rollback()
            print(exc.info())
        finally:
            db.session.close()
            if error:
                abort(500)
            else:
                result = {
                    "success": True,
                    "deleted_question": question_id
                }
                print(result)
                return jsonify(result)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/api/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        # POST for searching questions
        if "searchTerm" in data:
            questions = Question.query.filter(
                func.lower(Question.question).like('%{}%'.format(data["searchTerm"].lower()))
            ).all()
            formatted_questions = list(map(Question.format, questions))
            result = {
                "questions": formatted_questions,
                "total_questions": len(formatted_questions),
                "current_category": None
            }
            return jsonify(result)
        # POST for adding new questions
        else:
            if not (data["question"] and data["answer"] and data["category"] and data["difficulty"]):
                abort(422)

            error = False
            try:
                question = Question(
                    question=data["question"],
                    answer=data["answer"],
                    category=data["category"],
                    difficulty=data["difficulty"]
                )
                question.insert()
            except Exception:
                error = True
                db.session.rollback()
                print(exc.info())
            finally:
                db.session.close()
                if error:
                    abort(500)
                else:
                    result = {
                        "success": True
                    }
                    return jsonify(result)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        questions = list(map(Question.format, Question.query.
                             filter_by(category=category_id).all()))

        category = Category.query.get(category_id)
        if not category:
            abort(404)

        result = {
            "questions": questions,
            "total_questions": len(questions),
            "current_category": category_id
        }
        return jsonify(result)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/api/quizzes', methods=["POST"])
    def quiz():
        data = request.get_json()
        prev_qs = list(data["previous_questions"])
        quiz_category = int(data["quiz_category"]["id"])

        if quiz_category:

            if not Category.query.get(quiz_category):
                abort(404)
            get_questions = Question.query.filter(
                Question.category == quiz_category,
                Question.id.notin_(prev_qs)).all()
        else:
            get_questions = Question.query.filter(
                Question.id.notin_(prev_qs)).all()

        if len(get_questions) == 0:
            return jsonify(None)
        else:
            questions = list(map(Question.format, get_questions))
            question = random.choice(questions)
            return jsonify(question)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found."
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "We couldn't process your request."
        }), 422

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Something went wrong."
        }), 500

    return app
