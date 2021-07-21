# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students


### Endpoints


#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None.  NO request JSON required for GET requests.
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```


#### GET '/questions?page=${page}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer.  NO request JSON required for GET requests.  NOTE: The '?page=' parameter is optional.  If not provided, it returns the first 10 questions from the query results.
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category 

```
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
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
   
  ], 
  "total_questions": 21
}    
```


#### GET '/categories/${category id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: category_id - integer.  NO request JSON required for GET requests.
- Returns: An object with questions for the specified category, total questions, and current category string 

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```


#### POST '/questions' 
- Sends a post request in order to add a new question - requires a request json object.
- Request Arguments:  None.  But this POST request requires a request JSON containing details of the new question to be added 
```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- Returns:  
a. If request passes, it returns "success" status of True.
```
{
    "success": True
}
```

b. If request fails, it returns "success" status of False and HTTP Error Code returned with a corresponding error message
```
{
    "error": <HTTP Error Code>,
    "message": "<error message>",
    "success": False
    "
}
```

#### POST '/questions'
- Same API route as posting new questions, but this one sends a post request to search for a specific question by search term.
- Request argument:  None, but this POST request requires a JSON BODY containing the word or phrase to be searched
```
{
    'searchTerm': 'discovered'
}
```
- Returns: 
a. If one or more questions meet the search criteria, a list of 'questions' is provided along with 'total_questions' showing the number of questions retrieved - note that 'current_category' always returns "null".
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'null'
}
```

b. If no search criteria found, question array is empty and 'total_questions' return 0. Note that "current_category" always returns 'null'.
```
{
  "current_category": null, 
  "questions": [], 
  "total_questions": 0
}
```


#### POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Arguments:  None; this POST requests requires a list of question ids for 'previous_questions' and quiz_category as follows:

a.  to play quizzes for questions for a PARTICULAR category - 'previous_questions' may contain an empty list:
```
{ 
    "previous_questions" :[2, 16,21], 
    "quiz_category":{"id":1, "type": "Science"}}
```

b.  to play quizzes for questions for ALL categories, the quiz_category needs to contain only {"id":0 } - id of 0 indicates ALL categories - and 'previous_questions' may contain an empty list:
```
{ 
    "previous_questions" :[], 
    "quiz_category":{"id":0}}
```

- Returns: a single new question object 
```
{
    "question": {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
}
```


#### DELETE '/questions/${id}'
- Deletes a specified question using the id of the question. NO REQUEST JSON REQUIRED.
- Request Arguments: id - integer.  No request JSON required for DELETE requests.
- Returns: 

a. if successful delete,  only the "success" status is returned
```
{
    "success": True
}
```

b. If request fails, it returns "success" status of False and HTTP Error Code returned with a corresponding error message
```
{
    "error": <HTTP Error Code>,
    "message": "<error message>",
    "success": False
    "
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
