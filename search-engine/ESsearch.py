from elasticsearch import helpers





def search(es_client, query_term, field = 'content',phrase_match = False,num = 3):
    es_search_options = set_search_optional(query_term = query_term, field = field ,phrase_match = phrase_match)
    es_result = get_search_result(es_client, es_search_options)
    final_result = get_result_list(es_result,num = num)
    return final_result




def set_search_optional(query_term,field,phrase_match):
    # 检索选项

    es_search_options = {"query":{}}
    if phrase_match:
        es_search_options["query"]["term"]={field:query_term}
    else:
        es_search_options["query"]["match"]={field:{"query":query_term, "minimum_should_match": "75%"}}
        es_search_options["query"]["bool"]={"must":{"match":{field:query_term}}
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
    query = r"that's his dead son 's birthday"
    final_results = search(es_client = es_client, query_term= query, field = 'content',phrase_match = False,num = 10)
    for i in final_results:
        print(i)
    print(len(final_results))
    # with open('%s.json'% sys.argv[1], 'w') as f:
    #     f.write(json.dumps(final_results,ensure_ascii=False))

