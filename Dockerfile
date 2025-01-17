FROM python

RUN apt-get update && apt-get upgrade -y
RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN python -m pip install -r requirement.txt
RUN python manage.py migrate