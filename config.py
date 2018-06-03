import os
import sys
import platform
import codecs
import pandas as pd
import numpy as np
import re
import gc
import math
import _pickle as pickle
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S %p', level=logging.INFO)

# from tqdm import tqdm
from functools import partial
import warnings
warnings.filterwarnings('ignore')

label2int = {"POSITIVE":1,"NEGATIVE":0}
int2label = {1:"POSITIVE",0:"NEGATIVE"}

PATH_Mac = "/Users/yubowen/数据/代码/experiments/neg-para"
PATH_Ubuntu = '/home/yubowen/neg-para'

def isMacSystem():
    return 'Darwin' in platform.system()


class Config():
    project_dir = PATH_Mac if isMacSystem() else PATH_Ubuntu
    data_dir = project_dir + "/data"
    cache_dir = project_dir + "/cache"


    ## 复赛数据
    para_5m_LSH_path = data_dir + "/LSH-para-5m.json"
    para_5m_raw_path = data_dir + "/para-nmt-5m-processed.txt"
    train_path = data_dir + "/data/data_in_classification/without_first_two_para_train_data.json"
    test_path = data_dir + "/data/data_in_classification/without_first_two_para_test_data.json"

    ## 词性dict
    word_property_embed_dict_path = cache_dir + "/wordp_embed.dict.pkl"
    ## 词dict及预训练权重
    word_embed_dict_path = cache_dir + "/word_embed.dict.pkl"
    word_embed_weight_path = cache_dir + "/word_embed.npy"
    ## 字dict及预训练权重
    char_embed_dict_path = cache_dir + "/char_embed.dict.pkl"
    char_embed_weight_path = cache_dir + "/char_embed.npy"

    ## HAN && HCN
    ## 截断补齐句子个数
    sentence_num = 45
    ## 截断补齐句子词的个数
    sentence_word_length = 48
    ## 截断补齐句子字的个数
    sentence_char_length = 84

    ## 截断补齐文本词的个数
    word_seq_maxlen = 1143
    ## 截断补齐文本字的个数
    char_seq_maxlen = 1962
