import math
from pandas import Series, DataFrame
from recommendsystem.utils import count_set

#本引擎主要分为4个模块
#2个相似度计算模块：有向网络中的相似度、无向网络中的相似度
#1个基于相似度的好友推荐模块
#1个基于相似度的物品推荐模块
#其中，ETL接受两种格式的数据：用户之间的关系字典(graph2dataframe)，或者矩阵式的输入（matrix2dataframe）
#输入到引擎中开始计算相似度时应该已经是用户之间的关系

#判断输入的社交关系是有向还是无向，获得相应的相似度并返回
def social_similarity(dataframe, user=None, filter=True):
    for u in dataframe.columns[0:1]:
        for v in dataframe.columns[1:2]:
            if dataframe[u][v] == dataframe[v][u]:
                similarity = similarity_no_direction(dataframe, user, filter)
            else:
                similarity = similarity_have_direction(dataframe, user, filter)

    return similarity

#无向社交网络，根据共同好友比例计算相似度
#此处定义使用的是社交网络里的out来计算相似度，也可以使用in，在无向社交网络里两者相等
def similarity_no_direction(dataframe, user= None, filter= True):
    if user:
        similarity = Series(0.0, index= dataframe.index)
        for v in dataframe.index:
            if user == v or dataframe[user][v] == 1:
                if filter:
                    continue
                else:
                    similarity[v] += 1
                continue
            similarity[v] += count_set(dataframe[user] & dataframe.ix[v]) / \
                                math.sqrt(1.0 * count_set(dataframe[user]) * count_set(dataframe.ix[v]))
    else:
        similarity = DataFrame(0.0, index= dataframe.index, columns= dataframe.columns)
        for u in dataframe.columns:
            for v in dataframe.index:
                if u == v or dataframe[u][v] == 1:
                    if filter:
                        similarity[u][v] = 0
                    else:
                        similarity[u][v] = 1
                    continue
                similarity[u][v] += count_set(dataframe[u]&dataframe.ix[v]) / \
                                    math.sqrt(1.0 * count_set(dataframe[u]) * count_set(dataframe.ix[v]))

    return similarity

#有向社交网络中的相似度
def similarity_have_direction(dataframe, user= None, filter= True):
    if user:
        similarity = Series(0.0, index=dataframe.index)
        for v in dataframe.index:
            if user == v or dataframe[user][v] == 1:
                if filter:
                    continue
                else:
                    similarity[v] += 1
                continue
            result = 0
            for i in dataframe.columns:
                # 如果u没有关注过i，那么则跳过
                if dataframe[user][i] == 0:
                    continue
                if dataframe[i][v] == 1:
                    result += 1
            similarity[v] = result / math.sqrt(1.0 * count_set(dataframe[user]) * count_set(dataframe.ix[v]))
    else:
        similarity = DataFrame(0.0, index=dataframe.index, columns=dataframe.columns)
        for u in dataframe.columns:
            for v in dataframe.index:
                if u == v or dataframe[u][v] == 1:
                    if filter:
                        similarity[u][v] = 0
                    else:
                        similarity[u][v] = 1
                    continue
                result = 0
                for i in dataframe.columns:
                    #如果u没有关注过i，那么则跳过
                    if dataframe[u][i] == 0:
                        continue
                    if dataframe[i][v] == 1:
                        result += 1
                similarity[u][v] = result / math.sqrt(1.0 * count_set(dataframe[u]) * count_set(dataframe.ix[v]))

    return similarity


def sort_similarity_and_rank(similarity, user=None, N=1):
    if user:
        result = similarity.sort_values(ascending=False).index[0:N]
    else:
        result= DataFrame(columns=similarity.columns)
        for u in similarity.columns:
            result[u] = similarity[u].sort_values(ascending=False).index[0:N]

    return result


def FriendSuggestion(dataframe, user=None, N=1, filter=True):
    similarity = social_similarity(dataframe, user, filter)
    suggestion = sort_similarity_and_rank(similarity, user, N)
    return suggestion


def RecommendSocial(dataframe_social, dataframe_item, user=None, N=1):
    similarity_uu = social_similarity(dataframe_social, user)
    if user:
        rank = Series(0.0, index=dataframe_item.index)
        for v in dataframe_social.columns:
            if user == v or similarity_uu[user][v] == 0:
                continue
            for i in dataframe_item.index:
                if dataframe_item[v][i] == 0 or dataframe_item[user][i] != 0:
                    continue
                rank[i] += similarity_uu[user][v] * dataframe_item[v][i]
    else:
        rank = DataFrame(0.0, index=dataframe_item.index, columns=dataframe_social.columns)
        for u in dataframe_social.columns:
            for v in dataframe_social.columns:
                if u == v or similarity_uu[u][v] == 0:
                    continue
                for i in dataframe_item.index:
                    if dataframe_item[v][i] == 0 or dataframe_item[u][i] != 0:
                        continue
                    rank[u][i] += similarity_uu[u][v] * dataframe_item[v][i]

    result = sort_similarity_and_rank(rank, user, N)
    return result
