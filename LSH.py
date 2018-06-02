from sklearn.neighbors import LSHForest
from utils import *
import os
from config import Config
import time


remarks = '100k'
nums = 100000

sentences_path = Config.cache_dir + "/sentences_%s.pkl"%remarks
lshf_path = Config.cache_dir + "/lshf_%s.pkl"%remarks
tfidf_vec_path = Config.cache_dir + "/tfidf_%s.pkl"%remarks
indices_path = Config.data_dir + "/indices_%s.pkl"%remarks

if os.path.exists(sentences_path):
    raw_para_sentences = pickle.load(open(sentences_path,"rb"))
else:
    raw_para_sentences = get_para_5m_raw_data()[:nums]
    with open(sentences_path,'wb') as f:
        pickle.dump(raw_para_sentences, f)


if os.path.exists(tfidf_vec_path):
    tfidf_vec = pickle.load(open(tfidf_vec_path,"rb"))
else:  
    tfidf_vec =  get_tfidf_feature(raw_para_sentences, remarks)  
    with open(tfidf_vec_path,'wb') as f:
        pickle.dump(tfidf_vec_path, f)


if os.path.exists(lshf_path):
    lshf = pickle.load(open(lshf_path,"rb"))
else:  
    lshf = LSHForest(random_state=42)  
    lshf.fit(tfidf_vec.toarray()) 
    with open(lshf_path,'wb') as f:
        pickle.dump(lshf, f, protocol=4) 

  
orig_tfidf_vecs = [tfidf_vec[i] for i in range(0, len(tfidf_vec), 2)]


t1 =  time.time()
x_test = tfidf_vec[0] 
distances, indices = lshf.kneighbors(orig_tfidf_vecs.toarray(), n_neighbors = 3)  


with open(indices_path,'wb') as f:
    pickle.dump(indices, f)
# print(distances)  

# print('original', raw_para_sentences[0])
# print('para', raw_para_sentences[1])

# for i in indices:
#     print(raw_para_sentences[0][i])


t2 = time.time()

print(t2-t1)
# print(indices)  

