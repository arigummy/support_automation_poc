FROM python:3.9-slim

RUN apt-get updata &&b apt-get install -y --no-install-recomended \
    && rm -fr /var/lib/apt/lists/*

WORKDIR /API

COPY ../../API/ /API

RUN pip3 install --no-cahe-dir -r requirements.txt
