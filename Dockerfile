FROM python:3.8-slim
ARG port

USER root
COPY . /604-cats-dogs-classifier
WORKDIR /604-cats-dogs-classifier

ENV PORT=$port

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install curl \
    && apt-get install libgomp1

RUN chgrp -R 0 /604-cats-dogs-classifier \
    && chmod -R g=u /604-cats-dogs-classifier \
    && pip install pip --upgrade \
    && pip install -r requirements.txt
EXPOSE $PORT

CMD gunicorn app:server --bind 0.0.0.0:$PORT --preload
