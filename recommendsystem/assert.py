#计算准确率和召回率
def Recall(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user, N)
        for item in rank:
            if item in tu:
                hit += 1
        all += len(tu)
    return hit / (all * 1.0)

def Precision(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user, N)
        for item in rank:
            if item in tu:
                hit += 1
        all += N
    return hit / (all * 1.0)

#计算覆盖率
def Coverage(train, N):
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user]:
            all_items.add(item)
        rank = GetRecommendation(user, N)
        for item in rank:
            recommend_items.add(item)
    return len(recommend_items) / (len(all_items) * 1.0)

#计算新颖度
def Popularity(train, N):
    #首先计算不同物品的流行度
    item_popularity = dict()
    for user, items in train.items():
        for item in items:
            if item not in item_popularity:
                item_popularity[item] = 1
            item_popularity[item] += 1
    #接着计算推荐物品的流行度
    ret = 0
    n = 0
    for user in train.keys():
        rank = GetRecommendation(user, N)
        for item in rank:
            #print(item_popularity[item])
            #print(math.log(item_popularity[item]))
            ret += math.log(1 + item_popularity[item])
            n += 1
    ret /= n * 1.0
    return ret


#利用相似度度量计算推荐列表的多样性
# 如果推荐的物品相似度都很高，则说明多样性不强，反之，若相似度都不高，则说明多样性很高
# todo：这个评测在什么时候做，针对单个用户或者用户全体做等
# todo：暂时不能评测，因为推荐部分还没有完成——基于标签相似度的推荐
def Diversity(item_tags, recommend_items):
    ret = 0
    n = 0
    for i in recommend_items.keys():
        for j in recommend_items.keys():
            if i == j:
                continue
            ret += item_similarity(item_tags, i, j)
            n += 1
    #return 1 - ret / (n * 1.0)
    return None


import math
import operator


# 计算RMSE和MAE
def RMSE(records):
    '''
    print(sum([(rui-pui)*(rui-pui) for u,i,rui,pui in records]) )
    print(float(len(records)))
    print(math.sqrt(\
    sum([(rui-pui)*(rui-pui) for u,i,rui,pui in records]) / float(len(records))))
    '''
    return math.sqrt( \
        sum([(rui - pui) * (rui - pui) for u, i, rui, pui in records]) / float(len(records)))


def MAE(records):
    return sum([abs(rui - pui) for u, i, rui, pui in records]) / float(len(records))


# 计算准确率和召回率
def PrecisionRecall(test, N):
    hit = 0
    n_recall = 0
    n_precision = 0
    for user, items, rank in test:
        hit += sum(map(lambda x, y: 1 if x == y else 0, items, rank))
        n_recall += len(items)
        n_precision += N
    return [hit / (1.0 * n_recall), hit / (1.0 * n_precision)]

    '''
def PrecisionRecall(test, N):
    #原始版本，rank表示recommend处理推荐之后的结果集
    hit = 0
    n_recall = 0
    n_precision = 0
    for user, items in test.items():
        rank = Recommend(user, N)
        hit += len(rank & items)
        n_recall += len(items)
        n_precision += N
    return [hit / (1.0 * n_recall), hit / (1.0 * n_precision)]


#计算基尼系数
def GiniIndex(p):
    j = 1
    n = len(p)
    G = 0
    print(p)
    print(sorted(p, key=operator.itemgetter(1)))
    for item, weight in sorted(p, key=operator.itemgetter(1)):
        G += (2 * j - n - 1) * weight
    return G / float(n - 1)
    '''