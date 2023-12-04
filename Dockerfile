# FROM python:3.10-slim


# WORKDIR /usr/app

# ENV ENV production

# COPY requirements.txt /usr/app/

# RUN apt-get update && apt-get install -y libpq-dev build-essential

# RUN pip install -r requirements.txt


# EXPOSE 5000

# COPY /app /usr/app/

# CMD flask db upgrade && flask run --host=0.0.0.0 --port=5000


FROM python:3.11.6-bullseye
WORKDIR /code

COPY /app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /app /code/

CMD flask db upgrade && flask run --host=0.0.0.0 --port=5000
