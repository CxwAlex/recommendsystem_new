import pickle
import os
from pandas import DataFrame
from recommendsystem.utils import get_columns_and_index



#数据读入模块
def ReadFile(filepath, mode="r", lines=None):

    with open(filepath, mode) as f:
        read_result = f.readlines()[0:lines]
        return read_result


def WriteFile(data, filepath, mode='w'):
    with open(filepath, mode) as f:
        if isinstance(data, str):
            num = f.write(data)
        else:
            str_data = str(data)
            num = f.write(str_data)

        f.write('\n')

    return num


def PickleReadFile(filepath):
    with open(filepath, 'rb') as input:
        data = pickle.load(input)
    return data


def PickleWriteFile(data, filepath):
    with open(filepath, 'wb') as output:
        pickle.dump(data, output)
    #dump() 与 load() 相比 dumps() 和 loads() 还有另一种能力：
    # dump()函数能一个接着一个地将几个对象序列化存储到同一个文件中
    # 随后调用load()来以同样的顺序反序列化读出这些对象。
    return None

def WriteLog(data=None, filepath=None, mode='a'):
    if not filepath:
        pwd = os.path.split(os.path.realpath(__file__))[0]
        project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
        filepath = project_filepath + '/Log'
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath += '/default.log'

    num = WriteFile(data, filepath, mode)
    return num


#############################
#以下是MovieLens数据的ETL
#############################

#适用于cf的数据集
def MovieLensRatings2Dataframe(filepath, lines=None, users=None, items=None):
    data_raw = ReadFile(filepath, lines=lines)
    data_std = []
    for i in data_raw:
        j = i.split('::')
        data_std.append(j)

    if not users and not items:
        user_std, item_std = get_columns_and_index(data_std)
    elif not users:
        user_std = get_columns_and_index(data_std)[0]
    elif not items:
        item_std = get_columns_and_index(data_std)[1]
    else:
        user_std = users
        item_std = items

    dataframe = DataFrame(0, columns=user_std, index=item_std)
    for i in data_std:
        dataframe[i[0]][i[1]] += int(i[2])

    return dataframe


def MovieLensRatings2Std(filepath, lines=None, users=None, items=None):
    data_raw = ReadFile(filepath, lines=lines)
    data_std = []
    for i in data_raw:
        j = i.split('::')
        data_std.append(j)

    return data_std

def MovieLensRatings2Std(filepath, lines=None, users=None, items=None):
    data_raw = ReadFile(filepath, lines=lines)
    data_std = []
    for i in data_raw:
        j = i.split('::')
        data_std.append(j)

    return data_std


def MovieLensUsers2Std(filepath, lines=None, users=None, items=None):
    data_std = MovieLensRatings2Std(filepath, lines, users, items)

    return data_std


def MovieLensMovies2Std(filepath, lines=None, users=None, items=None):
    data_std = MovieLensRatings2Std(filepath, lines, users, items)

    #return data_std


def MovieLensStd2Dataframe(data_std, users=None, items=None):
    if not users and not items:
        user_std, item_std = get_columns_and_index(data_std)
    elif not users:
        user_std = get_columns_and_index(data_std)[0]
    elif not items:
        item_std = get_columns_and_index(data_std)[1]
    else:
        user_std = users
        item_std = items

    dataframe = DataFrame(0, columns=user_std, index=item_std)
    for i in data_std:
        dataframe[i[0]][i[1]] += int(i[2])

    return dataframe

#三种主要结构的转换
def UserInformation():
    #具体情况具体实现
    return None

def ItemInformation():
    #具体情况具体实现
    return None

def UserAction():
    #具体情况具体实现
    return None



