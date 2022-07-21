# API Development and Documentation Final Project

# Trivia App

This project is a virtual trivia game for Udacity employees and students. It is aimed at creating bonding experiences for employees and students. Team members can play the trivia game on a regular basis. Team menbers are able to add questions, play the quiz game, view the questions and by categories, and search through questions lists.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. 

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

The [backend](./backend/README.md) directory contains a detailed instructions on how to set up and run the project with Flask and SQLAlchemy server. 

> View the [Backend README](./backend/README.md) for more details.

From the backend folder run `pip install -r requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. 

> View the [Frontend README](./frontend/README.md) for more details.

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": "400",
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- `400`: Bad Request
- `404`: Resource Not Found
- `422`: Not Processable 

### Endpoints 

`GET '/categories'`
- General:

    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

    - Request Arguments: None

    - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

    - Sample: `curl http://127.0.0.1:5000/categories`


```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

`GET '/questions?page=${integer}'`
- General:

    - Fetches a paginated set of questions, a total number of questions, all categories and current category string.

    - Request Arguments: `page` - integer

    - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

    - Sample: `curl http://127.0.0.1:5000/questions?page=1`

```json
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
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```

`DELETE '/questions/${id}'`
- General:

    - Deletes a specified question using the id of the question

    - Request Arguments: `id` - integer

    - Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question.

    - Sample: `curl -X DELETE http://127.0.0.1:5000/questions/9`

```json
{
  "deleted": 9,
  "success": true
}
```
`POST '/questions'`
- General:

    - Sends a post request in order to search for a specific question by search term

    - Request Body:

    ```json
        {
            "searchTerm": "title"
        }
    ``` 
    - Returns: An object with questions for the specified search term, and total questions
    
    - Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "title"}`

    ```json
    {
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
  ],
    "success": true,
    "total_questions": 1
    }
    ```

`POST '/questions'`
- General:

    - Sends a post request in order to add a new question

    - Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
        "question": "Which continent is Nigeria located?",
        "answer": "Africa",
        "category": "Geography",
        " difficulty" : 3}'`
    - Returns: Does not return any new data

    - Request Body:
    ```json
        {
            "question": "Which continent is Nigeria located?",
            "answer": "Africa",
            "category": "Geography",
            "difficulty" : 3
        }
    ```

`GET '/categories/${id}/questions'`
- General:

    - Fetches questions for a cateogry specified by id request argument

    - Request Arguments: `id` - integer

    - Returns: An object with questions for the specified category, total questions, and current category string

    - Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```json

  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "A Human",
      "category": 1,
      "difficulty": 4,
      "id": 48,
      "question": "What are you?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

`POST '/quizzes'`

- General

    - Sends a post request in order to get the next question
    - Request Body:

    ```json
    {
        "previous_questions": [5, 9, 12],
        "quiz_category": {"type": "Science", "id": "1"}
    }
    ```
    - Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
        "previous_questions": [5, 9, 12],
        "quiz_category": {"type": "Science", "id": "1"}
    }'`

    - Returns: a single new question object

    ```json
    {
    "question": {
        "answer": "A Human",
        "category": 1,
        "difficulty": 4,
        "id": 48,
        "question": "What are you?"
    },
    "success": true
    }
    ```

## Deployment N/A

## Authors
Uchenna Egbo [YuhCee](https://github.com/yuhcee)

## Acknowledgements 
The awesome team at Udacity and all of the extraordinary tutors, session leads, students and instructors. 

