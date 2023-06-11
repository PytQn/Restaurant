FROM python:3.10-slim

WORKDIR /restaurant

RUN pip install Flask Flask-SQLAlchemy flask-login psycopg2-binary

COPY . .

CMD python server.py