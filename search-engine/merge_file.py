import json

file1 = 'sentence_pairs_0_30k.json'
file2 = 'sentence_pairs_0_30k_para.json'

file3 = 'sentence_pairs_0_30k_paired.json'


d1 = json.load(open(file1,'r'))
d2 = json.load(open(file1,'r'))


print(len(d1))

js = []

for i in len(d1):
    assert d1[i]['pos'] == d2[i]['pos']
    js.append({'orig':d1[i]['orig'],'para':d1[i]['pos'], 'neg_orign':d1[i]['neg'], 'neg_para':d2[i]['neg']})


    with open(file3,'w') as f:
        json_result = json.dumps(js, indent=2)
        f.write(json_result)