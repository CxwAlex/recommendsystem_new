import os
import sys
pwd = os.getcwd()
project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.append(project_filepath)
import unittest

from recommendsystem.TrainAndTestWorkflow import *

def MovieLens1MParameters(recommend_engine):
    parameters = {}
    if recommend_engine == 'RecommendUserCF':
        parameters['similarity'] = ['downhot']
        parameters['k'] = [20]
        parameters['N'] = [16]
    elif recommend_engine == 'RecommendItemCF':
        parameters['similarity'] = ['downhot']
        parameters['k'] = [40]
        parameters['N'] = [16]
    elif recommend_engine == 'RecommendUserProperty':
        parameters['k'] = [40]
        parameters['N'] = [16]
        parameters['weight'] = [[0, 0.3, 0.6, 0.3, 0.1]]
    else:
        return None

    return parameters




def getparaters(dataset, recommend_engine):
    if dataset == 'MovieLens1M':
        return MovieLens1MParameters(recommend_engine)
    else:
        return Parameters(recommend_engine)



class RecommendAndParameterTest(unittest.TestCase):
    def test_usercf_property_sim(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)

        recommend_engine = 'RecommendMostHot'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, repeat_k=10, parameters=parameters)

    def test_usercf_property_rank(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)

        recommend_engine = 'RecommendMostHot'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, repeat_k=10, parameters=parameters)

    def test_usercf_itemcf(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)

        recommend_engine = 'RecommendMostHot'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, repeat_k=10, parameters=parameters)
