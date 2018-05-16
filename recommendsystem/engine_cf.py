import time
from pandas import Series, DataFrame
import random
import math
from recommendsystem.utils import count_set

#计算余弦相似度
def UserSimilarityCF(train):
    w = DataFrame(0.0, index=train.columns, columns=train.columns)
    count_columns = train.apply(func=count_set, axis=0)

    for u in train.columns:
        for v in train.columns:
            if u == v:
                w[u][v] = 1
                continue

            w[u][v] += count_set(train[u] & train[v])
            if count_columns[u] * count_columns[v]:
                w[u][v] /= math.sqrt(count_columns[u] * count_columns[v])
    return w


#利用倒排方法计算用户相似度
def UserSimilarityBackCF(train):
    train_item_user = train.T
    #calculate co-rated items between users
    #C表示u和v对拥有相同兴趣的物品数
    #N表示用户对物品产生行为的个数
    N = train_item_user.apply(func=count_set, axis=1)
    C = DataFrame(0, index=train.columns, columns=train.columns)
    for item in train_item_user.columns:
        for u in train_item_user.index:
            for v in train_item_user.index:
                if train_item_user[item][u] == 0 or train_item_user[item][v] == 0 or u == v:
                    continue
                else:
                    C[u][v] += 1

    #calculate finial similarity matrix W
    W = DataFrame(0.0, index=train_item_user.index, columns=train_item_user.index)
    for u in train_item_user.index:
        for v in train_item_user.index:
            if u == v:
                W[u][v] += 1
            elif N[u] * N[v]:
                W[u][v] += C[u][v] / math.sqrt(N[u] * N[v])
    return W


#惩罚了共同兴趣中的热门物品后的user-II的相似度计算
def UserSimilarityDownHotCF(train):
    #calculate co-rated items between users
    C = DataFrame(0.0, index=train.columns, columns=train.columns)
    for item in train.index:
        users = train.columns[train.ix[item] != 0]
        for u in users:
            for v in users:
                if u == v:
                    C[u][v] += 1
                    continue
                C[u][v] += 1 / math.log(1 + len(users))
    #print('计算完成C')
    w = DataFrame(0.0, index= train.columns, columns= train.columns)
    N = train.apply(func=count_set, axis=0)

    for u in train.columns:
        for v in train.columns:
            if u == v:
                w[u][v] += 1
                continue
            w[u][v] += C[u][v]
            if N[u] * N[v]:
                w[u][v] /= math.sqrt(N[u] * N[v])
    #print('计算完成W')
    return w


#物品相似度
def ItemSimilarityCF(train):
    #calculate co-rated users between items
    #计算物品之间的相似性
    C = DataFrame(0.0, index=train.index, columns=train.index)
    N = train.apply(func=count_set, axis=1)
    for u in train.columns:
        t0 = time.clock()
        items = train.index[train[u] != 0]
        for i in items:
            for j in items:
                #有针对性的决定是否包含元素本身
                if i == j:
                    C[i][j] += 1
                    continue
                C[i][j] += 1
        t1 = time.clock()
        print(u,'done',t1-t0)

    #calculate finial similarity matrix W
    W = DataFrame(0.0, index=train.index, columns=train.index)
    for i in train.index:
        t0 = time.clock()
        for j in train.index:
            if N[i] * N[j]:
                W[i][j] += C[i][j] / math.sqrt(N[i] * N[j])
        t1 = time.clock()
        print('物品', i, 'done', t1-t0)
    return W



#todo:此处出现了分离，即两个在用户行为上完全一致的物品，其相似度不一样
#todo：主要是物品要跟自己相似，则自身相似度为1；但是一样行为的物品却因为热门惩罚系数降低
#todo：想一想这个问题如何解决——矩阵对称性重要，还是自身相似度为1重要
#惩罚活跃用户后的基于物品相似度的推荐算法
def ItemSimilarityDownHotCF(train):
    # calculate co-rated users between items
    # 计算物品之间的相似性
    C = DataFrame(0.0, index=train.index, columns=train.index)
    N = train.apply(func=count_set, axis=1)
    users = Series(0.0, index= train.index)
    for item in train.index:
        users[item] = train.columns[train.ix[item] != 0]

    for u in train.columns:
        items = train.index[train[u] != 0]
        for i in items:
            for j in items:
                #if i == j:
                #    C[i][j] += 1
                #   continue
                C[i][j] += 1 / math.log(1 + len(items) * 1.0)

    # calculate finial similarity matrix W
    W = DataFrame(0.0, index=train.index, columns=train.index)
    std_W = Series(0.0,index= train.index)
    for i in train.index:
        #下面是针对每一列进行归一化，但是会导致矩阵不对称问题
        #std_W[i] = C[i][i] / math.sqrt(N[i] * N[i])
        for j in train.index:
            #归一化
            #W[i][j] = (C[i][j] / math.sqrt(N[i] * N[j]))/std_W[i]
            if N[i] * N[j]:
                W[i][j] += (C[i][j] / math.sqrt(N[i] * N[j]))
    return W


def GetUserSimilarity(train, similarity_type=None):
    if similarity_type == 'downhot':
        W = UserSimilarityDownHotCF(train)
    else:
        W = UserSimilarityCF(train)

    return W


