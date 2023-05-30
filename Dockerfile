FROM python:3.9.10

WORKDIR /project/code

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH /project/code/app

CMD gunicorn --workers 4 settings.wsgi --max-requests 10000 --log-level info --bind 0.0.0.0:8000
