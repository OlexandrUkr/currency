
# manage_py := python app/manage.py
manage_py := docker compose exec -it backend python app/manage.py

run:
	$(manage_py) runserver

migrate:
	$(manage_py) migrate

makemigrations:
	$(manage_py) makemigrations

createsuperuser:
	$(manage_py) createsuperuser

shell:
	$(manage_py) shell_plus --print-sql

collectstatic:
	$(manage_py) collectstatic --no-input && \
	docker cp backend:/tmp/static /tmp/static && \
	docker cp /tmp/static nginx:/etc/nginx/static

worker:  # cd app && celery -A settings worker -l info --autoscale=0,10
	cd app && celery -A settings worker -l info -c 4 --pool threads

beat:
	cd app && celery -A settings beat -l info

pytest:
    docker compose exec -it backend pytest ./app/tests --cov=app --cov-report html && coverage report --fail-under=79.7754
# pytest ./app/tests --cov=app --cov-report html && coverage report --fail-under=70.00
