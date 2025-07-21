FROM python:3.7

ENV PYTHONUNBUFFERED 1

# Creating dir and copying content
RUN mkdir -p /opt/services/livro-aberto/src
ADD . /opt/services/livro-aberto/src

# Configuring .env file
WORKDIR /opt/services/livro-aberto/src

RUN pip install pipenv && pipenv install

EXPOSE 8000
