from com.com import get_bp
from com.data_import import ZH_JSON, ITEM_JSON, get_all


# 计算一定数量和花费金币的情况下,那个装备利润最高

# 定义一个函数，用于过滤列表
def fil_list(list_all, tType_fil: str = 'o', tier_fil: int = None,
             tag1_fil: list = ["common", "uncommon", "flawless", "epic", "legendary"]):
    """
    对列表进行过滤
    :param list_all: 原始列表
    :param tType_fil: o提供,r请求
    :param tier_fil: 最大要求等级
    :param tag1_fil: 允许品质组成的列表
    :return: 过滤后的列表
    """
    # 创建一个新的列表
    new_list = []

    # 遍历原始列表
    for i in list_all:

        # 如果tType_fil不为空且i['tType']不等于tType_fil，则跳过
        if tType_fil and i['tType'] != tType_fil:
            continue
        # 如果tier_fil不为空且i['tier']不在tier_fil中，则跳过
        if tier_fil and i['tier'] > tier_fil:
            continue
        # 如果tag1_fil不为空且i['tag1']不在tag1_fil中，则跳过
        if not i["tag1"]: i['tag1'] = 'common'  # 即普通

        if tag1_fil and i['tag1'] not in tag1_fil:
            continue

        # 将满足条件的元素添加到新列表中
        new_list.append(i)
    # 返回新列表
    return new_list


# 获取订单图纸的原始数据,并计算净利润,返回有利可图的订单
def get_order_drawings(blueprint: dict, 有利润: bool = False, 有经验: bool = True):
    """
    获取订单图纸的原始数据,并计算净利润,返回有利可图的订单
    :param blueprint: 从api中获取的单条订单信息
    :param 有利润: 是否要求有利润
    :return:
    """
    uid = blueprint['uid']
    for k, v in ITEM_JSON.items():
        if v['uid'] == uid:
            if not blueprint['goldPrice']:
                continue
            if 有利润 and v['value'] < blueprint['goldPrice']:
                continue
            if 有经验 and v['xp'] == 0:
                continue

            blueprint.update(get_bp(uid))
            blueprint['品质'] = ZH_JSON[blueprint['tag1'] + '_name']
            blueprint['净利润'] = v['value'] - blueprint['goldPrice']

            return blueprint


# 用表格把数据展示出来
def show_data(list_all: list):
    print("序号\t名称\t英文名\t类别\t等级\t品质\t市场价\t净利润\t日最大经验\t金币数限制\t售卖数量限制")
    for i, blueprint in enumerate(list_all):
        print(f"{i + 1}\t{blueprint['名称']}\t{blueprint['en_name']}\t{blueprint['装备类别']}\tT{blueprint['tier']}\t"
              f"{blueprint['品质']}\t{blueprint['goldPrice']}\t{blueprint['净利润']}\t"
              f"{blueprint['日最大经验']}\t{blueprint['金币限制']}\t{blueprint['数量限制']}")
    pass


# 定义一个主函数
def main(tType_fil: str = 'o', tier_fil: int = None, tag1_fil: list = None, num_day=200, money=1000000):
    print(f'\n限制条件,最大等级限制:{tier_fil} ;日最大出售量:{num_day} ;金币限制:{money}\n')
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
        if i['净利润'] >= 0:
            金币限制 = float('inf')
        else:
            金币限制 = int(money / abs(i['净利润'])) * i['item_data']['xp']
        数量限制 = num_day * i['item_data']['xp']
        日最大经验 = min(数量限制, 金币限制)
        i['日最大经验'] = 日最大经验
        i['金币限制'] = 金币限制
        i['数量限制'] = 数量限制
        set_list.append(i)

    ## 展示之前 先做一下清理
    set_list = fil_data_desc(set_list)

    sorted_data_desc = sorted(set_list, key=lambda x: x['日最大经验'], reverse=True)

    show_data(sorted_data_desc[:20])


def fil_data_desc(data_desc):
    t = {}
    for i in data_desc:
        tmp_id = i['uid'] + "_" + i['品质']
        if tmp_id not in t.keys():
            t[tmp_id] = i
        elif t[tmp_id]['id'] < i['id']:
            t[tmp_id] = i

        pass
    return list(t.values())


if __name__ == '__main__':
    main(tier_fil=7, num_day=200, money=1000000)
