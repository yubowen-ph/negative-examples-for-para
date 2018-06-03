import numpy as np
from config import Config
import os
import pickle


remarks = '100k'
sentences_path = Config.cache_dir + "/sentences_%s.pkl"%remarks
indices_path = Config.data_dir + "/indices_%s.pkl"%remarks
sentence_pairs_path = Config.data_dir + "/sentence_pairs_%s.json"%remarks

if not os.path.exists(sentences_path) or not os.path.exists(indices_path):
    print('文件缺失')
else:  
    raw_para_sentences = pickle.load(open(sentences_path,"rb"))
    indices = pickle.load(open(indices_path,"rb")).tolist()
    assert len(raw_para_sentences) == 2*len(indices),'indices与raw_para_sentences不匹配'
    sentence_pairs = []
    for i in range(len(indices)):
        kneighbors = indices[i]
        orig_index = 2*i
        para_index = 2*i+1
        if orig_index in kneighbors:
            kneighbors.remove(orig_index)
        if para_index in kneighbors:
            kneighbors.remove(para_index)
        neighbor_index = kneighbors[0]
        sentence_pairs.append({'ori':raw_para_sentences[orig_index],'pos':raw_para_sentences[para_index], 'neg':raw_para_sentences[neighbor_index]})
        with open(sentence_pairs_path,'w') as f:
            json_result = json.dumps(sentence_pairs, indent=2)
            f.write(json_result)