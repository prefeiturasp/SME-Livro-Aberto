FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

# Criando o diretório e copiando o conteúdo
RUN mkdir -p /opt/services/livro-aberto/src
COPY . /opt/services/livro-aberto/src

# Configurando o arquivo .env
WORKDIR /opt/services/livro-aberto/src

RUN pip install pipenv && pipenv install

EXPOSE 8000

