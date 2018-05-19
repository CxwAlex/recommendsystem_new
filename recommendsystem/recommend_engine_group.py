import os
import datetime
import time
from conf.settings import *
from recommendsystem.ETL import *
from recommendsystem.utils import SplitData
from recommendsystem.assessment import Summary
from recommendsystem.engine_cf import *
from recommendsystem.engine_common import *
from recommendsystem.engine_tags import *
from recommendsystem.engine_social import *
from recommendsystem.engine_user_property import *
from recommendsystem.TrainAndTestWorkflow import DataStd2Dataframe, WriteSummaryToLog


def RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_user=None, data_std_item=None, user=None, parameters=None, train_test_ratio=9, repeat_k=1):
    #以下写法把每个推荐引擎拆开来，对其可重复利用的部分进行重复利用
    if recommend_engine == 'RecommendUserCF&UserProperty_similarity':
        for i in range(repeat_k):
            t0 = time.clock()
            train, test = DataStd2Dataframe(data_std, train_test_ratio)
            t1 = time.clock()
            time_stddata = t1 - t0

            item_similarity = GetUserSimilarity(train)
            t2 = time.clock()
            time_item_similarity = t2 - t1

            weight = parameters['weight']
            user_similarity_property = UserSimilarityProperty(data_std_user, weight)
            t3 = time.clock()
            time_user_similarity_property = t3 - t2

            similarity = parameters['similarity']
            user_similarity = GetUserSimilarity(train, similarity)
            t4 = time.clock()
            time_user_similarity = t4 - t3

            user_similarity += user_similarity_property

            for k in parameters['k']:
                t5 = time.clock()
                rank = GetRankUserCF(train, user, k, user_similarity)
                t6 = time.clock()
                time_rank = t6 - t5


                N = parameters['N']
                log_name = recommend_engine + "_k=" + str(k) + '_N=' + str(N) + '_similarity=' + similarity
                t7 = time.clock()
                recommend = FilterAndSort(train, rank, user, N)
                t8 = time.clock()
                time_recommend = t8 - t7

                summary, spendtime_summary = Summary(train, recommend, test, item_similarity)
                t9 = time.clock()
                time_summary = t9 - t8
                time_all = {'time_stddata': time_stddata, 'time_item_similarity': time_item_similarity, 'time_user_similarity_property': time_user_similarity_property, 'time_user_similarity': time_user_similarity, 'time_rank': time_rank, 'time_recommend': time_recommend, 'time_summary': time_summary}
                WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)

    elif recommend_engine == 'RecommendUserCF&UserProperty_rank':
        for i in range(repeat_k):
            t0 = time.clock()
            train, test = DataStd2Dataframe(data_std, train_test_ratio)
            t1 = time.clock()
            time_stddata = t1 - t0

            item_similarity = GetItemSimilarity(train)
            t2 = time.clock()
            time_item_similarity = t2 - t1

            if parameters:
                for weight in parameters['weight']:
                    t3 = time.clock()
                    user_similarity = UserSimilarityProperty(data_std_user, weight)
                    t4 = time.clock()
                    time_user_similarity = t4 - t3

                    for k in parameters['k']:
                        t5 = time.clock()
                        rank = GetRankUserCF(train, user, k, user_similarity)
                        t6 = time.clock()
                        time_rank = t6 - t5

                        for N in parameters['N']:
                            t7 = time.clock()
                            recommend = FilterAndSort(train, rank, user, N)
                            t8 = time.clock()
                            time_recommend = t8 - t7

                            log_name = recommend_engine + "_k=" + str(k) + '_N=' + str(N) + '_weight=' + str(weight)

                            summary, spendtime_summary = Summary(train, recommend, test, item_similarity)
                            t9 = time.clock()
                            time_summary = t9 - t8

                            time_all = {'time_stddata': time_stddata, 'time_item_similarity': time_item_similarity, 'time_user_similarity': time_user_similarity,  'time_rank': time_rank, 'time_recommend': time_recommend, 'time_summary': time_summary}
                            WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)

    elif recommend_engine == 'RecommendUserCF&ItemCF_rank':
        for i in range(repeat_k):
            t0 = time.clock()
            train, test = DataStd2Dataframe(data_std, train_test_ratio)
            t1 = time.clock()
            time_stddata = t1 - t0

            if parameters:
                for similarity in parameters['similarity']:
                    t2 = time.clock()
                    item_similarity = GetItemSimilarity(train, similarity)
                    t3 = time.clock()
                    time_similarity = t3 - t2

                    for k in parameters['k']:
                        t4 = time.clock()
                        rank = GetRankItemCF(train, user, k, item_similarity)
                        t5 = time.clock()
                        time_rank = t5 - t4

                        for N in parameters['N']:
                            log_name = recommend_engine + "_k=" + str(k) + '_N=' + str(N) + '_similarity=' + similarity

                            t5 = time.clock()
                            recommend = FilterAndSort(train, rank, user, N)
                            t6 = time.clock()
                            time_recommend = t6 - t5

                            summary, spendtime_summary = Summary(train, recommend, test, item_similarity)
                            t7 = time.clock()
                            time_summary = t7 - t6
                            time_all = {'time_stddata': time_stddata, 'time_similarity': time_similarity, 'time_rank': time_rank, 'time_recommend': time_recommend, 'time_summary': time_summary}
                            WriteSummaryToLog(log_name, time_all, summary, spendtime_summary, i)



    return None