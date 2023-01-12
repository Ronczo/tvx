# Family budget
### Application to manage your family budget.

## Tech/Frameworks used
1. python 3.9
2. django
3. djangorestframework

## Requirements

1. docker
2. docker-compose
3. poetry

## Setting up dev environment

1. Create and fill `.env` file (use `.envtemplate` file to know which variables are needed)
2. Run `docker-compose up` in main directory
3. If everything is fine you should see your app on host `http://localhost:3000/` and the api on host 'http://127.0.0.1:8000/'
4. Install pre-commits `pre-commit install` (If you want to change something :) )

## Tests
1. To run tests make sure you entered the poetry shell.
2. go to directory `backend` (`cd backend/`)
3. type `pytest`
