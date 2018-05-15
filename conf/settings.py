def Parameter(recommend_engine):
    parameter = {}
    if recommend_engine == 'RecommendUserCF':
        parameter['k'] = [5, 10, 20, 40, 100]
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendItemCF':
        parameter['k'] = [5, 10, 20, 40, 100]
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendSocial':
        parameter['k'] = [5, 10, 20, 40, 100]
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendByTags':
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendItemSimilarityTime':
        parameter['alpha_item_similarity'] = [0.3, 0.6, 1.0, 2.0]
        parameter['alpha_item_item'] = [0.3, 0.6, 1.0, 2.0]
        parameter['k'] = [5, 10, 20, 40, 100]
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendUserSimilarityTime':
        parameter['alpha_user_similarity'] = [0.3, 0.6, 1.0, 2.0]
        parameter['alpha_user_item'] = [0.3, 0.6, 1.0, 2.0]
        parameter['k'] = [5, 10, 20, 40, 100]
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendMostHot':
        parameter[type] = ['day', 'week', 'month', 'ever']
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendColdStartItem':
        parameter['N'] = [5, 10, 20]
    elif recommend_engine == 'RecommendRandom':
        parameter['N'] = [5, 10, 20]

    return parameter