import os
import datetime
import time
from conf.settings import *
from recommendsystem.ETL import *
from recommendsystem.utils import SplitData
from recommendsystem.assessment import Summary
from recommendsystem.engine_cf import *
from recommendsystem.engine_common import *
from recommendsystem.engine_time import *
from recommendsystem.engine_tags import *
from recommendsystem.engine_social import *
from recommendsystem.engine_user_property import *

#主要分为以下几个功能：
def TrainAndTestWorkflow(filepath, user_filepath, item_filepath, recommend_engine_name, dataset_name, user=None, parameters=None, train_test_ratio=9, repeat_k=1):
    #首先读入信息并获得标准数据data_std（这一步要根据不同的数据集的特点来修改）
    data_std = MovieLensRatings2Std(filepath)
    data_std_user = MovieLensRatings2Std(user_filepath)
    data_std_item = MovieLensRatings2Std(item_filepath)

    #获取不同的参数设定
    parameters = getparaters(dataset_name, recommend_engine_name)

    #开始训练&写结果
    RecommendAndParameterHighSpeed(data_std, 'RecommendUserCF', repeat_k=10)

    return None


def RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_user=None, data_std_item=None, user=None, parameters=None, train_test_ratio=9, repeat_k=1):
    #以下写法把每个推荐引擎拆开来，对其可重复利用的部分进行重复利用
    if recommend_engine == 'RecommendUserCF':
        if parameters:
            for similarity in parameters['similarity']:
                for i in range(repeat_k):
                    t0 = time.clock()
                    train, test = DataStd2Dataframe(data_std, train_test_ratio)
                    t1 = time.clock()
                    time_stddata = t1 - t0

                    user_similarity = GetUserSimilarity(train, similarity)
                    t2 = time.clock()
                    time_similarity = t2 - t1

                    for k in parameters['k']:
                        rank = GetRankUserCF(train, user, k, user_similarity)
                        for N in parameters['N']:
                            log_name = recommend_engine + "_k=" + str(k) + '_N=' + str(N) + '_similarity=' + similarity
                            recommend = FilterAndSort(train, rank, user, N)
                            t3 = time.clock()
                            time_recommend = t3 - t2

                            summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                            t4 = time.clock()
                            time_summary = t4 - t3
                            time_all = {'time_stddata': time_stddata, 'time_similarity': time_similarity, 'time_recommend': time_recommend, 'time_summary': time_summary}
                            WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)
        else:
            for i in range(repeat_k):
                t0 = time.clock()
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                t1 = time.clock()
                time_stddata = t1 - t0

                recommend = RecommendUserCF(train, user)
                t2 = time.clock()
                time_recommend = t2 - t1

                summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                t3 = time.clock()
                time_summary = t3 - t2

                log_name = recommend_engine
                time_all = {'time_stddata': time_stddata, 'time_recommend': time_recommend, 'time_summary': time_summary}
                WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)

    elif recommend_engine == 'RecommendItemCF':
        if parameters:
            for similarity in parameters['similarity']:
                for i in range(repeat_k):
                    t0 = time.clock()
                    train, test = DataStd2Dataframe(data_std, train_test_ratio)
                    t1 = time.clock()
                    time_stddata = t1 - t0

                    item_similarity = GetItemSimilarity(train, similarity)
                    t2 = time.clock()
                    time_similarity = t2 - t1

                    for k in parameters['k']:
                        rank = GetRankItemCF(train, user, k, item_similarity)
                        for N in parameters['N']:
                            log_name = recommend_engine + "_k=" + str(k) + '_N=' + str(N) + '_similarity=' + similarity

                            recommend = FilterAndSort(train, rank, user, N)
                            t3 = time.clock()
                            time_recommend = t3 - t2

                            summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                            t4 = time.clock()
                            time_summary = t4 - t3
                            time_all = {'time_stddata': time_stddata, 'time_similarity': time_similarity,'time_recommend': time_recommend, 'time_summary': time_summary}
                            WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)
        else:
            for i in range(repeat_k):
                t0 = time.clock()
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                t1 = time.clock()
                time_stddata = t1 - t0

                recommend = RecommendItemCF(train, user)
                t2 = time.clock()
                time_recommend = t2 - t1

                summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                t3 = time.clock()
                time_summary = t3 - t2

                log_name = recommend_engine
                time_all = {'time_stddata': time_stddata, 'time_recommend': time_recommend, 'time_summary': time_summary}
                WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)

    elif recommend_engine == 'RecommendPersonalRank':
        t0 = time.clock()
        train, test = DataStd2Dataframe(data_std, train_test_ratio)
        t1 = time.clock()
        time_stddata = t1 - t0

        if parameters:
            for p in parameters['p']:
                for repeat_times in parameters['repeat_times']:

                    rank = PersonalRank(train, user, p=p, repeat_times=repeat_times)
                    t2 = time.clock()
                    time_rank = t2 - t1

                    for N in parameters['N']:
                        t2 = time.clock()
                        recommend = FilterAndSort(train, rank, user, N)
                        t3 = time.clock()
                        time_recommend = t3 - t2

                        log_name = recommend_engine + "_p=" + str(p) + '_repeat_times=' + str(repeat_times) + '_N=' + str(N)

                        summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                        t4 = time.clock()
                        time_summary = t4 - t3

                        time_all = {'time_stddata': time_stddata, 'time_rank': time_rank, 'time_recommend': time_recommend, 'time_summary': time_summary}
                        WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i=1)
        else:
            for i in range(repeat_k):
                t0 = time.clock()
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                t1 = time.clock()
                time_stddata = t1 - t0

                rank = PersonalRank(train, user)
                t2 = time.clock()
                time_rank = t2 - t1

                recommend = FilterAndSort(train, rank, user, N=1)
                t3 = time.clock()
                time_recommend = t3 - t2

                summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                t4 = time.clock()
                time_summary = t4 - t2

                log_name = recommend_engine
                time_all = {'time_stddata': time_stddata, 'time_rank': time_rank, 'time_recommend': time_recommend, 'time_summary': time_summary}
                WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)

    elif recommend_engine == 'RecommendUserProperty':
        if parameters:
            for weight in parameters['weight']:
                t0 = time.clock()
                user_similarity = UserSimilarityProperty(data_std_user, weight)
                t1 = time.clock()
                time_similarity = t1 - t0

                for k in parameters['k']:
                    for i in range(repeat_k):
                        t1 = time.clock()
                        train, test = DataStd2Dataframe(data_std, train_test_ratio)
                        t2 = time.clock()
                        time_stddata = t2 - t1

                        rank = GetRankUserCF(train, user, k, user_similarity)
                        t3 = time.clock()
                        time_rank = t3 - t2
                        for N in parameters['N']:
                            t4 = time.clock()
                            recommend = FilterAndSort(train, rank, user, N)
                            t5 = time.clock()
                            time_recommend = t5 - t4

                            log_name = recommend_engine + "_k=" + str(k) + '_N=' + str(N) + '_weight=' + str(weight)

                            summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                            t6 = time.clock()
                            time_summary = t6 - t5

                            time_all = {'time_similarity': time_similarity, 'time_stddata': time_stddata, 'time_rank': time_rank, 'time_recommend': time_recommend, 'time_summary': time_summary}
                            WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i=1)
        else:
            for i in range(repeat_k):
                t0 = time.clock()
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                t1 = time.clock()
                time_stddata = t1 - t0

                rank = PersonalRank(train, user)
                t2 = time.clock()
                time_rank = t2 - t1

                recommend = FilterAndSort(train, rank, user, N=1)
                t3 = time.clock()
                time_recommend = t3 - t2

                summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                t4 = time.clock()
                time_summary = t4 - t2

                log_name = recommend_engine
                time_all = {'time_stddata': time_stddata, 'time_rank': time_rank, 'time_recommend': time_recommend, 'time_summary': time_summary}
                WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)


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
        t0 = time.clock()

        data_all = MovieLensStd2Dataframe(data_std)
        t1 = time.clock()
        time_stddata = t1 - t0

        print('start_similarity')
        item_similarity = GetItemSimilarity(data_all)
        t2 = time.clock()
        time_similarity = t2 - t1
        print('end_similarity', time_similarity)

        if parameters:
            for N in parameters['N']:
                log_name = recommend_engine + '_N=' + str(N)
                result_str = 'setting: N=' + str(N)
                for i in range(repeat_k):
                    t2 = time.clock()
                    recommend = DataFrame(columns=data_all.columns, index=range(N))
                    for u in data_all.columns:
                        recommend[u] = RecommendRandom(list(data_all.index), N)
                    t3 = time.clock()
                    time_recommend = t3 - t2

                    summary, spendtime_summary = Summary(data_all, recommend, data_all, item_similarity)
                    t4 = time.clock()
                    time_summary = t4 - t3

                    time_all = {'time_stddata': time_stddata, 'time_similarity': time_similarity, 'time_recommend': time_recommend, 'time_summary': time_summary}
                    WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)

    return None


