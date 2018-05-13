#此章主要用来补充一些不需要用到推荐逻辑的推荐引擎
import random
import datetime
from pandas import Series
from recommendsystem.utils import count_set

#最热门推荐
def RecommendMostHot(dataframe, N=1, type='day', date_now=None):
    if type == 'day':
        result = RecommendMostHotDay(dataframe, N, date_now)
    elif type == 'week':
        result = RecommendMostHotWeek(dataframe, N, date_now)
    elif type == 'month':
        result = RecommendMostHotMonth(dataframe, N, date_now)
    elif type == 'ever':
        result = RecommendMostHotEver(dataframe, N, date_now)
    else:
        return None
    return result


def RecommendMostHotEver(dataframe, N=1):
    result = Series(index=dataframe.index)
    for i in dataframe.index:
        result[i] = count_set(dataframe.ix[i])

    result = result.sort_values(ascending=False).index[0:N]

    return result


#todo:最近最热门如何实现：是在数据选入阶段只选择最近24小时
#todo:周排行榜和月排行榜
#最近最热门推荐算法
#推荐当日还是24小时内？此处仅推荐当日最火
def RecommendMostHotDay(dataframe, N=1, date_now=None):
    if not date_now:
        date_now = datetime.datetime.now().date()
    else:
        date_now = datetime.datetime.strptime(date_now,'%Y-%m-%d').date()

    result = Series(0, index=dataframe.index)
    for u in dataframe.columns:
        for i in dataframe.index[dataframe[u].notnull()]:
            date_item = datetime.datetime.strptime(dataframe[u][i], '%Y-%m-%d').date()

            if date_item == date_now:
                result[i] += 1

    return result.sort_values(ascending=False).index[0:N]


def RecommendMostHotWeek(dataframe, N=1, date_now=None):
    if not date_now:
        date_now = datetime.datetime.now().date()
    else:
        date_now = datetime.datetime.strptime(date_now,'%Y-%m-%d').date()

    date_start = date_now + datetime.timedelta(-7)
    result = Series(0, index=dataframe.index)
    for u in dataframe.columns:
        for i in dataframe.index[dataframe[u].notnull()]:
            date_item = datetime.datetime.strptime(dataframe[u][i], '%Y-%m-%d').date()
            if date_item >= date_start and date_item < date_now:
                result[i] += 1

    return result.sort_values(ascending=False).index[0:N]


def RecommendMostHotMonth(dataframe, N=1, date_now=None):
    if not date_now:
        date_now = datetime.datetime.now().date()
    else:
        date_now = datetime.datetime.strptime(date_now,'%Y-%m-%d').date()

    date_start = date_now + datetime.timedelta(-30)
    result = Series(0, index=dataframe.index)
    for u in dataframe.columns:
        for i in dataframe.index[dataframe[u].notnull()]:
            date_item = datetime.datetime.strptime(dataframe[u][i], '%Y-%m-%d').date()
            if date_item >= date_start and date_item < date_now:
                result[i] += 1

    return result.sort_values(ascending=False).index[0:N]


#随机推荐引擎
def RecommendRandom(items, N=1):
    result = random.sample(items, N)
    return result


# 冷启动物品的推荐——即新物品的推荐
def RecommendColdStartItem(cold_items, N=1):
    #每次随机推荐，对于同一个物品，推荐次数到达一定程度或者点击量到达一定程度之后从冷启动名单中删去
    result = RecommendRandom(cold_items, N)
    #todo:因为点击量要靠后台统计，所以此处仅对展示量进行统计

    return result


#最新推荐
def RecommendNew(new_items, N=1):
    return None


# 出于广告目的的推荐——对特定物品集的推荐
def RecommendADs(ad_items, N=1):
    #根据广告原则决定展出顺序
    return None