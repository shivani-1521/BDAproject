# !pip install -U kaleido
# !pip install bertopic

from bertopic import BERTopic
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pymongo import MongoClient
from json import loads

def create_wordcloud(topic_model, topic):
    text = {word: value for word, value in topic_model.get_topic(topic)}
    wc = WordCloud(background_color="white", max_words=1000)
    wc.generate_from_frequencies(text)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('topic0.png', bbox_inches='tight')

client = MongoClient('localhost:27017')
collection2 = client.bigdata.news_collection

documents = []
for document in collection2.find({}):
    documents.append(dict(document))

articleWise= []
yearOfArticle = []

for data in documents:
  newsItem = data['response']['docs']
  for i in range(0, len(newsItem)):
      absAndLeadPara = newsItem[i]['abstract'] + newsItem[i]['lead_paragraph']
      if "climate" in absAndLeadPara and "change" in absAndLeadPara:
          articleWise.append(absAndLeadPara)
          yearOfArticle.append(year)
   

topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(articleWise)

freq = topic_model.get_topic_info()
fig = topic_model.visualize_barchart(top_n_topics=8)
fig.write_image('graph1.png', engine='kaleido')
topics_over_time = topic_model.topics_over_time(articleWise, yearOfArticle, nr_bins= 20)
fig = topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=11)
fig.write_image("graph2.png", engine='kaleido') 
create_wordcloud(topic_model, topic=0)