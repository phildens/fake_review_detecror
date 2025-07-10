FROM python:3.10-slim
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


CMD ["python3", "src/server.py" ]