import os
from recommendsystem.ETL import MovieLensRatings2Dataframe, WriteLog
from recommendsystem.utils import SplitData
from recommendsystem.assessment import Summary
from recommendsystem.engine_cf import *
from recommendsystem.engine_common import *
from recommendsystem.engine_time import *
from recommendsystem.engine_tags import *
from recommendsystem.engine_social import *

#主要分为以下几个功能：
def TrainAndTestWorkflow(dataframe, recommend_engine, user=None, parameters=None, train_test_ratio=9, repeat_k=1):
    result = []
    for i in range(repeat_k):
        train, test = SplitData(dataframe, M=train_test_ratio+1, k=1)
        recommend = RecommendAndParameter(recommend_engine, train, user, parameters)
        summary = Summary(train, recommend, test, item_similarity=None)
        result.append(summary)
        result_str = recommend_engine + '第' + str(i) + '次训练结果：'
        result[i] = {result_str: summary}

        num = Result2Log(result[i], recommend_engine)

        print(result)
        if num:
            print('写入成功', num)
        else:
            print('写入失败')

    return result


def RecommendAndParameter(recommend_engine, train, user=None, parameters=None):
    if recommend_engine == 'RecommendUserCF':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)


    elif recommend_engine == 'RecommendItemCF':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)
    elif recommend_engine == 'RecommendSocial':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)

    elif recommend_engine == 'RecommendByTags':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)


    elif recommend_engine == 'RecommendItemSimilarityTime':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)


    elif recommend_engine == 'RecommendUserSimilarityTime':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)


    elif recommend_engine == 'RecommendMostHot':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)


    elif recommend_engine == 'RecommendColdStartItem':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)


    elif recommend_engine == 'RecommendRandom':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    recommend = RecommendUserCF(train, user=user, k=k, N=N)

    return recommend

def Result2Log(result, recommend_engine):
    pwd = os.getcwd()
    project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
    filepath = project_filepath + '/Log/' + recommend_engine + '.log'
    num = WriteLog(result, filepath)

    return num


def TrainAndTest():
    return None


def TestParameter(parameter):
    return None



#分割数据集

#对不同的数据集，采用不同的模型进行训练

#所有模型训练后一起评估