import math
from pandas import Series, DataFrame
from collections import defaultdict
from recommendsystem.utils import count_set, count_tags
from recommendsystem.utils import get_user_item, get_item_tags,get_user_tags,get_user_item_tag

#修改成一个通用的计算相似度的方式
def SimilarityTags(dataframe, feature=None):
    if feature:
        feature_similarity = Series(0.0, index=dataframe.columns)
        for feature_j in dataframe.columns:
            count = 0
            if feature == feature_j:
                continue
            for tag in dataframe.index:
                if dataframe[feature][tag] == 0 or dataframe[feature_j][tag] == 0:
                    continue
                count += 1
            if count == 0:
                feature_similarity[feature_j] = 0
            else:
                feature_similarity[feature_j] = count / math.sqrt(count_set(dataframe[feature]) * count_set(dataframe[feature_j]))
    else:
        feature_similarity = DataFrame(0.0, columns=dataframe.columns, index=dataframe.columns)
        for feature_i in dataframe.columns:
            for feature_j in dataframe.columns:
                count = 0
                if feature_i == feature_j:
                    continue
                for tag in dataframe.index:
                    if dataframe[feature_i][tag] == 0 or dataframe[feature_j][tag] == 0:
                        continue
                    count += 1
                if count == 0:
                    feature_similarity[feature_i][feature_j] = 0
                else:
                    feature_similarity[feature_i][feature_j] = count / math.sqrt(count_set(dataframe[feature_i]) * count_set(dataframe[feature_j]))

    return feature_similarity

#计算基于标签的物品余弦相似度
#此处假设不包含标签的次数
def ItemSimilarityTags(item_tags, item=None):
    item_similarity = SimilarityTags(item_tags, item)
    return item_similarity


def UserSimilarityTags(user_tags, user=None):
    user_similarity = SimilarityTags(user_tags, user)
    return user_similarity


def TagsSimilarityByItem(tags_item, tag=None):
    tag_similarity = SimilarityTags(tags_item,tag)
    return tag_similarity


def TagsSimilarityByUser(tags_user, tag=None):
    tag_similarity = SimilarityTags(tags_user, tag)
    return tag_similarity

#基于标签的推荐
#从 records 中统计出 user_tags 和 tag_items
#统计出user_tags和tag_items之后，就可以通过以下程序对用户进行个性化推荐
def RecommendByTags(user_item_tags, user=None, N=1):
    user_tags = get_user_tags(user_item_tags)
    tag_items = get_item_tags(user_item_tags).T
    user_items = get_user_item(user_item_tags)
    #todo:这里需要做出两个改变，1是要将数据格式换成series，2是要转换成对所有用户进行标签推荐
    if user:
        recommend_items = defaultdict(int)
        tagged_items = user_items.index[user_items[user] != 0]

        for tag in user_tags.index[user_tags[user] != 0]:
            for item in tag_items.index[tag_items[tag] != 0]:
                if item in tagged_items:
                    continue
                else:
                    recommend_items[item] += user_tags[user][tag] * tag_items[tag][item]
        recommend = Series(recommend_items)
        result = recommend.index.sort_values()[0:N].tolist()
    else:
        result = DataFrame(columns=user_tags.columns)
        for user in user_tags.columns:
            recommend_items = defaultdict(int)
            tagged_items = user_items.index[user_items[user] != 0]

            for tag in user_tags.index[user_tags[user] != 0]:
                for item in tag_items.index[tag_items[tag] != 0]:
                    if item in tagged_items:
                        continue
                    else:
                        recommend_items[item] += user_tags[user][tag] * tag_items[tag][item]
            recommend = Series(recommend_items)
            result[user] = recommend.index.sort_values()[0:N].tolist()
    return result


def RecommendTags(user_item_tag, user=None, item=None, tag=None, alpha=0.3, N=1):
    if tag:
        result = RecommendSimilarityTags(user_item_tag, tag, N)
    elif user and item:
        result = RecommendHybridPopularTags(user_item_tag, user, item, alpha, N)
    elif user:
        result = RecommendUserPopularTags(user_item_tag, user, N)
    elif item:
        result = RecommendItemPopularTags(user_item_tag, item, N)
    else:
        result = RecommendPopularTags(user_item_tag, N)

    return result

#给用户推荐标签
#给用户推荐整个系统里最热门的标签
def RecommendPopularTags(user_item_tag, N=1):
    tags = count_tags(user_item_tag)
    return tags.sort_values(ascending=False).index.tolist()[0:N]


#给用户推荐物品i上最热门的标签
def RecommendItemPopularTags(user_item_tag, item=None, N=1):
    if not item:
        return None
    item_tags = get_item_tags(user_item_tag)
    return item_tags[item].sort_values(ascending=False).index.tolist()[0:N]


#给用户推荐自己最经常会用的标签
def RecommendUserPopularTags(user_item_tag, user=None, N=1):
    if not user:
        return None
    user_tags = get_user_tags(user_item_tag)
    return user_tags[user].sort_values(ascending=False).index.tolist()[0:N]

#结合上述两种方式
#alpha是指用户自己经常打的标签的权重
def RecommendHybridPopularTags(user,item, user_item_tag, alpha = 0.3, N=1):
    # 此处假设两者传来的标签一致
    item_tags = get_item_tags(user_item_tag)
    user_tags = get_user_tags(user_item_tag)
    ret = Series(0.0, index= item_tags.index)
    max_user_tag_weight = user_tags[user].max()
    for tag in user_tags[user].index:
        ret[tag] = (1 - alpha) * user_tags[user][tag] / max_user_tag_weight
    max_item_tag_weight = item_tags[item].max()
    for tag in item_tags[item].index:
        ret[tag] += alpha * item_tags[item][tag] / max_item_tag_weight

    return ret.sort_values(ascending=False).index.tolist()[0:N]


def RecommendSimilarityTags(user_item_tag, tag=None, N=1):
    if not tag:
        return None
    tags_item = get_item_tags(user_item_tag).T
    tags_similarity = TagsSimilarityByItem(tags_item, tag)
    return tags_similarity.sort_values(ascending=False).index.tolist()[0:N]
