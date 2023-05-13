# BDAproject

As climate change continues to dominate headlines, our topic modeling analysis can help businesses stay informed and proactively manage risk.

1. Using NYU email account, open link in browser https://console.cloud.google.com/compute/instances?project=bda-project-384817. Alternatively, after landing on the project home page click the navbar on the left and select "Compute Engine". 
2. Click on "SSH" under "Connect" next to the instance name. This starts a new terminal.
3. Run Kafka Zookeeper in a terminal as ```bash startKafkaZookeeper.sh```
4. Run Kafka Server in another terminal as ```bash startKafkaServer.sh```
5. Run stock price API Kafka producer in another terminal as ```bash startProducerStocks.sh```
6. Run news API Kafka producer in another terminal as ```bash startProducerNews.sh```
7. Run Kafka consumer in another terminal as ```bash startConsumer.sh```
8. Start Flask server as ```bash startFlaskServer.sh```. **Open the external IP address** as mentioned as soon as the Flask server starts. (Current value is http://34.125.95.198:5000/). The internal localhost IP address cannot be used in this case.
