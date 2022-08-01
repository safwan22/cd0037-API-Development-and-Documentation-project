import os
from logging import exception
from tkinter.messagebox import QUESTION
from json import load
from unicodedata import category
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
# 
@app.route('/foo', methods=['GET'])
def response():
     response = Flask.jsonify({'app': 'resources'})
     response.headers.add('Access-Control-Allow-Origin', '*')
     return response
  # cors to allow all origin

@app.route()
def add_cors_headers(response):
        r = request.referrer[:-1]
        if r in response:
         response.headers.add('Access-Control-Allow-Origin', r)
        response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        return response   

    # endpoint to get all available categories
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
# paginate questions
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


 # endpoint to handle GET requests for questions,
 #including pagination (every 10 questions).
@app.route('/questions')
def retrieve_questions(self):
    try:
        question=question.query().all()
        selection = question.query(question.question_id == self.id)\
      .group_by(Category.id) \
      .order_by(Category.category_id) \
      .all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
        if len(current_questions) == 0:
          abort(404)
        else:
         return jsonify({
                          'success': True,
                          'questions': current_questions,
                          'total_questions': len(selection),
                          'categories': [category.type for category in categories],
                          'current_category': None
      
                        })
    except Exception:
            abort(422)

 # endpoint to delete question using Id
@app.route('/delete_questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):  
    try:
          question = Question.query.get(question_id)
          if not question:
             abort(404)
           
          question.delete()
          return jsonify({
          'success': True,
           'deleted': question_id
    })

    except Exception:
            abort(422)
        
 #POST a new question,
 #which will require the question and answer text,
 # category, and difficulty score.      


@app.route("/questions", methods=["POST"])
def create_question(self):
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None) 
        search = body.get("search", None)
        try:
            if search:
                selection = question.query.order_by(question.id).filter(
                    question.question.ilike("%{}%".format(search))
                )
        
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                    }
                )
            else:
                question = question(question=new_question, answerr=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = question.query(question.question_id == self.id)\
                          .group_by(Category.id) \
                          .order_by(Category.category_id) \
                          .all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "books": current_questions,
                        "total_questions": len(question.query.all()),
                    }
                )

        except:
            abort(422)               
    #endpoint to get questions based on a search term.            
@app.route('/search', methods=['POST'])
def search_question(search_term):
      
            body = request.get_json()
            search = body.get('searchTerm', None)
            
            if not search_term:
                  abort(404)

            search_results = Question.query.filter(
              Question.question.ilike(f'%{search_term}%')
             ).all()
            return jsonify({
                              'success': True,
                              'questions': [question.format() for question in search_results],
                              'total_questions': len(search_results),
                              'current_category': None
    
                            })
# enpoint to get question using category_Id
@app.route('/categories/<int:category_id>', methods=['GET'])
def retrieve_questions_by_category(category_id):  
    
    try:
          selection = Question.query.get(question.category==category_id).all()
          current_questions = paginate_questions(request, selection)
          categories = Category.query.all()

          if category_id > len(categories):
                abort(404)
        
          return jsonify({
                          'success': True,
                          'question':list(current_questions),
                          'total_questions':len(selection),
                          'current_category':(category.type for category in categories if category.id == category_id)
                        })
    except Exception:
            abort(422)  
            #play trivia quizes endpoint
@app.route('/quizzes', methods=['POST'])
def play_trivia_quizes():
        try:

             body = request.get_json()

             if  ('quiz_category' in body or 'previous_questions' in body) is None:
                abort(422)

             category = body.get('quiz_category')
             previous_questions = body.get('previous_questions')

             if category ['id'] is None:
                available_questions = (Question.query.filter).all()
             else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(previous_questions).all()
            
       
             new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None
 
             return jsonify({
                'success': True,
                'question': new_question
            })
        except:
               abort(422)





  #error handlers
@app.errorhandler(404)
def not_found(error):
        return( 
            jsonify({'success': False, 'error': 404,'message': 'Not found'}),
            404
        )
    
@app.errorhandler(422)
def unprocessed(error):
        return(
            jsonify({'success': False, 'error': 422,'message': 'request cannot be completed'}),
            422

        )

@app.errorhandler(400)
def bad_request(error):
        return(
            jsonify({'success': False, 'error': 400,'message': 'bad request'}),
            400

        )

@app.errorhandler(405)
def not_allowed(error):
        return(
            jsonify({'success': False, 'error': 405,'message': 'Not alllowed'}),
            405

        )
        return app
  