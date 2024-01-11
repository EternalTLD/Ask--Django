.PHONY: run mm

run:
	python manage.py runserver

mm:
	python manage.py makemigrations
	python manage.py migrate
uvrun:
	python -m uvicorn ask_project.asgi:application
