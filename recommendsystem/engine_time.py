import math
import time
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from recommendsystem.utils import count_set_not_nan


#加入时间上下文后的基于物品的推荐
#todo:此处出错是因为N的计算错误，之前是非0计算，现在应该是非nan计算
#todo:此处考虑了时间的衰减项，却没有考虑热门物品的衰减
def ItemSimilarityTime(train, alpha_item_similarity=1.0):
    #calculate co-rated users between items
    C = DataFrame(0.0, index=train.index, columns=train.index)
    N = train.apply(func=count_set_not_nan, axis=1)
    for u in train.columns:
        items = train.index[train[u].notnull()]
        for i in items:
            for j in items:
                if i == j:
                    C[i][j] = 0
                    continue
                C[i][j] += 1 / (1 + alpha_item_similarity * abs(train[u][i] - train[u][j]))

    # calculate finial similarity matrix W
    W = DataFrame(0.0, index=train.index, columns=train.index)
    for i in train.index:
        for j in train.index:
            #归一化
            W[i][j] = (C[i][j] / math.sqrt(N[i] * N[j]))
    return W


#上面是基于同一个人喜欢的多个物品计算物品的相似度
#还可以使用喜欢两个物品共同人数的比例，但是在基于时间的这一假设下不好统计，因此放弃


#考虑时间因素后的用户相似度（对共同的兴趣引入时间衰减因子）
def UserSimilarityTime(train, alpha_user_similarity=1.0):
    #calculate co-rated items between users
    C = DataFrame(0.0, index=train.columns, columns=train.columns)
    for i in train.index:
        users = train.columns[train.ix[i].isnull() == False]
        for u in users:
            for v in users:
                if u == v:
                    continue
                C[u][v] += 1 / (1 + alpha_user_similarity * abs(train[u][i] - train[v][i]))
    #此处为直接使用user_item计算两者相似度
    w = DataFrame(index= train.columns, columns=train.columns)
    N = train.apply(func=count_set_not_nan, axis=0)

    for u in train.columns:
        for v in train.columns:
            #此处不判断，结果也是1，但是这样减少了后面乘除法的操作
            if u == v:
                w[u][v] = 0
                continue
            w[u][v] = C[u][v]/math.sqrt(N[u] * N[v] * 1.0)

    return w


def GetRankItemSimilarityTime(train, user=None, k=1, alpha_item_similarity=1.0, alpha_item_item=1.0, t0=0):
    #首先获得物品相似度矩阵
    item_similarity = ItemSimilarityTime(train, alpha_item_similarity)
    #对用户列表里的每一个物品，计算其相关物品的推荐结果
    if user:
        rank = Series(0.0, index=train.index)
        for j in train.index[train[user].isnull() == False]:
            for i in item_similarity[j].sort_values(ascending=False).index[0:k]:
                if not np.isnan(train[user][i]) or item_similarity[i][j] == 0:
                    continue
                else:
                    rank[i] += item_similarity[i][j] / (1 + alpha_item_item * abs(t0 - train[user][j]))
    else:
        rank = DataFrame(0.0, index=train.index, columns=train.columns)
        #u是目标用户，v是近邻用户，wuv是相似度
        #i是物品编号，rvi是v对i的兴趣
        for u in train.columns:
            for j in train.index[train[u].isnull() == False]:
                for i in item_similarity[j].sort_values(ascending=False).index[0:k]:
                    if not np.isnan(train[u][i]) or item_similarity[i][j] == 0:
                        continue
                    else:
                        rank[u][i] += item_similarity[i][j] / (1 + alpha_item_item * abs(t0 - train[u][j]))
    return rank


def GetRankUserSimilarityTime(train, user=None, k=1, alpha_user_similarity=1.0, alpha_user_item=1.0, t0=0):
    W = UserSimilarityTime(train, alpha_user_similarity)
    if user:
        rank = Series(0.0, index=train.index)
        for v in W[user].sort_values(ascending=False).index[0:k]:
            for i in train[v].index[train[v].isnull() == False]:
                if pd.isnull(train[user][i]) == False:
                    continue
                rank[i] += W[user][v] / (1 + alpha_user_item * (t0 - train[v][i]))
    else:
        rank = DataFrame(0.0, index=train.index, columns=train.columns)
        for u in train.columns:
            #print(u)
            for v in W[u].sort_values(ascending=False).index[0:k]:
                for i in train[v].index[train[v].isnull() == False]:
                    if pd.isnull(train[u][i]) == False:
                        continue
                    rank[u][i] += W[u][v] / (1 + alpha_user_item * (t0 - train[v][i]))
    return rank

def SortRank(rank, user=None, N=1):
    # 是否排序&是否TopN推荐
    if user:
        result = rank.sort_values(ascending=False).index[0:N]
    else:
        result = DataFrame(columns=rank.columns)
        for u in rank.columns:
            result[u] = rank[u].sort_values(ascending=False).index[0:N]

    return result

#加大用户最近行为比重的推荐算法
def RecommendItemSimilarityTime(train, user=None, k=1, N=1, alpha_item_similarity=1.0, alpha_item_item=1.0, t0=0):
    rank = GetRankItemSimilarityTime(train, user, k, alpha_item_similarity, alpha_item_item, t0)
    result = SortRank(rank, user, N)
    return result



#考虑（考虑时间后）兴趣相似用户的最近兴趣
def RecommendUserSimilarityTime(train, user=None, k=1, N=1, alpha_user_similarity=1.0, alpha_user_item=1.0, t0=0):
    rank = GetRankUserSimilarityTime(train, user, k, alpha_user_similarity, alpha_user_item, t0)
    result = SortRank(rank, user, N)
    return result






