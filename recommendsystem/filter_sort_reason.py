from pandas import DataFrame
from recommendsystem.engine_cf import ItemSimilarityCF
def sortByWeight(recommendations):
    return None

#根据推荐理由增加推荐多样性（每次拿出一个结果，若已经使用过，则对其降权）
def ReasonDiversity(recommendations):
    reasons = set()
    for i in recommendations:
        if i.reason in reasons:
            i.weight /= 2
        reasons.add(i.reason)
    recommendations = sortByWeight(recommendations)


#带解释的基于物品的推荐
def RecommendationItemCF(train):
    item_similarity = ItemSimilarityCF(train)

    #对用户列表里的每一个物品，计算其相关物品的推荐结果
    rank = DataFrame(0.0, index= train.index, columns= train.columns)
    rank_reason = DataFrame("" ,index= train.index, columns= train.columns)
    for u in train.columns:
        for i in train.index[train[u] != 0]:
            for j in item_similarity.index[item_similarity[i] != 0]:
                #此处因为单独取出了不为0的物品，所以没有必要查重了
                #但是以后要是有评分或者权重的时候，还是需要的
                rank[u][j] += train[u][i] * item_similarity[i][j]
                rank_reason[u][j] += ("用户" + u + "喜欢" + i + "，物品" + i + "和" + j + "相似度为" + str(item_similarity[i][j]) + "；")
    return rank, rank_reason