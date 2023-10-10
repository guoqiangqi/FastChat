FROM python:3.9
WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt && \
    pyinstaller --off-line fastchat/serve/model_worker.py

FROM nvidia/cuda:11.7.1-runtime-ubuntu20.04

WORKDIR /app
COPY --from=0 /app/dist/openai_api_server /app

CMD ["model_worker", "--model-path /vicuna-7b-v1.5", "--controller http://localhost:21001", "--worker http://localhost:31000", "--port 31000"]