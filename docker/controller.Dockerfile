FROM python:3.9
WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt && \
    pyinstaller --off-line fastchat/serve/controller.py

FROM alpine:3.18
WORKDIR /app
COPY --from=0 /app/dist/controller /app

# Run controller
CMD ["controller"]