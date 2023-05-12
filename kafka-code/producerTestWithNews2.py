from time import sleep
from json import dumps
from kafka import KafkaProducer
import requests
from datetime import datetime

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

apiKey = {}
apiKey["NYT"] = "hOmmd1Qc0LlqsAQMS8GXQJdt5MKzH93G"

year = datetime.now().year
month = datetime.now().month

print("Starting Kafka producer for news data...")
while True:
        for key, value in apiKey.items():
                response = requests.get("https://api.nytimes.com/svc/archive/v1/" + str(year) + "/" + str(month) + ".json?api-key=" + value)
                if response.status_code == 200:
                        data = response.json()
                        producer.send('NYTNews', value=data)

        sleep(86400)
        # sleep for a day