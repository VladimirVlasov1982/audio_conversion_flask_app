FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y ffmpeg
COPY . ./

CMD python app.py
