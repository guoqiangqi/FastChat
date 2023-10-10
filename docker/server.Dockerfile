FROM python:3.9
WORKDIR /app
COPY . /app

RUN echo \
    "openai==0.28.0\n\
    google-cloud-aiplatform \n\
    psycopg2 \n\
    anthropic==0.3.11" >> requirements.txt && \
    pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
# Run controller
CMD ["python3", "fastchat/serve/openai_api_server.py", "--host=127.0.0.1", "--port=8000", "--add-chatgpt"]