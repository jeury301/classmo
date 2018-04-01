FROM python:latest

ENV PYTHONUNBUFFERED 1

ENV C_FORCE_ROOT true

RUN mkdir /static

WORKDIR /

ADD ./ /

RUN pip install -r requirements.txt


##ENV DJANGO_ENV=prod
##ENV DOCKER_CONTAINER=1

##EXPOSE 8200

##CMD ["uwsgi", "--ini", "/uwsgi.ini"]
##CMD ["uwsgi", "--check-static", "/static"]
##CMD python manage.py makemigrations schedules;python manage.py makemigrations discussions; python manage.py migrate; gunicorn classmo.wsgi -b 0.0.0.0:8000
##CMD python manage.py makemigrations; python manage.py migrate; gunicorn classmo.wsgi -b 0.0.0.0:8000
CMD ./initial_setup.sh; gunicorn classmo.wsgi -b 0.0.0.0:8000
