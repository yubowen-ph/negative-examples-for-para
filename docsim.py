from utils import *
import os
from config import Config
import time
import numpy as np
from gensim import corpora
from gensim.similarities import Similarity

remarks = '1k'
nums = 1000

sentences_path = Config.cache_dir + "/sentences_%s.pkl"%remarks
sim_path = Config.cache_dir + "/docsim/sim_%s.pkl"%remarks
indices_path = Config.data_dir + "/docsim/indices_%s.pkl"%remarks
corpus_path = Config.cache_dir + "/docsim/corpus_%s.pkl"%remarks


if os.path.exists(sentences_path):
    raw_para_sentences = pickle.load(open(sentences_path,"rb"))
else:
    raw_para_sentences = get_para_5m_raw_data()[:nums]
    with open(sentences_path,'wb') as f:
        pickle.dump(raw_para_sentences, f)



if os.path.exists(sim_path):
    similarity = pickle.load(open(sim_path,"rb"))
    corpus = pickle.load(open(sim_path,"rb"))
else:  
    similarity, corpus =  get_docsim_feature(raw_para_sentences, remarks)  
    with open(sim_path,'wb') as f:
        pickle.dump(similarity, f, protocol=4)





  


t1 =  time.time()

for i in corpus:
    print(i)
    x_test = i
    break

result = similarity[x_test]

indices = [index for (index, distance) in result]


for index in indices:
    print(raw_para_sentences[index])



t2 = time.time()

print(t2-t1)
# print(indices)  

