FROM python:3.11-alpine
RUN apk update && \
    apk add --no-cache mariadb-connector-c-dev mariadb-dev gcc musl-dev && \
    pip install --no-cache-dir mysqlclient
WORKDIR /usr/app
COPY requirements.txt /usr/app/
RUN pip install --no-cache-dir -r /usr/app/requirements.txt
COPY . /usr/app/
RUN python manage.py makemigrations authapp
RUN python manage.py makemigrations confapp
RUN python manage.py makemigrations subscription
RUN python manage.py makemigrations 
RUN python manage.py migrate authapp
RUN python manage.py migrate confapp
RUN python manage.py migrate subscription
RUN python manage.py migrate
RUN python manage.py seed_main
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]