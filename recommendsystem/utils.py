import random
from pandas import Series, DataFrame
import numpy as np

#engine_cf中使用到
#计算单独一行中不为0的个数
def count_set(train):
    count = 0
    for i in train:
        if i != 0:
            count += 1

    return count

#engine_tags中使用到
def get_user_item_tag(train):
    # etl模块，输入train，返回u，i，tag
    # todo:如何解决顺序问题,改变数据类型为list
    u = set()
    i = set()
    t = set()
    for a in train:
        u.add(a[0])
        i.add(a[1])
        for tmp in a[2]:
            t.add(tmp)
    return u, i, t

def get_user_tags(train):
    # 获得user_tags矩阵
    users, items, tags = get_user_item_tag(train)
    result = DataFrame(0, index= tags, columns= users)
    for i in train:
        user = i[0]
        tags = i[2]
        for t in tags:
            result[user][t] += 1
    return result

def get_item_tags(train):
    # 获取item_tags矩阵
    users, items, tags = get_user_item_tag(train)
    result = DataFrame(0, index= tags, columns= items)
    for i in train:
        item = i[1]
        tags = i[2]
        for t in tags:
            result[item][t] += 1
    return result

def get_user_item(train):
    # 获取item_tags矩阵
    users, items, tags = get_user_item_tag(train)
    result = DataFrame(0, index= items, columns= users)
    for i in train:
        user = i[0]
        item = i[1]
        result[user][item] += 1
    return result

def count_tags(train):
    # 返回每个标签出现的次数
    tags = get_user_item_tag(train)[2]
    result =Series(0, index= tags)
    for i in train:
        tags = i[2]
        for t in tags:
            result[t] += 1
    return result


#获取三元组数据的行和列
def get_columns_and_index(train):

    # todo:如何解决顺序问题
    u = set()
    i = set()
    for a in train:
        u.add(a[0])
        i.add(a[1])
    return u, i


#根据user、item、tag为主键切分数据集
# 该数据集的作用是，测试给用户关于某一物品推荐的标签是否和其真正打的标签一致
# 输入的是原始数据集，返回的是分类好的训练集和测试集
# 注意，此处采用的是随机分类，所以只有在数据量比较大的情况下，才可以得到比较符合设定的比例
def SplitData(records):
    # todo：该部分上不可用
    # todo：需要原始格式的数据为user：item：tag格式
    # 假设此处使用的是三元组格式
    test = []
    train = []
    for record in records:
            if random.randint(1, 10) == 1:
                test.append(record)
            else:
                train.append(record)

    return train, test


def count_set_not_nan(train):
    count = 0
    for i in train:
        if not np.isnan(i):
            count += 1

    return count
