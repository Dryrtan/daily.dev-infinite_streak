FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium

COPY ./main.py .
COPY ./requirements.txt .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
