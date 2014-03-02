
import json
import sys

from elasticsearch import Elasticsearch
es = Elasticsearch("XXX")


data = json.load(open(sys.argv[1]))

for i, element in enumerate(data):
    es.index(index="sunshine", doc_type='kdo', id=i, body=element)

