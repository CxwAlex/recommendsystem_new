from recommendsystem.ETL import MovieLensRatings2Dataframe
from recommendsystem.utils import SplitData
from recommendsystem.engine_cf import *
from recommendsystem.engine_common import *
from recommendsystem.engine_time import *
from recommendsystem.engine_tags import *
from recommendsystem.engine_social import *

def ETL(raw_data, raw_schema, result_schema):
    return None

def RecommendationCore(train,user,):
    #基于用户行为的推荐系统CF推荐系统引擎使用
    #recommend1 = RecommendUserCF(train, user=None, k=1, N=1, similarity=None, sort=True)
    #recommend2 = RecommendItemCF(train, user=None, k=1, N=1, similarity=None, sort=True)

    #基于社交网络的推荐系统的使用
    #recommend3 = RecommendSocial(dataframe_social, dataframe_item, user=None, k=1, N=1)
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
    #recommend7 = RecommendMostHot(dataframe, N=1, type='day', date_now=None)
    #分为当日最热门（day），一周(week)，一年(year)和所有记录（ever）

    #冷启动物品的推荐
    #仅针对新物品或者冷门物品推荐
    #recommend8 = RecommendColdStartItem(cold_items, N=1)
    #出于广告目的的推荐
    #recommend9 = RecommendADs(ad_items, N=1)

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
            continue
            #result[i] = wi * wengine
    #result.sort
    return None

def Reason(recommendation,recommendation_after_sort):
    for i in recommendation_after_sort:
        result[i].addreason()
    return result_has_reason


if __name__ == '__main__':
    #此处先对MovieLens的1M数据集进行测试，现阶段只考虑用户是否会对某部电影评分，而不考虑分数值
    #使用的推荐引擎：随机、基于用户相似度、基于物品相似度、基于人口统计学的用户相似度，基于时间上下文的推荐

    train = ETL()
    recommendation = RecommendationCore()
    recommendation_after_filter = Filter(recommendation)
    result = Sort(recommendation_after_filter)
    result_has_reason = Reason(result)

    print(result_has_reason)
