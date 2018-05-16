import os
import datetime
from conf.settings import *
from recommendsystem.ETL import *
from recommendsystem.utils import SplitData
from recommendsystem.assessment import Summary
from recommendsystem.engine_cf import *
from recommendsystem.engine_common import *
from recommendsystem.engine_time import *
from recommendsystem.engine_tags import *
from recommendsystem.engine_social import *

#主要分为以下几个功能：
def TrainAndTestWorkflow(filepath, recommend_engine_name, dataset_name, user=None, parameters=None, train_test_ratio=9, repeat_k=1):
    #首先读入信息并获得标准数据data_std（这一步要根据不同的数据集的特点来修改）
    data_std = MovieLensRatings2Std(filepath)

    #获取不同的参数设定
    parameters = getparaters(dataset_name, recommend_engine_name)

    #开始训练&写结果
    RecommendAndParameter(data_std, 'RecommendUserCF', repeat_k=10)

    return None


def RecommendAndParameter(data_std, recommend_engine, user=None, parameters=None, train_test_ratio=9, repeat_k=1):
    #以下写法是代码简洁版，但是在效率上较差
    WriteEngineToLog(recommend_engine)
    if recommend_engine == 'RecommendUserCF':
        if parameters:
            for k in parameters['k']:
                for similarity in parameters['similarity']:
                    for N in parameters['N']:
                        result_str = 'setting: k=' + str(k) + ', N=' + str(N) + ', similarity=' + similarity
                        WriteParameterSettingToLog(result_str, recommend_engine)
                        for i in range(repeat_k):
                            train, test = DataStd2Dataframe(data_std, train_test_ratio)
                            recommend = RecommendUserCF(train, user=user, k=k, N=N, similarity=similarity)
                            summary = Summary(train, recommend, test, item_similarity=None)
                            WriteSummaryToLog(summary, i, recommend_engine)
        else:
            for i in range(repeat_k):
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                recommend = RecommendUserCF(train, user)
                summary = Summary(train, recommend, test, item_similarity=None)
                WriteSummaryToLog(summary, i, recommend_engine)

    elif recommend_engine == 'RecommendItemCF':
        if parameters:
            for k in parameters['k']:
                for similarity in parameters['similarity']:
                    for N in parameters['N']:
                        result_str = 'setting: k=' + str(k) + ', N=' + str(N) + ', similarity=' + similarity
                        WriteParameterSettingToLog(result_str, recommend_engine)
                        for i in range(repeat_k):
                            train, test = DataStd2Dataframe(data_std, train_test_ratio)
                            recommend = RecommendItemCF(train, user=user, k=k, N=N, similarity=similarity)
                            summary = Summary(train, recommend, test, item_similarity=None)
                            WriteSummaryToLog(summary, i, recommend_engine)
        else:
            for i in range(repeat_k):
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                recommend = RecommendItemCF(train, user)
                summary = Summary(train, recommend, test, item_similarity=None)
                WriteSummaryToLog(summary, i, recommend_engine)
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
                for i in repeat_k:
                    train, test = DataStd2Dataframe(data_std, train_test_ratio)
                    recommend = RecommendRandom(train, N)
                    summary = Summary(train, recommend, test, item_similarity=None)
                    WriteSummaryToLog(summary, i, recommend_engine)

    return None


def RecommendAndParameterHighSpeed(data_std, recommend_engine, user=None, parameters=None, train_test_ratio=9, repeat_k=1):
    #以下写法把每个推荐引擎拆开来，对其可重复利用的部分进行重复利用
    WriteEngineToLog(recommend_engine)
    if recommend_engine == 'RecommendUserCF':
        if parameters:
            for similarity in parameters['similarity']:
                for i in range(repeat_k):
                    train, test = DataStd2Dataframe(data_std, train_test_ratio)
                    user_similarity = GetUserSimilarity(similarity)
                    for k in parameters['k']:
                        rank = GetRankUserCF(train, user, k, user_similarity)
                        for N in parameters['N']:
                            result_str = 'setting: k=' + str(k) + ', N=' + str(N) + ', similarity=' + similarity
                            WriteParameterSettingToLog(result_str, recommend_engine)
                            recommend = FilterAndSort(train, rank, user, N)
                            summary = Summary(train, recommend, test, item_similarity=None)
                            WriteSummaryToLog(summary, i, recommend_engine)
        else:
            for i in range(repeat_k):
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                recommend = RecommendUserCF(train, user)
                summary = Summary(train, recommend, test, item_similarity=None)
                WriteSummaryToLog(summary, i, recommend_engine)
    elif recommend_engine == 'RecommendItemCF':
        if parameters:
            for similarity in parameters['similarity']:
                for i in range(repeat_k):
                    train, test = DataStd2Dataframe(data_std, train_test_ratio)
                    item_similarity = GetItemSimilarity(similarity)
                    for k in parameters['k']:
                        rank = GetRankItemCF(train, user, k, item_similarity)
                        for N in parameters['N']:
                            result_str = 'setting: k=' + str(k) + ', N=' + str(N) + ', similarity=' + similarity
                            WriteParameterSettingToLog(result_str, recommend_engine)
                            recommend = FilterAndSort(train, rank, user, N)
                            summary = Summary(train, recommend, test, item_similarity=None)
                            WriteSummaryToLog(summary, i, recommend_engine)
        else:
            for i in range(repeat_k):
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                recommend = RecommendItemCF(train, user)
                summary = Summary(train, recommend, test, item_similarity=None)
                WriteSummaryToLog(summary, i, recommend_engine)
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
                for i in repeat_k:
                    train, test = DataStd2Dataframe(data_std, train_test_ratio)
                    recommend = RecommendRandom(train, N)
                    summary = Summary(train, recommend, test, item_similarity=None)
                    WriteSummaryToLog(summary, i, recommend_engine)

    return None


def DataStd2Dataframe(data_std, train_test_ratio):
    #该模块需要根据实际需求修改
    #这里的功能是先按照需求分割为训练集和测试集，再讲训练集转换为dataframe后返回
    train_raw, test = SplitData(data_std, M=train_test_ratio + 1, k=1)
    train = MovieLensStd2Dataframe(train_raw)

    return train, test


def WriteEngineToLog(recommend_engine):
    date = datetime.datetime.now()

    num0 = Result2Log('engine_start_time'+str(date), recommend_engine)
    num1 = Result2Log(recommend_engine, recommend_engine)

    print(recommend_engine)
    print('start_time', date)
    return num1


def WriteParameterSettingToLog(result_str2, recommend_engine):
    date = datetime.datetime.now()
    num0 = Result2Log('new_setting_start_time'+str(date), recommend_engine)
    num2 = Result2Log(result_str2, recommend_engine)
    print(result_str2)

    return num2


def WriteSummaryToLog(summary, i, recommend_engine):
    date = datetime.datetime.now()
    num0 = Result2Log('' + str(date), recommend_engine)
    result_str3 = '第' + str(i) + '次训练结果：'
    result_summary = result_str3 + str(summary)
    print(result_summary)
    num3 = Result2Log(result_summary, recommend_engine)

    return num3


def Result2Log(result, recommend_engine='default'):
    pwd = os.path.split(os.path.realpath(__file__))[0]
    project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    filepath = project_filepath + '/Log/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filepath += recommend_engine + '.log'
    num = WriteLog(result, filepath)

    return num