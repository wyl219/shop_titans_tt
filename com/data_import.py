import json
import requests
def get_json(url):
    try:
        for i in range(5):
            a=requests.get(url)
            if a.status_code==200:
                return a.text
    except :
        Exception(f"获取{url}失败")
def get_all():
    a=get_json(r'https://smartytitans.com/api/item/last/all')

    return json.loads(a)['data']

ITEM_JSON=json.loads(get_json(r"https://smartytitans.com/assets/gameData/items.json"))
EN_JSON=json.loads(get_json(r"https://smartytitans.com/assets/gameData/texts_en.json"))['texts']
ZH_JSON=json.loads(get_json(r"http://st.yikexu.wang/data/texts_zh.json"))['texts']
ITEM_TYPE_ZH=json.loads(get_json(r"http://st.yikexu.wang/data/item_type_zh.json"))

# ITEM_JSON=json.load(open(r'./data/items.json','r',encoding='utf-8'))
# ZH_JSON=json.load(open(r'./data/texts_zh.json','r',encoding='utf-8'))['texts']
# EN_JSON=json.load(open(r'./data/texts_en.json','r',encoding='utf-8'))['texts']
# ITEM_TYPE_ZH=json.load(open('item_type_zh.json',"r",encoding='utf-8'))