import os
import sys
pwd = os.getcwd()
project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.append(project_filepath)
import unittest

from recommendsystem.TrainAndTestWorkflow import *

class RecommendAndParameterTest(unittest.TestCase):
    #此处只做most_hot_ever
    def test_item1k(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_1kuser.dat'
        data_std = MovieLensRatings2Std(read_filepath)

        recommend_engine = 'RecommendMostHot'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, repeat_k=10, parameters=parameters)

    def test_item100(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)

        recommend_engine = 'RecommendMostHot'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, repeat_k=10, parameters=parameters)
