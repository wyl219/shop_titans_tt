import copy
from com.data_import import ZH_JSON, EN_JSON, ITEM_JSON, ITEM_TYPE_ZH

MUNDRA_PRICE = dict(
    mundrahammer=700000,
    mundrabow=19400,
    mundrastaff=105000,
    mundrapotion=2850000,
    mundraarmor=33000,
    mundrahelm=12700000,
    mundrashield=5450000,
    mundraamulet=21000,
)


def get_bp(uid):
    item_data = copy.deepcopy(ITEM_JSON[uid])  # 直接再原始数据上修改,会导致重复调用后出错
    en_name = EN_JSON[uid + '_name']
    名称 = ZH_JSON[uid + '_name']
    装备类别 = ITEM_TYPE_ZH[item_data['type']]

    # 如果图纸是箱子图 经验是要附加上附魔的部分的
    # 价格只能算差不多
    # 各种属性也要增加
    if item_data['lTag3'] or item_data['lTag2']:  # lTag2保存了自带的元素,lTag3保存了自带的精萃
        a = item_data['lTag3'] or item_data['lTag2']  # 获取元素的uid
        ltag = ITEM_JSON[a]  # 获取元素的数据
        item_data['xp'] += min(item_data['xp'], ltag['xp'])  # 增加的经验取装备原来的经验和附魔经验的最小值
        # 然后是攻防血属性 如果不是亲和 那么跟经验一样的算法 加最小值 如果是亲和,附魔或元素的值要乘1.5
        # 因为自带元素的装备全亲和,所以直接乘1.5
        for k in ["atk", "def", "hp"]:
            if item_data[k] > 0: item_data[k] += min(item_data[k], ltag[k] * 1.5)

        if uid in MUNDRA_PRICE.keys():  # 但是穆达拉系列直接从数据中取
            item_data['value'] = MUNDRA_PRICE[uid]
        else:
            # 售价也要增加,怀疑应该是亲和增加1.1倍,这里的数据是已经增加了1倍了,所以这里要重新计算一下
            # 数据并不统一,这里直接加上附魔本身的0.1倍吧,和A大数据表得数一致
            item_data['value'] += ltag['value'] * 0.1
        del a, k, ltag  # 清理一下变量

    # 对于部分装备,不计算飞龙值
    if 装备类别 not in ["符文石", "月光石", "材料", "光环", "使魔"]:
        飞龙威力 = int((item_data['atk'] * 0.8 + item_data['def'] * 1.2 + item_data['hp'] * 5) + (
                    1 + float(item_data['eva']) * 10 + float(item_data['crit']) * 10))
        飞龙类别 = {"a": "护甲",
                    "b": "副甲",
                    "g": "副甲",
                    "h": "副甲",
                    "w": "武器",
                    "u": "饰品",
                    "x": "饰品",
                    "f": "饰品",
                    "z": "其他", }[item_data['type'][0]]
    else:
        飞龙威力 = 0
        飞龙类别 = "不可用"

    # 加个单工人经验
    if item_data['worker3']:
        单工人经验 = int(item_data['craftXp'] / 3)
    elif item_data['worker2']:
        单工人经验 = int(item_data['craftXp'] / 2)
    else:
        单工人经验 = item_data['craftXp']
    # 判断图纸是否有1.25里程碑
    for  i in range(1, 6):
        if "value" in item_data['upgrade' + str(i)]:
            里程碑价格加成=float(item_data['upgrade' + str(i)].split("*")[1])
            break
        else:
            里程碑价格加成=1
    return locals()  # 返回所有本地变量


## 写个金币格式转换的工具
def 金币格式转换(金币, s2i=False):
    """
    将int转换成KMGT的缩写形式,例如1100000 转换成1.1M
    如果s2i为True,则将KMGT的缩写形式转换成int
    否则,则将int转换成KMGT的缩写形式
    """
    单位 = ["", "K", "M", "G", "T"]
    if s2i:
        # 将KMGT的缩写形式转换成int
        if isinstance(金币, str):
            if len(金币) > 1 and 金币[-1] in 单位[1:]:
                单位索引 = 单位.index(金币[-1])
                金币数值 = float(金币[:-1])
                金币数值 *= 10 ** (3 * 单位索引)
                return int(金币数值)
            else:
                return int(金币)
        else:
            return int(金币)
    else:
        # 将int转换成KMGT的缩写形式
        if isinstance(金币, int):
            if 金币 == 0:
                return "0"
            else:
                单位索引 = 0
                while 金币 >= 1000 and 单位索引 < len(单位) - 1:
                    金币 /= 1000
                    单位索引 += 1
                return f"{金币:.1f}{单位[单位索引]}"
        else:
            return 金币


if __name__ == '__main__':
    uid='mundraamulet'
    p="123"
    a=get_bp(uid)
    # 测试代码
    print(金币格式转换(1100000))  # 输出: 1.1M
    print(金币格式转换("1.1M", s2i=True))  # 输出: 1100000
    print(金币格式转换(1000000000))  # 输出: 1.0G
    print(金币格式转换("1.0G", s2i=True))  # 输出: 1000000000

    print()
