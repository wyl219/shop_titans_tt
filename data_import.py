import json

ITEM_JSON=json.load(open(r'./data/items.json','r',encoding='utf-8'))
ZH_JSON=json.load(open(r'./data/texts_zh.json','r',encoding='utf-8'))['texts']
EN_JSON=json.load(open(r'./data/texts_en.json','r',encoding='utf-8'))['texts']
ITEM_TYPE_ZH=json.load(open('item_type_zh.json',"r",encoding='utf-8'))