import time
import datetime

import random
from faker import Faker
import uuid

import requests
import json

import logging

from requests.exceptions import Timeout

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Generator:

    def __init__(self, api_url, transactions_per_second=1):
        self.api_URL = api_url
        self.tps = transactions_per_second
        self.faker = Faker()
        self.session = requests.Session()

        # response = self.session.post(
        #     f"{self.api_URL}",
        #     json={"message": "Hello, world!"},
        # )

        logger.info(f"Generator has started. Sending to API:{api_url}")

    def generate_transaction(self):
        statuses = ['success', 'failed', 'pending']
        chances = [0.8, 0.05, 0.15]

        transaction = {
            'id': str(uuid.uuid4()),
            'amount': round(random.uniform(100.0, 10000.0), 2),
            'currency': random.choice(['USD', 'EUR', 'CNY', 'RUB']),
            'timestamp': datetime.datetime.now().isoformat(),
            'status': random.choices(statuses, weights=chances, k=1)[0],
            'sender': f"user_{format(random.randint(1000, 65535), '04X')}",
            'recipient': f"user_{format(random.randint(1000, 65535), '04X')}"
        }

        return transaction

    def send_transaction(self, data):

        try:
            response = self.session.post(
                f"{self.api_URL}/api/transactions",
                json=data,
                timeout=5,
                headers={"Content-type": "application/json"}
            )

            if response.status_code == 200:
                logger.info(f"Transaction {data['id']} has been sent successfuly")
                return True
            else:
                logger.warning(f"Transaction {data['id']} has been sent with fail. ERROR: {response.status_code}")
                return False

        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to server")
            return False
        except requests.exceptions.Timeout:
            logger.error("Timeout connectiong to server")
            return False
        except Exception as e:
            logger.errro(f"Other error: {str(e)}")
            return False


    def run(self, duration=5):
        start_time = time.time()
        while time.time() - start_time <= duration:
            phase_start_time = time.time()
            for x in range(self.tps):
                self.send_transaction(self.generate_transaction())
            delay_time = 1 - (time.time() - phase_start_time)
            time.sleep(delay_time)

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    model = Generator("http://localhost:8000", transactions_per_second=1)
    model.run()
    # x = model.generate_transaction()
    # model.send_transaction(x)
