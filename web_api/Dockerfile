FROM python:3.10-slim
WORKDIR /app
COPY . /app/web_api


RUN pip install -U "huggingface_hub[cli]" transformers
RUN huggingface-cli login --token $HF_TOKEN
RUN pip install --no-cache-dir --upgrade -r /app/web_api/requirements.txt
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

CMD ["uvicorn", "web_api.main:app",  "--host", "0.0.0.0", "--port", "8000", "--reload" ]