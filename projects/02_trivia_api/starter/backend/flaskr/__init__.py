import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

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
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        
        if not categories:
            abort(404)
        
        return jsonify({
            "success": True,
            # "categories":results}
            'categories': {category.id:category.type for category in categories}
        })


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
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by("id").all()

        return jsonify(json_response(current_questions, len(Question.query.all()), None, categories))

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):

        question = Question.query.get(q_id)

        if question is None:
            abort(404)
        
        try:
            question.delete()

            return jsonify({
                "success": True
            })
        
        except:
            abort(422)


    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  

    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include questions
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions', methods=['POST'])
    def search_or_post_question():
        body =  request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        search_term = body.get('searchTerm', None)

        if search_term:
            results = Question.query.filter(Question.question.ilike("%{}%".format(search_term))).\
                                order_by("id").all()
            questions = [question.format() for question in results]
            return jsonify(json_response(questions, len(results), None))
        else:
            # ensure all fields are NOT EMPTY (for strings) and NOT ZERO (for numeric fields)
            if question.strip()  and answer.strip()  and difficulty  and category:
                question = Question(question=question,answer=answer,difficulty=difficulty,category=category)
            else:
                abort(422)   # not processable if any of the fields are null
            try: 

                question.insert()
                return jsonify({
                    "success": True
                })
                
            except:
                abort(422)


    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:cat_id>/questions')
    def get_category_questions(cat_id):
        
        results = Question.query.filter(Question.category==cat_id).order_by(Question.id).all()      
        questions = [question.format() for question in results]
        return jsonify(json_response(questions, len(results),cat_id))

    # json_response function
    def json_response(results, len_results, cat_id=None, categories=None):

        if cat_id:
            type = db.session.query(Category.type).filter(Category.id==cat_id).one()[0]
        else:
            type = None

        if categories:
            return {
                'questions': results,
                'total_questions': len_results,
                'current_category': type,
                'categories': {category.id:category.type for category in categories}
            }
            
        else:
            return {
                'questions': results,
                'total_questions': len_results,
                'current_category': type
            }



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
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        body =  request.get_json()

        # prev_quesions is a LIST of question ids  - if none is provided in the json, just assign an empty list   
        prev_questions = body.get('previous_questions', [])
        # quiz_category contains the dictionary entry of id and type of the selected category - if none is provided, assign Vvalue of 0
        quiz_category = body.get('quiz_category',0)

        # get all questions but include only questions not in prev_questions
        if quiz_category['id'] == 0:  # ALL categories
            test_questions = [q for q in  Question.query.filter(Question.id.notin_(prev_questions)).\
                                                    order_by(Question.id).all()]

        else:
            # filter questions by quiz_category.id AND include only questions not in prev_questions
            test_questions  = [q for q in  Question.query.filter(Question.category==quiz_category["id"]).
                                                            filter(Question.id.notin_(prev_questions)).
                                                            order_by(Question.id).all()]

        
        
        question = random.choice(test_questions).format() if len(test_questions) else None

        return jsonify({
                "success": True,
                "question": question
        })


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
        "message": "resources not found"
        }), 404

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    return app