def GetItemSimilarity(train, similarity_type=None):
    if similarity_type == 'downhot':
        W = ItemSimilarityDownHotCF(train)
    else:
        W = ItemSimilarityCF(train)

    return W


# userCF推荐算法
def GetRankUserCF(train, user=None, k=1, user_similarity=None):
    #W是用户之间的兴趣相似度, k是邻居数目
    if not isinstance(user_similarity, DataFrame):
        user_similarity = UserSimilarityCF(train)

    if user:
        rank = Series(0.0, index=train.index)
        for v in user_similarity[user].sort_values(ascending=False).index[1:k + 1]:
            for i in train[v].index:
                if train[v][i] == 0:
                    continue
                else:
                    rank[i] += user_similarity[user][v] * train[v][i]
    else:
        rank = DataFrame(0.0, index=train.index, columns=train.columns)
        #u是目标用户，v是近邻用户，W[u][v]是相似度
        #i是物品编号，train[v][i]是v对i的兴趣
        for u in train.columns:
            for v in user_similarity[u].sort_values(ascending=False).index[1:k+1]:
                for i in train[v].index:
                    if train[v][i] == 0:
                        rank[u][i] += 0
                    else:
                        rank[u][i] += user_similarity[u][v] * train[v][i]

    return rank


def GetRankItemCF(train, user=None, k=1, item_similarity=None):
    #首先获得物品相似度矩阵
    if not isinstance(item_similarity, DataFrame):
        item_similarity = ItemSimilarityCF(train)

    #对用户列表里的每一个物品，计算其相关物品的推荐结果
    if user:
        rank = Series(0.0, index=train.index)
        for i in train.index[train[user] != 0]:
            for j in item_similarity[i].sort_values(ascending=False).index[0:k]:
                rank[j] += train[user][i] * item_similarity[i][j]
    else:
        rank = DataFrame(0.0, index=train.index, columns=train.columns)
        for u in train.columns:
            for i in train.index[train[u] != 0]:
                for j in item_similarity[i].sort_values(ascending=False).index[0:k]:
                    rank[u][j] += train[u][i] * item_similarity[i][j]

    return rank


def SortRankUser(rank, N=1):
    if N:
        result = rank.sort_values(ascending=False).index[0:N]
    else:
        result = rank.sort_values(ascending=False).index
    return result

def SortRank(rank, N=1):
    # 是否排序&是否TopN推荐
    if N:
        result = DataFrame(columns=rank.columns)
        for u in rank.columns:
            result[u] = rank[u].sort_values(ascending=False).index[0:N]
    else:
        result = DataFrame(columns=rank.columns)
        for u in rank.columns:
            result[u] = rank[u].sort_values(ascending=False).index
    return result


def FilterAndSort(train, rank, user=None, N=1):
    if user:
        for i in train.index[train[user] != 0]:
            rank[i] = 0
        result = SortRankUser(rank, N)
    else:
        for u in train.columns:
            for i in train.index[train[u] != 0]:
                rank[u][i] = 0
        result = SortRank(rank, N)

    return result


#若排序则返回排序后的推荐结果，否则返回推荐分数矩阵
#train是训练集，user是待推荐的用户，k是训练时的近邻个数，N是返回的推荐结果数
def RecommendUserCF(train, user=None, k=1, N=1, similarity=None):
    user_similarity = GetUserSimilarity(train, similarity)
    rank = GetRankUserCF(train, user, k, user_similarity)
    recommend = FilterAndSort(train, rank, user=None, N=1)

    return recommend


def RecommendItemCF(train, user=None, k=1, N=1, similarity=None, sort=True):
    item_similarity = GetItemSimilarity(train, similarity)
    rank = GetRankItemCF(train, user, k, item_similarity)
    recommend = FilterAndSort(train, rank, user=None, N=1)

    return recommend


#基于图的随机游走算法
#train是训练集，p是每次漫步的继续的随机数，即有p的概率继续向下走
#N是每个用户重复训练的次数, is_P决定返回是概率还是频率，默认概率
def PersonalRank(train, p, N, is_P=True, filter_item=True):
    users_items = Series(index=train.columns)
    items_users = Series(index=train.index)
    for u in train.columns:
        users_items[u] = train.index[train[u] != 0]
    for i in train.index:
        items_users[i] = train.columns[train.ix[i] != 0]

    #接下来开始随机游走——分为两步：随机走一步&随机停
    result = DataFrame(0.0, index= train.index, columns= train.columns)

    for u in train.columns:
        for count in range(0, N):
            i = random.sample(list(users_items[u]), 1)[0]
            if filter_item:
                while i in users_items[u]:
                    while random.random() <= p:
                        iu = random.sample(list(items_users[i]), 1)[0]
                        i = random.sample(list(users_items[iu]), 1)[0]
            else:
                while random.random() <= p:
                    iu = random.sample(list(items_users[i]), 1)[0]
                    i = random.sample(list(users_items[iu]), 1)[0]
            if is_P:
                result[u][i] += 1 / N
            else:
                result[u][i] += 1

    return result