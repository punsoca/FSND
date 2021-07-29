import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
app.debug = True
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    if drinks:
        drinks = [drink.short() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": drinks
        })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    drinks = Drink.query.all()
    if drinks:
        drinks = [drink.long() for drink in drinks]
        return jsonify({
            "status": 200,
            "success": True,
            "drinks": drinks
        })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth("post:drinks")
def post_drink(payload):
    
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title and recipe:   # only process if title AND recipe are populated
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)  # need to convert the dict to a STRING or it fails!
        )

        try:
            drink.insert()

            return jsonify({
                "status": 200,
                "drinks": drink.long()

            })

        except Exception as e:
            abort(422)

    else:
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Title and recipe are required"
        }), 422

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def patch_drink(payload,drink_id):

    drink = Drink.query.get(drink_id)

    if not drink:
        return jsonify({
            "success": False,
            "error": 404,
            "message": "drink id not found"
        }), 404

    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title and recipe:   # only process if title AND recipe are populated
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)  # need to convert the dict to a STRING or it fails!
        )

        try:
            drink.update()
            
            print('\n\nUpdate success\n\n')
            return jsonify({
                "status": 200,
                "drinks": drink.long()

            })

        except Exception as e:
            abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth("delete:drinks")
def delete_drink(payload,drink_id):
    drink = Drink.query.get(drink_id)

    if drink:
        try: 
            drink.delete()
        except:
            abort(422)  # not processable (could be database glitch, etc)
    
    else:
        abort(404)

    return jsonify({
        "success": True,
        "delete": drink_id

            })
# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Drink not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
