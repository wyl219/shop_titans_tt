import copy
import json

item_json=json.load(open(r'../data/items.json', 'r', encoding='utf-8'))
zh_json=json.load(open(r'../data/texts_zh.json', 'r', encoding='utf-8'))['texts']
en_json=json.load(open(r'../data/texts_en.json', 'r', encoding='utf-8'))['texts']
item_type_zh=json.load(open('../item_type_zh.json', "r", encoding='utf-8'))
print(item_json)
# 把字典改为uid为key的汉化字典,包含常用数据
new_dict={}

for k,v in item_json.items():
    en_dict=copy.deepcopy(v)
    en_dict['name']=en_json[k+'_name'] # 英文名字

    zh_dict=copy.deepcopy(en_dict)
    zh_dict['name']=zh_json[k+'_name'] # 汉化名字
    zh_dict['type']=item_type_zh[en_dict['type']]
    for k in ['worker1','worker2','worker3']:
        if zh_dict[k]:
            zh_dict[k]=zh_json['worker_'+zh_dict[k]]
    for k in ['resource1','resource2','resource3']:
        if zh_dict[k]:
            zh_dict[k]=zh_json['resource_'+zh_dict[k]]
    zh_dict['en_dict'] = en_dict
    new_dict[en_dict['uid']]=zh_dict

    pass

json.dump(new_dict, open(r'../item_zh.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
print(new_dict)