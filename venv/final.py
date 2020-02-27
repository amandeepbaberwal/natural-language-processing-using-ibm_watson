import requests
import pyodbc
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('{your_ibm_watson_api_key_here}')
service = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    authenticator=authenticator)
service.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')
# Connecting to Azure Server
server = ''
database = ''
username = ''
password = ''
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

url = ('https://newsapi.org/v2/everything?q=trump&domains=cnn.com&apiKey={your_newsapi.org_api_key_here}')

response = requests.get(url)

#print(response.json())
r = response.json()

a_list = r['articles']
for a in a_list:
    print(a['url'])
    print(a['source']['name'])
    #print(a['content'])
    try:
        response = service.analyze(
                text=a['content'],
                features=Features(keywords=KeywordsOptions(emotion=True, limit=2))).get_result()
        y = json.dumps(response)
        data = json.loads(y)
        i = 0
        print(data)
        for item in data['keywords']:
            if i == 0:
                sadness = item["emotion"]["sadness"]
                joy = item["emotion"]["joy"]
                fear = item["emotion"]["fear"]
                disgust = item["emotion"]["disgust"]
                anger = item["emotion"]["anger"]
                cursor.execute("INSERT nltk (source, url, sadness, joy, fear, disgust, anger) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (a['source']['name'], a['url'],sadness, joy, fear, disgust, anger))
                cnxn.commit()
                print("saving to database: ")
                i = i+1
    except:
        print("this is a error")

