from recommendsystem.ETL import MovieLensRatings2Dataframe
from recommendsystem.utils import SplitData
from recommendsystem.assessment import Summary
from recommendsystem.engine_cf import *
from recommendsystem.engine_common import *
from recommendsystem.engine_time import *
from recommendsystem.engine_tags import *
from recommendsystem.engine_social import *

#主要分为以下几个功能：
def TrainAndTestWorkflow(dataframe, recommend_engines, train_test_ratio=9, repeat_k=1):
    for recommend_engine in recommend_engines:
        if recommend_engine == 'RecommendUserCF':
            for i in repeat_k:
                train, test = SplitData(dataframe, M=train_test_ratio+1, k=1)
                recommend = RecommendUserCF(train, user=None, k=1, N=1, similarity=None)
                summary = Summary(recommend, test)
                print(recommend_engine, '第', i, '次训练结果：')
                print(summary)




def TrainAndTest()


def TestParameter(parameter):
    return None



#分割数据集

#对不同的数据集，采用不同的模型进行训练

#所有模型训练后一起评估