#!/usr/bin/env python3

import json
import random
import string
from datetime import datetime
from elasticsearch import Elasticsearch

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

with open('data.txt') as json_file:  
    data = json.load(json_file)

# generate server-name
idstr = randomString(10)
data['source']['name'] = "server-" + idstr
print(data['source']['name'])

# generate timestamp
data['timestamp'] = datetime.now().strftime("%Y-%m-%dT%X")
print(data['timestamp'])

es =  Elasticsearch()
print(es.index(index='aminertest', doc_type='data',body=json.dumps(data).encode('ascii')))
