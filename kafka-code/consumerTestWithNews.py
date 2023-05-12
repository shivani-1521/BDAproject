from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads

topic1 = 'stockPrice'
topic2 = 'NYTNews'

client = MongoClient('localhost:27017')
collection1 = client.bigdata.stock_collection
collection2 = client.bigdata.news_collection

print("Starting Kafka consumer...")
# consumer for topic1
consumer1 = KafkaConsumer(
    topic1,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group1',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

# consumer for topic2
consumer2 = KafkaConsumer(
    topic2,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group2',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

# consume messages from topic1
for message in consumer1:
    if message.topic == topic1:
        message = message.value
        collection1.insert_one(message)

# consume messages from topic2
for message in consumer2:
    if message.topic == topic2:
        message = message.value
        collection2.insert_one(message)