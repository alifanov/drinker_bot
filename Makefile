install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

shell:
	heroku run python manage.py shell

migrate:
	heroku run python manage.py migrate