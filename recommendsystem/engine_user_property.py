import time
from pandas import Series, DataFrame
from recommendsystem.engine_social import sort_similarity_and_rank

#计算余弦相似度
def UserSimilarityProperty(data_std, weight):
    user = []
    for i in data_std:
        user.append(i[0])

    w = DataFrame(0.0, index=user, columns=user)

    len_users = len(data_std[0])
    for i in data_std:
        t0 = time.clock()
        for j in data_std:
            if i == j:
                continue
            w[i[0]][j[0]] += GetPropertySimilarity(i, j, len_users, weight)

        t1 = time.clock()
        print('user_property', i[0], 'done', t1 - t0)

    return w


def GetPropertySimilarity(user_property1, user_property2, len_user_property, weight):
    similarity = 0
    for i in range(1, len_user_property):
        similarity += weight[i] * PropertySimilarity(user_property1[i], user_property2[i], i)
    return similarity


def PropertySimilarity(property1, property2, i):
    #注意，这里是专门针对MovieLens的相似度计算
    result = 0
    if i == 1:
        if property1 == property2:
            result = 1
    elif i == 2:
        result = 1 - abs(int(property2) - int(property1)) / 56
    elif i == 3:
        if property1 == property2:
            result = 1
    elif i == 4:
        if len(property1.split("-")) == 2:
            property1 = property1.split("-")[0]
        if len(property2.split("-")) == 2:
            property2 = property2.split("-")[0]
        result = 1 - abs(int(property2) - int(property1)) / 100000
    else:
        return result

    return result


#若排序则返回排序后的推荐结果，否则返回推荐分数矩阵
#train是训练集，user是待推荐的用户，k是训练时的近邻个数，N是返回的推荐结果数
def FriendSuggestionUserProperty(data_std, weight, user=None, N=1):
    user_similarity = UserSimilarityProperty(data_std, weight)
    friend_suggestion = sort_similarity_and_rank(user_similarity, user, N)

    return friend_suggestion
