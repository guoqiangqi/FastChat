FROM python:3.9
WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
# Run controller, set host as 127.0.0.1 instead of localhost to avoid address bind error
CMD ["python3", "fastchat/serve/controller.py", "--host=127.0.0.1"]