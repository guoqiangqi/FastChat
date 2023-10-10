FROM nvidia/cuda:11.7.1-runtime-ubuntu20.04

WORKDIR /app
COPY . /app
RUN apt-get update -y && apt-get install -y python3.9 python3.9-distutils curl && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    echo \
   "accelerate>=0.21.0\n\
    peft==0.5.0\n\
    sentencepiece==0.1.99\n\
    torch\n\
    transformers>=4.31.0\n\
    protobuf==3.18.0" >> requirements.txt && \
    pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python3", "fastchat/serve/model_worker.py", "--model-path=lmsys/vicuna-7b-v1.5", "--controller=http://localhost:21001", "--worker=http://localhost:31000", "--port=31000"]
