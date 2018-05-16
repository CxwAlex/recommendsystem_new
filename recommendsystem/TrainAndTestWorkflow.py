import os
from conf.settings import Parameter
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
                    for similarity in parameters['similarity']:
                        recommend = RecommendUserCF(train, user=user, k=k, N=N, similarity=similarity)
        else:
            recommend = RecommendUserCF(train, user)
    elif recommend_engine == 'RecommendItemCF':
        if parameters:
            for k in parameters['k']:
                for N in parameters['N']:
                    for similarity in parameters['similarity']:
                        recommend = RecommendItemCF(train, user=user, k=k, N=N, similarity=similarity)
        else:
            recommend = RecommendItemCF(train, user)
    #social暂不使用，因为没有社交属性数据
    #elif recommend_engine == 'RecommendSocial':
    #   if parameters:
    #        for k in parameters['k']:
    #            for N in parameters['N']:
    #                recommend = RecommendSocial(dataframe_social, dataframe_item, user=None, k=k, N=N)
    #tags暂时不用
    #elif recommend_engine == 'RecommendByTags':
    #    if parameters:
    #        for N in parameters['N']:
    #            recommend = RecommendByTags(user_item_tags, user=None, N=N)
    #elif recommend_engine == 'RecommendItemSimilarityTime':
    #    if parameters:
    #        for k in parameters['k']:
    #            for N in parameters['N']:
    #                recommend = RecommendUserCF(train, user=user, k=k, N=N)
    #elif recommend_engine == 'RecommendUserSimilarityTime':
    #    if parameters:
    #        for k in parameters['k']:
    #            for N in parameters['N']:
    #                recommend = RecommendUserCF(train, user=user, k=k, N=N)
    #elif recommend_engine == 'RecommendMostHot':
    #    if parameters:
    #        for k in parameters['k']:
    #            for N in parameters['N']:
    #                recommend = RecommendUserCF(train, user=user, k=k, N=N)
    #elif recommend_engine == 'RecommendColdStartItem':
    #    if parameters:
    #        for k in parameters['k']:
    #            for N in parameters['N']:
    #                recommend = RecommendUserCF(train, user=user, k=k, N=N)
    elif recommend_engine == 'RecommendRandom':
        if parameters:
            for N in parameters['N']:
                if user:
                    recommend = RecommendRandom(train.index, N=N)
                else:
                    recommend = DataFrame(columns=train.columns)
                    for u in train.columns:
                        recommend[u] = RecommendRandom(train.index, N=N)

    return recommend

def Result2Log(result, recommend_engine):
    pwd = os.getcwd()
    project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
    filepath = project_filepath + '/Log/' + recommend_engine + '.log'
    num = WriteLog(result, filepath)

    return num