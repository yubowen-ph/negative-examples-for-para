
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk
import time
import os
import io
PATH = '/home/yubowen/experiments/neg-para/search-engine/para-nmt-5m-processed.txt'
es = Elasticsearch('http://192.168.124.87:9200/')





def get_para_5m_raw_data():
    examples = []
    lines = io.open(PATH, 'r', encoding='utf-8').readlines()
    for i in lines:
        s1 = i.split("\t")[0].lower()
        s2 = i.split("\t")[1].lower()
        examples.append({'content':s1, 'type':'origin'})
        examples.append({'content':s2, 'type':'para'})
    return examples


def document(sentences):
    for s in sentences:
        dic = {'content': s['content'], 
                            'type': s['type']
                            }
        yield dic


if __name__ == '__main__':
    # init_log()
    doc_num = 0 
    sentences = get_para_5m_raw_data()
    for ok, result in streaming_bulk(
        es,
        document(sentences),
        index='para-nmt-50m',
        doc_type='sentence',
        chunk_size=5000):
        action, result = result.popitem()
        doc_id = '/%s/doc/%s' % (index, result['_id'])
        doc_num += 5000
        print("indexed"+str(doc_num)+"docs")
        # logging.info("indexed"+str(doc_num)+"docs")