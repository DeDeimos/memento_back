# app/Dockerfile

# pull official base image
FROM python:3.11.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# install libs for postgres
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev build-base linux-headers pcre-dev
# install dependencies
COPY ./requirements.txt .
RUN pip install uwsgi
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD [ "uwsgi", "--http", ":8000", "--wsgi-file", "./memento_back/wsgi.py"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]