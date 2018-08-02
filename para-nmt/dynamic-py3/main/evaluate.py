import numpy as np
import io
from scipy.stats import spearmanr
from scipy.stats import pearsonr
from example import example

def get_seqs(p1, p2, words, params):
    p1 = example(p1)
    p2 = example(p2)

    if params.wordtype == "words":
        p1.populate_embeddings(words, True)
        p2.populate_embeddings(words, True)
    else:
        p1.populate_embeddings_ngrams(words, 3, True)
        p2.populate_embeddings_ngrams(words, 3, True)

    return p1.embeddings, p2.embeddings

def get_correlation(model, words, f, params):
    f = io.open(f, 'r', encoding='utf-8')
    lines = f.readlines()
    preds = []
    golds = []
    seq1 = []
    seq2 = []
    ct = 0
    for i in lines:
        i = i.split("\t")
        p1 = i[0]; p2 = i[1]; score = float(i[2])
        X1, X2 = get_seqs(p1, p2, words, params)
        seq1.append(X1)
        seq2.append(X2)
        ct += 1
        if ct % 100 == 0:
            x1,m1 = model.prepare_data(seq1)
            x2,m2 = model.prepare_data(seq2)
            scores = model.scoring_function(x1,x2,m1,m2)
            scores = np.squeeze(scores)
            preds.extend(scores.tolist())
            seq1 = []
            seq2 = []
        golds.append(score)
    if len(seq1) > 0:
        x1,m1 = model.prepare_data(seq1)
        x2,m2 = model.prepare_data(seq2)
        scores = model.scoring_function(x1,x2,m1,m2)
        scores = np.squeeze(scores)
        preds.extend(scores.tolist())
    return pearsonr(preds,golds)[0], spearmanr(preds,golds)[0]

def evaluate_all(model, words, params):
    prefix = "../data/"
    parr = []; sarr = []

    farr = ["annotated-ppdb-test",
            "STS/STS2012-test/STS2012.MSRpar.txt", 
            "STS/STS2012-test/STS2012.MSRvid.txt",
            "STS/STS2012-test/STS2012.SMTeuroparl.txt",
            "STS/STS2012-test/STS2012.surprise.OnWN.txt",
            "STS/STS2012-test/STS2012.surprise.SMTnews.txt",
            
            "STS/STS2013-test/STS2013.FNWN.txt",
            "STS/STS2013-test/STS2013.headlines.txt",
            "STS/STS2013-test/STS2013.OnWN.txt",
            
            "STS/STS2014-test/STS2014.deft-forum.txt",
            "STS/STS2014-test/STS2014.deft-news.txt",
            "STS/STS2014-test/STS2014.headlines.txt",
            "STS/STS2014-test/STS2014.images.txt",
            "STS/STS2014-test/STS2014.OnWN.txt",
            "STS/STS2014-test/STS2014.tweet-news.txt",
            
            "STS/STS2015-test/STS2015.answers-forums.txt",
            "STS/STS2015-test/STS2015.answers-students.txt",
            "STS/STS2015-test/STS2015.belief.txt",
            "STS/STS2015-test/STS2015.headlines.txt",
            "STS/STS2015-test/STS2015.images.txt",
            ]

    for i in farr:
        p,s = get_correlation(model, words, prefix + i, params)
        parr.append(p); sarr.append(s)

    s = ""
    for i,j,k in zip(parr,sarr,farr):
        s += str(i)+" "+str(j)+" "+k+" | "

    parr = np.asarray(parr)
    ppdb = parr[0]
    STS_2012 = np.mean(parr[1:6])
    STS_2013 = np.mean(parr[6:9])
    STS_2014 = np.mean(parr[9:15])
    STS_2015 = np.mean(parr[15:20])
    STS_12to15 = np.mean(parr[1:20])
    # STS_2016 = np.mean(parr[-5:])
    
    s += "STS_2012 : " + str(STS_2012) + "\n"
    s += "STS_2013 : " + str(STS_2013) + "\n"
    s += "STS_2014 : " + str(STS_2014) + "\n"
    s += "STS_2015 : " + str(STS_2015) + "\n"
    s += "STS_12to15 : " + str(np.mean(parr[1:20])) + "\n"
    # s += "STS_2016 : " + str(STS_2016) + "\n"
    s += "ppdb : " + str(ppdb) + "\n"
    
    '''
    with open("results.txt", "a") as f:
        f.write(s)
    '''
    print (s)
    return STS_12to15
