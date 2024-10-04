FROM python:3.10-alpine

LABEL maintainer="sevca"

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

