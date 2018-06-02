import numpy as np
import io
from random import randint
from random import choice
from random import shuffle
from config import Config
import os
from sklearn.feature_extraction.text import TfidfVectorizer 
import string
import pickle


def get_para_5m_raw_data():
    examples = []
    lines = io.open(Config.para_5m_raw_path, 'r', encoding='utf-8').readlines()
    for i in lines:
        s1 = i.split("\t")[0].lower()
        s2 = i.split("\t")[1].lower()
        examples.append(s1)
        examples.append(s2)
    return examples


class Tokenizer():
    def __init__(self):
        self.n = 0
    def __call__(self, line):
        tokens = [word for word in line.split() if word not in string.punctuation]
        self.n += 1
        return tokens



def get_tfidf_feature(contents, remarks=""):
    result_path = Config.cache_dir + "/tfidf_%s.pkl"%remarks
    tfidf_vec_path = Config.cache_dir + "/%s_vecs.pkl"%remarks
    tfidf_vec = TfidfVectorizer(tokenizer=Tokenizer(), min_df=2, max_df=0.95, sublinear_tf=True)
    result = tfidf_vec.fit_transform(contents)
    print("tfidf shape is ",result.shape,"="*10,"vocabulary counts : ", len(tfidf_vec.vocabulary_))
    pickle.dump(result, open(result_path,"wb"))
    pickle.dump(tfidf_vec, open(tfidf_vec_path,"wb"))
    return result