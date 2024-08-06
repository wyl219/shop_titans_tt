# 英译汉
import json
zh_json=json.load(open(r'./data/texts_zh.json','r',encoding='utf-8'))['texts']
en_json=json.load(open(r'./data/texts_en.json','r',encoding='utf-8'))['texts']

# json.dump(en_json,open(r'./data/texts_en.json','w',encoding='utf-8'),ensure_ascii=False,indent=4)

def en2zh(en:str="",zh:str=""):
    t,t1=en_json,zh_json
    if not en :
        t,t1=t1,t
        en=zh


    for k,v in t.items():
        if v==en:
            return t1[k]



if __name__ == '__main__':
    en="Kiku-Ichimonji"
    print(en2zh(en=en))
    zh="菊一文字"
    print(en2zh(zh=zh))
