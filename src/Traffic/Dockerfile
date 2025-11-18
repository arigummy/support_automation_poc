FROM python:3.9-slim

RUN apt-get update || true && rm -fr /var/lib/apt/lists/*

WORKDIR /app

COPY ./ /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "Transactions_generator.py" ]
