
import pickle
from pyelasticsearch import ElasticSearch
from pyelasticsearch import bulk_chunks
import platform
import logging
import time
import os
import io
from logging.handlers import RotatingFileHandler
PATH = '/home/yubowen/experiments/neg-para/search-engine/para-nmt-5m-processed.txt'
es = ElasticSearch('http://192.168.124.87:9200/',http_auth=(user,pass), verify_certs=False))



def init_log():
    logging.getLogger().setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d]  %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # add log ratate
    Rthandler = RotatingFileHandler("backend_run.log", maxBytes=1000 * 1024 * 1024, backupCount=1000,
                                    encoding="gbk")
    Rthandler.setLevel(logging.INFO)
    Rthandler.setFormatter(formatter)
    logging.getLogger().addHandler(Rthandler)


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
        yield es.index_op(dic)


if __name__ == '__main__':
    init_log()
    sentences = get_para_5m_raw_data()
    for chunk in bulk_chunks(document(sentences), docs_per_chunk=10000,
        bytes_per_chunk=100000):
        es.bulk(chunk, doc_type='sentence', index='para-nmt-50m')
        doc_num += 10000
        print("indexed"+str(doc_num)+"docs")
        logging.info("indexed"+str(doc_num)+"docs")