def getparaters(dataset, recommend_engine):
    if dataset == 'MovieLens1M':
        return MovieLens1MParameters(recommend_engine)
    else:
        return Parameters(recommend_engine)

def Parameters(recommend_engine):
    parameters = {}
    if recommend_engine == 'RecommendUserCF':
        parameters['similarity'] = ['downhot', 'norm']
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 16]
    elif recommend_engine == 'RecommendItemCF':
        parameters['similarity'] = ['downhot', 'norm']
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 16]
    elif recommend_engine == 'RecommendSocial':
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendByTags':
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendItemSimilarityTime':
        parameters['alpha_item_similarity'] = [0.3, 0.6, 1.0, 2.0]
        parameters['alpha_item_item'] = [0.3, 0.6, 1.0, 2.0]
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendUserSimilarityTime':
        parameters['alpha_user_similarity'] = [0.3, 0.6, 1.0, 2.0]
        parameters['alpha_user_item'] = [0.3, 0.6, 1.0, 2.0]
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendMostHot':
        parameters[type] = ['day', 'week', 'month', 'ever']
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendColdStartItem':
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendRandom':
        parameters['N'] = [5, 10, 20]

    return parameters

def MovieLens1MParameters(recommend_engine):
    parameters = {}
    if recommend_engine == 'RecommendUserCF':
        parameters['similarity'] = ['downhot', 'norm']
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 16]
    elif recommend_engine == 'RecommendItemCF':
        parameters['similarity'] = ['downhot', 'norm']
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 16]
    elif recommend_engine == 'RecommendItemSimilarityTime':
        parameters['alpha_item_similarity'] = [0.3, 0.6, 1.0, 2.0]
        parameters['alpha_item_item'] = [0.3, 0.6, 1.0, 2.0]
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendUserSimilarityTime':
        parameters['alpha_user_similarity'] = [0.3, 0.6, 1.0, 2.0]
        parameters['alpha_user_item'] = [0.3, 0.6, 1.0, 2.0]
        parameters['k'] = [5, 10, 20, 40, 100]
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendMostHot':
        parameters[type] = ['day', 'week', 'month', 'ever']
        parameters['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendRandom':
        parameters['N'] = [5, 10, 20]
    else:
        return None

    return parameters