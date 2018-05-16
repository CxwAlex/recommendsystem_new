import random
import numpy
import datetime
from pandas import Series, DataFrame


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
def get_columns_and_index(train, user_place=0, item_place=1):

    # todo:如何解决顺序问题
    u = set()
    i = set()
    for a in train:
        u.add(a[user_place])
        i.add(a[item_place])

    user_std = sorted(list(u), key=int)
    item_std = sorted(list(i), key=int)

    return user_std, item_std


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
        if not numpy.isnan(i):
            count += 1

    return count


def datediff(date1, date2, return_type='day'):
    date1_std = datetime.datetime.strptime(date1,'%Y-%m-%d')
    date2_std = datetime.datetime.strptime(date2,'%Y-%m-%d')
    date_diff = date1_std - date2_std
    if return_type == 'day':
        return date_diff.days
    elif return_type == 'seconds':
        return date_diff.seconds
    elif return_type == 'week':
        return round(date_diff.days/7, 2)
    elif return_type == 'month':
        return round(date_diff.days/30, 2)
    elif return_type == 'year':
        return round(date_diff.days/365, 2)
    else:
        return None


#engine_social用到的etl模块：matrix2dataframe, raw2std, graph2dataframe

#根据具体的结构在完善，首先需要具备基础的将字典列表转换为dataframe的能力
def matrix2dataframe(matrix):
    if isinstance(matrix, dict):
        result = DataFrame(matrix, index=matrix.keys())
    elif isinstance(matrix, list):
        result = DataFrame(matrix)
    return result


def graph2dataframe(graph):
    result = DataFrame(0, columns=graph.keys(), index=graph.keys())
    for u, v_list in graph.items():
        for i in v_list:
            result[u][i] = 1

    return result


#将原始的用户行为数据转化为标准化的矩阵格式
def raw2std(raw_data,index=None):
    mid_data = DataFrame(raw_data)
    if isinstance(mid_data[mid_data.columns[0]][mid_data.index[0]], (numpy.int64, numpy.float64)):
        if index:
            result = DataFrame(raw_data, index=index)
        else:
            result = DataFrame(raw_data)
    elif isinstance(mid_data[mid_data.columns[0]][mid_data.index[0]], str):
        result = list2matrix(raw_data)
    else:
        raise TypeError("not support data formart")

    return result


# 获得用户对哪些物品产生过行为
# 将用户-物品表格转换为用户-物品-行为矩阵（0或1）
def list2matrix(raw_data):
    columns = []
    index = []
    for u, v_list in raw_data.items():
        if u in columns:
            pass
        else:
            columns.append(u)
        for v in v_list:
            if v in index:
                pass
            else:
                index.append(v)

    result = DataFrame(index= index, columns= columns)

    for u, v_list in raw_data.items():
        for i in index:
            if i in v_list:
                result[u][i] = 1
            else:
                result[u][i] = 0

    return result


#这个地方专管三元组的转换
def list2dataframe_time(train, columns= None, index= None):
    #todo:这个地方不太好写啊
    #todo:1要对多种数据进行处理
    #todo:2决定好到底要使用什么形式的矩阵
    #列表套列表
    if (not index) and (not columns):
        columns, index = get_columns_and_index(train)
    elif not columns:
        columns = get_columns_and_index(train)[0]
    elif not index:
        index = get_columns_and_index(train)[1]

    #单矩阵方案
    user_item_time = DataFrame(index=index, columns=columns)
    for a in train:
        u=a[0]
        i=a[1]
        t=a[2]
        user_item_time[u][i] = t
    return user_item_time

#todo:该函数以来具体的数据格式
#将数据集拆分成训练集和测试集的过程
def SplitData(data, M=10, k=1):
    test = []
    train = []
    for i in data:
        if random.randint(0,M) <= k:
            #randint随机生成0~M之间的数
            test.append(i)
        else:
            train.append(i)
    return train, test