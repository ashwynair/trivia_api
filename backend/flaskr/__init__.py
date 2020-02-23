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

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/api/categories', methods=["GET"])
    def all_categories():
        """
        GET request for all available categories
        :return: JSON object with category_id: category_type key-value pairs
        """
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

    @app.route('/api/questions', methods=['GET'])
    def all_questions():
        """
        GET request for all questions
        :return: JSON object with all questions, total_questions and categories.
        """
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

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        DELETE method for a question
        :param question_id: ID of a question
        :return: ID of question if successfully deleted
        """
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

    @app.route('/api/questions', methods=['POST'])
    def add_question():
        """
        POST method to add a question, or search for questions
        :return:
        - If search: Returns questions based on search term
        - If adding question: Returns JSON object confirming
        question was added
        """
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

    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        """
        GET method for all questions within a user-specified category
        :param category_id: ID of category for question
        :return: questions, the category ID and number of questions
        """
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

    @app.route('/api/quizzes', methods=["POST"])
    def quiz():
        """
        POST method for quiz
        :return: JSON object for random question
        """
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
