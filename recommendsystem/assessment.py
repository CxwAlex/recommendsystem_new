import math
import time
from pandas import Series, DataFrame
from recommendsystem.engine_cf import ItemSimilarityCF

#对推荐结果进行总结
#其中，train是原始的训练集dataframe， recommend是推荐结果dataframe
#test是测试集的dataframe或者多元组
def Summary(train, recommend, test, item_similarity=None):
    t0 = time.clock()

    recall = Recall(recommend, test)
    t1 = time.clock()
    time_recall = t1 - t0
    print("recall:", recall, "   time_recall:", time_recall)

    precision = Precision(recommend, test)
    t2 = time.clock()
    time_precision = t2 - t1
    print("precision:", precision, "   time_precision:", time_precision)

    coverage = Coverage(train, recommend)
    t3 = time.clock()
    time_coverage = t3 - t2
    print("coverage:", coverage, "   time_coverage:", time_coverage)

    popularity = Popularity(train, recommend)
    t4 = time.clock()
    time_popularity = t4 - t3
    print("popularity:", popularity, "   time_popularity:", time_popularity)

    novelty = Novelty(train, recommend)
    t5 = time.clock()
    time_novelty = t5 - t4
    print("novelty:", novelty, "   time_novelty:", time_novelty)

    if not isinstance(item_similarity, DataFrame):
        item_similarity = ItemSimilarityCF(train)
    diversity = Diversity(recommend, item_similarity)
    t6 = time.clock()
    time_diversity = t6 - t5
    print("diversity:", diversity, "   time_diversity:", time_diversity)

    '''
    index_all = ['recall', 'precision', 'coverage', 'popularity', 'novelty', 'diversity']
    result = Series(index=index_all)
    result['recall'] = recall
    result['precision'] = precision
    result['coverage'] = coverage
    result['popularity'] = popularity
    result['novelty'] = novelty
    result['diversity'] = diversity
    '''
    time_all = t6 - t0
    result = {'recall':recall, 'precision':precision, 'coverage':coverage, 'popularity':popularity, 'novelty':novelty, 'diversity':diversity}
    spend_time = {'time_recall':time_recall, 'time_precision':time_precision, 'time_coverage':time_coverage, 'time_popularity':time_popularity, 'time_novelty':time_novelty, 'time_diversity':time_diversity, 'time_all':time_all}
    return result, spend_time

#计算准确率和召回率
def Recall(recommend, test):
    all = 0
    #分为原始数据和dataframe两种方式
    if isinstance(test, DataFrame):
        for u in test.columns:
            for i in test.index:
                if test[u][i] != 0:
                    all += 1
    else:
        all = len(test)

    hit = Hit(recommend, test)

    return hit / all


def Precision(recommend, test):
    all = 0
    N = len(recommend.index)

    for user in recommend.columns:
        all += N

    hit =Hit(recommend, test)

    return hit / all

def Hit(recommend, test):
    hit = 0
    #分为原始数据和dataframe两种方式
    if isinstance(test, DataFrame):
        for user in test.columns:
            for item in test.index:
                if test[user][item] != 0:
                    if user in recommend.columns and item in recommend[user].values:
                        hit += 1
    else:
        for i in test:
            if i[0] in recommend.columns and i[1] in recommend[i[0]].values:
                hit += 1
    return hit


#计算覆盖率
def Coverage(train, recommend):
    recommend_items = set()
    all_items = set()

    for item in train.index:
            all_items.add(item)

    for user in recommend.columns:
        for item in recommend[user].values:
            recommend_items.add(item)

    return len(recommend_items) / len(all_items)


#计算新颖度
#如果推荐的每个物品都很流行，那么结果或很高，新颖度会很低；反之如果每个物品都是冷门物品，则结果约等于1
def Popularity(train, recommend):
    popularity = 0
    n = 0

    #首先计算不同物品的流行度
    item_popularity = Series(0.0, index=recommend.index)
    for user in train.columns:
        for item in train.index:
            if train[user][item] != 0:
                if item not in item_popularity:
                    item_popularity[item] = 1
                item_popularity[item] += 1

    #接着计算推荐物品的流行度
    for user in recommend.columns:
        for item in recommend[user].values:
            if item in item_popularity.index:
                popularity += math.log(1 + item_popularity[item])
                n += 1

    popularity /= n

    return popularity

def Novelty(train, recommend):
    novelty = 1 / Popularity(train, recommend)
    return novelty

#利用相似度度量计算推荐列表的多样性
#如果推荐的物品相似度都很高，则说明多样性不强，反之，若相似度都不高，则说明多样性很高
def Diversity(recommend, item_similarity):
    similarity = 0
    n = 0
    recommend_items = set()
    for user in recommend.columns:
        for item in recommend[user].values:
            recommend_items.add(item)

    for i in recommend_items:
        for j in recommend_items:
            if i == j:
                continue
            if i in item_similarity.columns and j in item_similarity.index:
                similarity += item_similarity[i][j]
                n += 1

    return 1 - math.sqrt(similarity/n)



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

'''
if rv is not None and rsv is not None:
# extract version/subversion
self._nmap_version_number = int(line[rv.start():rv.end()])
self._nmap_subversion_number = int(line[rsv.start()+1:rsv.end()])
break
}


'''