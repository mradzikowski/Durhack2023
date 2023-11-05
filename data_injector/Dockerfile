FROM python:3.10.2-alpine

USER root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /usr/local/source

WORKDIR /usr/local/source

RUN pip3 install -r requirements.txt

CMD ["python","-u","app.py"]
