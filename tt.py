import json

list_all = json.load(open("list_all.json", 'r', encoding='utf-8'))['data']
t=[]
uid="druidcloak"
for i in list_all:
    if i['uid']==uid:
        if  not i['tag1']:
            if  i["tType"]=='o':
                t.append(i)
