FROM python

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN python -m pip install -r requirements.txt
RUN python manage.py makemigrations app
RUN python manage.py migrate
RUN python manage.py create_bank
RUN python manage.py runserver 0.0.0.0:5555
