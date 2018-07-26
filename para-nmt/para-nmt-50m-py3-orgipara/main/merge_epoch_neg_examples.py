import json


d1 = json.load(open('../data/generated_samples_lstmmax_epoch_0.json','r'))

sentence_to_id = {}

samples = []

for i in range(len(d1)):
    sentence_to_id[d1[i]['orig']] = i
    samples.append({'orig':d1[i]['orig'],'para':d1[i]['para'], 'neg_orig_epoch0':d1[i]['neg_orign'], 'neg_para_epoch0':d1[i]['neg_para']})

samples = d1

for j in range(1,10):
    d = json.load(open('../data/generated_samples_lstmmax_epoch_%d.json'%(j),'r'))
    for i in range(len(d)):
        samples[sentence_to_id[d[i]['orig']]]['neg_orig_epoch'%j]=d[i]['neg_orign']
        samples[sentence_to_id[d[i]['orig']]]['neg_para_epoch'%j]=d[i]['neg_para']

with open("../data/generated_samples.json",'w') as f:
    json_result = json.dumps(samples, indent=2)
    f.write(json_result)