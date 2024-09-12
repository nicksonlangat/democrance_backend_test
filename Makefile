run:
	python manage.py runserver
migrate:
	python manage.py makemigrations && python manage.py migrate
test:
	export DJANGO_SETTINGS_MODULE=mysite.settings && pytest -vv
