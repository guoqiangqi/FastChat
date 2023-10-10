FROM python:3.9
WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt && \
    pyinstaller --onefile fastchat/serve/openai_api_server.py

FROM alpine:3.18
WORKDIR /app
COPY --from=0 /app/dist/api_server /app

# Run controller
CMD ["api_server", "--host localhost", "--port 8000", "--add-chatgpt"]