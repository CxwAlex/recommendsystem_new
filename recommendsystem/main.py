import numpy
from pandas import Series, DataFrame
from collections import defaultdict
import random
import math

#实际上的多引擎并不单单只是指算法上的多引擎，更多的是指在业务上的：
#比如专门负责冷启动的，专门负责重点广告业务的等，即常见的浏览器中其他文章+广告的模式

#推荐系统核心模块，处理的是特征维度，而不仅仅是简单的行为、矩阵、图
#对单一用户的推荐+推荐理由

#todo:分成两部分，第一部分对单个用户进行推荐，第二部分对整个矩阵进行推荐

def ETL(raw_data, raw_schema, result_schema):
    return None

def RecommendationCore(train,user,):
    recommendation = {}
    recommendation.add()
    #基于用户行为的推荐系统CF推荐系统引擎使用
    #recommend1 = RecommendUserCF(train, user=None, k=1, N=1, similarity=None, sort=True)
    #recommend2 = RecommendItemCF(train, user=None, k=1, N=1, similarity=None, sort=True)

    #基于社交网络的推荐系统的使用
    #recommend3 = RecommendSocial(dataframe_social, dataframe_item, user=None, N=1)
    #推荐朋友
    #frend = FriendSuggestion(dataframe, user=None, N=1, filter=True)

    #基于标签的推荐系统
    #recommend4 = RecommendByTags(user_item_tags, user=None, N=1)
    #给用户推荐标签
    #tags = RecommendTags(user_item_tag, user=None, item=None, tag=None, alpha=0.3, N=1)

    #基于时间上下文的推荐系统
    #recommend5 = RecommendItemSimilarityTime(train, user=None, k=1, N=1, alpha_item_similarity=1.0, alpha_item_item=1.0, t0=0)
    #recommend6 = RecommendUserSimilarityTime(train, user=None, k=1, N=1, alpha_user_similarity=1.0, alpha_user_item=1.0, t0=0)

    #一些常用的推荐系统
    #最热门推荐
    #
    #最近最热门推荐
    #
    #冷启动物品的推荐
    #
    #出于广告目的的推荐
    #

    return recommendation


def Filter(train, recommendation, user=None):
    for recommend in recommendation:
        for i in recommend:
            if train[user][i] != 0:
                recommend.drop(i)

    return recommendation


def Sort(recommendation, weight, user=None):
    for recommend in recommendation:
        for i in recommend:
            result[i] = wi * wengine
    result.sort
    return result

def Reason(recommendation,recommendation_after_sort):
    for i in recommendation_after_sort:
        result[i].addreason()
    return result_has_reason


if __name__ == '__main__':
    train = ETL()
    recommendation = RecommendationCore()
    recommendation_after_filter = Filter(recommendation)
    result = Sort(recommendation_after_filter)
    result_has_reason = Reason(result)

    print(result_has_reason)
