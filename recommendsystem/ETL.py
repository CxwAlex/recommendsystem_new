import numpy
import random
from pandas import Series, DataFrame
from recommendsystem.utils import get_columns_and_index

#三种主要结构的转换
def UserInformation():
    return None

def ItemInformation():
    return None

def UserAction():
    return None


#其他的就是不同格式之间的转换

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
            result = DataFrame(raw_data, index= index)
        else:
            result = DataFrame(raw_data)
    elif isinstance(mid_data[mid_data.columns[0]][mid_data.index[0]], str):
        result = list2matrix(raw_data)
    else:
        raise TypeError("not support data formart")
    #todo：三元组格式给出的结果
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


#将数据集拆分成训练集和测试集的过程
def SplitData(data, M, k, seed=0):
    test = []
    train = []
    random.seed(seed)
    for user, item in data:
        if random.randint(0,M) <= k:
            #randint随机生成0~M之间的数
            test.append([user,item])
        else:
            train.append([user,item])
    return train, test

