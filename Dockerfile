FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . .

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]