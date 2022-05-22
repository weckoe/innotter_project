FROM python:3.8-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

#requirements for postgres
RUN apk update && apk upgrade && apk add postgresql-dev gcc python3-dev musl-dev

#requirements for pilllow
RUN apk add zlib-dev jpeg-dev gcc musl-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app/
WORKDIR /app/

