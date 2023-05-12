from time import sleep
from json import dumps
from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
apiKey = {}

file = open('apiKeys.txt', 'r')
while True:
        s = file.readline()
        if not s:
                break
        s = s.strip('\n')
        keyValuePair = s.split(',')
        apiKey[keyValuePair[0]] = keyValuePair[1]

print("Starting Kafka producer for stock market data...")
while True:
    for key, value in apiKey.items():
        response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + key + "&interval=1min&apikey=" + value)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            ticker = data['Meta Data']['2. Symbol']
            data['Meta Data']['Ticker'] = ticker
            producer.send('stockPrice', value=data)
    sleep(30)