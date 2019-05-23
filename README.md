### Installation
1. Install [pipenv](https://pypi.org/project/pipenv/)
2. Clone this repo and `cd issue-tracker-3635`
3. Run `pip install --user --upgrade pipenv` to get the latest pipenv version.
4. Run `pipenv --python 3.6`
5. Run `pipenv install`
6. Run `cp .env.example .env`
7. Update .env file `DATABASE_URL` with your `database_name`, `database_user`, `database_password` if needed.

### Running locally
1. Run `pipenv shell`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Run `python manage.py runserver`
