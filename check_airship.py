import json

from com import get_bp
from data_import import ZH_JSON, EN_JSON, ITEM_JSON, ITEM_TYPE_ZH

from check_mo import get_all
from check_mo import fil_list
from check_mo import fil_data_desc
# 计算一定数量和花费金币的情况下,那个装备利润最高





# 获取订单图纸的原始数据,并计算净利润,返回有利可图的订单
def get_order_drawings(blueprint: dict,有飞龙分=True):
    """
    获取订单图纸的原始数据,并计算净利润,返回有利可图的订单
    :param blueprint: 从api中获取的单条订单信息
    :param 有利润: 是否要求有利润
    :return:
    """
    uid = blueprint['uid']
    for k, v in ITEM_JSON.items():
        if v['uid'] == uid:
            if not blueprint['goldPrice']: # 金币买不到
                continue


            blueprint.update(get_bp(uid))
            blueprint['品质'] = ZH_JSON[blueprint['tag1'] + '_name']
            if 有飞龙分 and not blueprint['飞龙威力']:
                continue
            blueprint['净利润'] =  int(v['value'] - blueprint['goldPrice'])
            blueprint['飞龙分单价'] =int( blueprint['净利润'] / blueprint['飞龙威力'])

            return blueprint


# 用表格把数据展示出来
def show_data(list_all: list):
    # 分类展示
    for h in["武器", "护甲", "饰品","副甲","其他"]:
        print(f"\n{h}类")
        print("序号\t名称\t英文名\t类别\t等级\t品质\t市场价\t飞龙分\t净利润\t飞龙分单价")
        i=0
        for blueprint in list_all:
            if blueprint['飞龙类别'] != h:
                continue
            if i>4:
                 break
            i+=1
            print(f"{i}\t{blueprint['名称']}\t{blueprint['en_name']}\t{blueprint['装备类别']}\tT{blueprint['tier']}\t"
                  f"{blueprint['品质']}\t{blueprint['goldPrice']}\t{blueprint['飞龙威力']}\t"
                  f"{blueprint['净利润'] }\t{blueprint['飞龙分单价']}")
        pass


# 定义一个主函数
def main(tType_fil: str = 'o', tier_fil: int = None, tag1_fil: list = ["common"]):
    print(f'\n限制条件,最大等级限制:{tier_fil} \n')
    # 从list_all.json文件中读取数据
    # list_all = json.load(open("list_all.json", 'r', encoding='utf-8'))['data']
    #
    list_all = get_all()
    # 调用fil_list函数，过滤列表
    new_list = fil_list(list_all, tType_fil, tier_fil, tag1_fil)

    set_list = []
    # 获取列表数据
    for i in new_list:
        if not get_order_drawings(i):
            continue
        set_list.append(i)

    ## 展示之前 先做一下清理
    set_list = fil_data_desc(set_list)

    sorted_data_desc = sorted(set_list, key=lambda x: x['飞龙威力'], reverse=True)

    show_data(sorted_data_desc)



if __name__ == '__main__':
    main(tier_fil=7)
