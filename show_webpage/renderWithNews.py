import json
import os

from pymongo import MongoClient

from flask import Flask, render_template
from flask import request

from datetime import datetime, timedelta

client = MongoClient('localhost:27017')
collection1 = client.bigdata.stock_collection
collection2 = client.bigdata.news_collection

def calculate_rate(opening_price, closing_price):
    difference = closing_price - opening_price
    percentage_gain_over_loss = (difference / opening_price) * 100
    return percentage_gain_over_loss

def read_new_stock_price():
    new_price = {}
    if len(new_price) != 0:
        for i in companyTickers:
            new_price[i] = {}

            rawData = collection1.find({"Ticker": i}).sort([("_id", -1)]).limit(1)
            lastRefreshed = rawData['Meta Data']['3. Last Refreshed']
            stockDetails = rawData['Time Series (1min)'][lastRefreshed]
            new_rate = calculate_rate(stockDetails['1. open'], stockDetails['4. close'])
            new_value = stockDetails['4. close']

            new_price[i]['rate'] = new_rate
            new_price[i]['value'] = new_value    
    return new_price

def update_output_json(heatData):
    new_price = read_new_stock_price()
    for i in companyTickers:
        for i in heatData['children'][0]['children']:
            if i['name'] == i:
                i['value'] = new_price[i]['rate']
                i['rate'] = new_rate[i]['value']
    return heatData

def within_one_week(date_string):
    date_time_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    now = datetime.now(date_time_obj.tzinfo)
    one_week_ago = now - timedelta(weeks=1)
    if one_week_ago <= date_time_obj <= now:
        return True
    else:
        return False

def checkTopic(newsItem):
    abstractAndLeadPara = newsItem['abstract'] + newsItem['lead_paragraph']
    if "climate" in abstractAndLeadPara and "change" in abstractAndLeadPara:
        return True
    return False

def getRelatedNewsList(data):
    news = []
    count, i = 0, 0
    while (count < 10) and (i < len(data['response']['docs'])):
        newsItem = data['response']['docs'][i]
        if within_one_week(newsItem['pub_date']) and checkTopic(newsItem):
            l = {}
            l['title'] = newsItem['abstract'][:120] + " ..."
            l['link'] = newsItem['web_url']
            news.append(l)
            count+=1
        i += 1
    return news

def getNewsData():
    data = collection2.find({}).sort([("_id", -1)]).limit(1)
    result = {}
    for doc in data:
        result = doc
    if len(result) == 0:
        with open('sample.json', 'r') as f:
            result = json.load(f)
    return getRelatedNewsList(result)

with open('data.json', 'r') as f:
    heatData = json.load(f)

companyTickers = []
fileTickers = open('apiKeys.txt', 'r')
while True:
    s = fileTickers.readline()
    if not s:
        break
    s = s.strip('\n')
    companyTickers.append(s.split(',')[0])

app = Flask("flask_demo")

@app.route('/')
def index():
    return render_template('index.html')


PEOPLE_FOLDER = os.path.join('static', 'graph_photo')

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/show_topics', methods=['GET', 'POST'])
def show_topics():
    full_filename = [os.path.join(app.config['UPLOAD_FOLDER'], 'topic1.png'), os.path.join(app.config['UPLOAD_FOLDER'], 'topic2.png'), os.path.join(app.config['UPLOAD_FOLDER'], 'topic3.png'), os.path.join(app.config['UPLOAD_FOLDER'], 'topic0.png')]
    return render_template("show_topics.html", wordClouds = full_filename)

@app.route('/show_image', methods=['GET', 'POST'])
def show_image():
    full_filename_topics = os.path.join(app.config['UPLOAD_FOLDER'], 'topic-score-turn-2.png')
    return render_template("show_image.html", graph_image = full_filename_topics)

@app.route('/show_image_overTime', methods=['GET', 'POST'])
def show_image_overTime():
    full_filename_over_time = os.path.join(app.config['UPLOAD_FOLDER'], 'topic-time-turn-2.png')
    return render_template("show_image_overTime.html", graph_image = full_filename_over_time)

@app.route('/recent_news', methods=['GET', 'POST'])
def recent_news():
    return render_template("recent-news.html", result=getNewsData())

@app.route('/heat_local')
def heat_local():
    return render_template('heatLocal.html')

@app.route('/get_data')
def get_data():
    newHeatData = update_output_json(heatData)
    with open('data.json', 'w') as f:
        json.dump(newHeatData, f)
    with open('data.json', 'r') as f:
        updatedHeatData = json.load(f)
    return updatedHeatData

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0') 