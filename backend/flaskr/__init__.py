import os
from pickle import APPEND
from sre_constants import CATEGORY
from urllib import response
from flask import Flask, request, abort, jsonify, app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
CATEGORY_ALL = 0

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)


    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    @app.route('/foo', methods=['GET'])
    def response():
     response = Flask.jsonify({'app': 'resources'})
     response.headers.add('Access-Control-Allow-Origin', '*')
    return response
  # cors to all all origin
@app.route()
def add_cors_headers(response):
        r = request.referrer[:-1]
        if r in response:
         response.headers.add('Access-Control-Allow-Origin', r)
         response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
         response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        return response   

    # endpoint to get categories
@app.route('/categories' , method=['GET'])
def retrieve_categories(self):
    try:
            categories = Category.query(Category.category_id == self.id)\
      .group_by(Category.id) \
      .order_by(Category.category_id) \
      .all()
            return jsonify({
              'success': True,
              'categories': {
                category.id: category.type for category in categories
              }
            })
    except Exception:
            abort(422)

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

 # GET QUESTIONS
@app.route('/questions')
def retrieve_questions(self):
    try:
      
        selection = question.query(question.question_id == self.id)\
      .group_by(Category.id) \
      .order_by(Category.category_id) \
      .all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
 
      return jsonify({
      'success': True,
      'questions': current_questions,{
      'total_questions': len(selection),
      'categories': [category.type for category in categories],
      'current_category': None
      }
    })
 except Exception:
         if len(current_questions) == 0:
        abort(404)
     
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """





    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

