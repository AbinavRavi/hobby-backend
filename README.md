# Local Environment setup

1. Use some virtual environment and activate it for python 3.11. I prefer using miniconda 

```
conda create -n <env_name> python=3.11
conda activate
```
2. Once the virtual environment is ready you can install poetry for package management

```
pip install poetry
```
3. To install dependencies 
```
poetry install
```
4. There is some styling and code linting done already using pre-commit hooks so I would suggest installing by doing
```
pre-commit install
```
5. Workflow to push any commit would then be
- git add <file>
- pre-commit (Does the formatting and linting checks) if fails add again and then perform pre-commit again
- git commit -m "commit message"
- git push

# Endpoints and functionality

There are three endpoints

1. http://localhost:8000/onboarding/check_user/{user_id} - This endpoint basically returns a json of with a flag of user_exists as either true or false if False returns list of filters along with the response (GET)
2. http://localhost:8000/onboarding/get_preferences/{user_id} - This endpoint will dump the preferences to the database please use the correct items from previous JSON in signals etc else we will get a 500 error (POST)
3. http://localhost:8000/dashboard/show_dashboard_data/{user_id}?page=1&per_page=25 - This endpoint will show the data for the dashboard for the user, the page and per_page variables have to be provided as query parameters so that items can be fetched accordingly, else the first page with 25 items will always be fetched. (GET)