def DataStd2Dataframe(data_std, train_test_ratio):
    #该模块需要根据实际需求修改
    #这里的功能是先按照需求分割为训练集和测试集，再讲训练集转换为dataframe后返回
    train_raw, test_raw = SplitData(data_std, M=train_test_ratio + 1, k=1)
    train = MovieLensStd2Dataframe(train_raw)
    test = MovieLensStd2Dataframe(test_raw)

    return train, test


def WriteSummaryToLog(log_name, time_all, summary, time_summary, i):
    date = datetime.datetime.now()
    result_str3 = '第' + str(i) + '次训练结果：'
    result_summary = result_str3 + str(summary)
    print(time_all)
    print(result_summary)
    print(time_summary)
    num0 = Result2Log(log_name, '' + str(date))
    num1 = Result2Log(log_name, time_all)
    num2 = Result2Log(log_name, result_summary)
    num3 = Result2Log(log_name, time_summary)

    return num3


def Result2Log(log_name, result):
    pwd = os.path.split(os.path.realpath(__file__))[0]
    project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
    filepath = project_filepath + '/Log/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filepath += log_name + '.log'
    num = WriteLog(result, filepath)

    return num


'''

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
                            t0 = time.clock()
                            train, test = DataStd2Dataframe(data_std, train_test_ratio)
                            t1 = time.clock()
                            time_stddata = t1 - t0

                            recommend = RecommendUserCF(train, user=user, k=k, N=N, similarity=similarity)
                            t2 = time.clock()
                            time_recommend = t2 - t1

                            summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                            t3 = time.clock()
                            time_summary = t3 - t2

                            time_all = {'time_stddata':time_stddata, 'time_recommend':time_recommend, 'time_summary':time_summary}
                            WriteSummaryToLog(time_all, summary, spendtime_summary, i, recommend_engine)

        else:
            for i in range(repeat_k):
                t0 = time.clock()
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                t1 = time.clock()
                time_stddata = t1 - t0

                recommend = RecommendUserCF(train, user)
                t2 = time.clock()
                time_recommend = t2 - t1

                summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                t3 = time.clock()
                time_summary = t3 - t2

                time_all = {'time_stddata': time_stddata, 'time_recommend': time_recommend, 'time_summary': time_summary}
                WriteSummaryToLog(time_all, summary, spendtime_summary, i, recommend_engine)

    elif recommend_engine == 'RecommendItemCF':
        if parameters:
            for k in parameters['k']:
                for similarity in parameters['similarity']:
                    for N in parameters['N']:
                        result_str = 'setting: k=' + str(k) + ', N=' + str(N) + ', similarity=' + similarity
                        WriteParameterSettingToLog(result_str, recommend_engine)
                        for i in range(repeat_k):
                            t0 = time.clock()
                            train, test = DataStd2Dataframe(data_std, train_test_ratio)
                            t1 = time.clock()
                            time_stddata = t1 - t0

                            recommend = RecommendItemCF(train, user=user, k=k, N=N, similarity=similarity)
                            t2 = time.clock()
                            time_recommend = t2 - t1

                            summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                            t3 = time.clock()
                            time_summary = t3 - t2

                            time_all = {'time_stddata': time_stddata, 'time_recommend': time_recommend, 'time_summary': time_summary}
                            WriteSummaryToLog(time_all, summary, spendtime_summary, i, recommend_engine)

        else:
            for i in range(repeat_k):
                t0 = time.clock()
                train, test = DataStd2Dataframe(data_std, train_test_ratio)
                t1 = time.clock()
                time_stddata = t1 - t0

                recommend = RecommendItemCF(train, user)
                t2 = time.clock()
                time_recommend = t2 - t1

                summary, spendtime_summary = Summary(train, recommend, test, item_similarity=None)
                t3 = time.clock()
                time_summary = t3 - t2

                time_all = {'time_stddata': time_stddata, 'time_recommend': time_recommend, 'time_summary': time_summary}
                WriteSummaryToLog(time_all, summary, spendtime_summary, i, recommend_engine)

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
        t0 = time.clock()

        data_all = MovieLensStd2Dataframe(data_std)
        t1 = time.clock()
        time_stddata = t1 - t0

        print('start_similarity')
        item_similarity = GetItemSimilarity(data_all)
        t2 = time.clock()
        time_similarity = t2 - t1
        print('end_similarity', time_similarity)


        if parameters:
            for N in parameters['N']:
                result_str = 'setting: N=' + str(N)
                WriteParameterSettingToLog(result_str, recommend_engine)
                for i in range(repeat_k):
                    t2 = time.clock()
                    recommend = DataFrame(columns=data_all.columns, index=range(N))
                    for u in data_all.columns:
                        recommend[u] = RecommendRandom(list(data_all.index), N)
                    t3 = time.clock()
                    time_recommend = t3 - t2

                    summary, spendtime_summary = Summary(data_all, recommend, data_all, item_similarity)
                    t4 = time.clock()
                    time_summary = t4 - t3

                    time_all = {'time_stddata': time_stddata, 'time_similarity': time_similarity, 'time_recommend': time_recommend, 'time_summary': time_summary}
                    WriteSummaryToLog(time_all, summary, spendtime_summary, i, recommend_engine)

    return None




'''