from elasticsearch import helpers
import pickle
import json
import io
import time
PATH = '/home/yubowen/experiments/neg-para/search-engine/para-nmt-5m-processed.txt'
sentence_pairs_path = 'sentence_pairs_0_30k_neg_100.json'

# unpaired_sentences_path = 'unpaired_sentences.json'



def search(es_client, query_term, field = 'content',phrase_match = False,num = 3):
    es_search_options = set_search_optional(query_term = query_term, field = field ,phrase_match = phrase_match)
    es_result = get_search_result(es_client, es_search_options)
    final_result = get_result_list(es_result,num = num)
    return final_result

def get_para_5m_raw_data():
    examples = []
    lines = io.open(PATH, 'r', encoding='utf-8').readlines()
    for i in lines:
        s1 = i.split("\t")[0].lower()
        s2 = i.split("\t")[1].lower()
        examples.append([s1, s2])
    return examples


def set_search_optional(query_term,field,phrase_match):
    # 检索选项

    es_search_options = {"query":{}}
    if phrase_match:
        es_search_options["query"]["term"]={field:query_term}
    else:
        # es_search_options["query"]["match"]={field:{"query":query_term, "minimum_should_match": "75%"}}
        es_search_options["query"]["bool"]={"should":{ "match":{field:{"query":query_term, "minimum_should_match": "80%"}} }}
    return es_search_options



def get_search_result(es_client,es_search_options, scroll='5m',index='para-nmt-50m', doc_type='sentence', timeout="1m"):
    es_result = helpers.scan(
        client=es_client,
        query=es_search_options,
        scroll=scroll,
        index=index,
        doc_type=doc_type,
        timeout=timeout
    )
    return es_result



def get_result_list(es_result, num):
    final_result = []
    for i,item in enumerate(es_result):
        if i < num: 
            final_result.append(item['_source'])
        else:
            break
    return final_result 
      


def content_search():# 是否为短语 
    pass 

def in_title_search():# 是否为短语 
    pass
    
# print(es.search(index="sogout_data",doc_type="page",body=body))


if __name__ == '__main__':
    
    from elasticsearch import Elasticsearch
    import json
    import sys
    es_client = Elasticsearch('http://192.168.124.87:9200/')
    sentences = get_para_5m_raw_data()
    sentence_pairs = []
    unpaired_sentences = []
    # flag = False
    start_time = time.time()
    for i, sentence in enumerate(sentences):
        origin, para = sentences
        final_results = search(es_client = es_client, query_term= origin, field = 'content',phrase_match = False,num = 100)
        if len(final_results) > 0:
            results = []
            for i in final_results:
                if i['content'] != origin and i['content'] != para:
                    results.append(i['content'])
            sentence_pairs.append({'orig':origin,'pos':para, 'neg':results})
                    # flag = True
                    # break
        # if not flag:
        #     unpaired_sentences.append({'orig':origin,'pos':para})
        if i > 10:
            print ('has searched',i,'sentences')
            current_time = time()
            print((current_time-start_time)/i,'s per search')
            break
        if (i%1000==0):
            print ('has searched',i,'sentences')
            current_time = time.time()
            print((current_time-start_time)/i,'s per search')
            

    # with open('%s.json'% sys.argv[1], 'w') as f:
    #     f.write(json.dumps(final_results,ensure_ascii=False))
    with open(sentence_pairs_path,'w') as f:
        json_result = json.dumps(sentence_pairs, indent=2)
        f.write(json_result)

    # with open(unpaired_sentences_path,'w') as f:
    #     json_result = json.dumps(unpaired_sentences, indent=2)
    #     f.write(json_result)
        