FROM python:3.9.13-buster

EXPOSE 8000

COPY requirements.txt graphql_server.py ./

RUN pip install -r requirements.txt

CMD [ "strawberry", "server", "graphql_server"]