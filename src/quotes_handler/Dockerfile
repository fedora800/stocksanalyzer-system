FROM python:3.10-slim

ARG APP_VERSION

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV APP_VERSION=${APP_VERSION}

CMD ["python", "quotes_handler.py"]
