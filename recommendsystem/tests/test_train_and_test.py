import os
import sys
pwd = os.getcwd()
project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")

sys.path.append(project_filepath)
import unittest
from conf.settings import *
from recommendsystem.ETL import *
from recommendsystem.TrainAndTestWorkflow import *

class RecommendAndParameterTest(unittest.TestCase):
    '''
    def test_user_cf(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        RecommendAndParameter(data_std, 'RecommendUserCF', repeat_k=10)
        #parameters = getparaters('MovieLens1M', 'RecommendUserCF')
        #RecommendAndParameter(data_std, 'RecommendUserCF', parameters=parameters, repeat_k=10)

    def test_random(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        parameters = getparaters('MovieLens1M', 'RecommendRandom')
        RecommendAndParameter(data_std, 'RecommendUserCF', repeat_k=10, parameters=parameters)
    '''
    def test_random1k(self):
        print(pwd)
        print(project_filepath)
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_1kuser.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        parameters = getparaters('MovieLens1M', 'RecommendRandom')
        RecommendAndParameter(data_std, 'RecommendRandom', repeat_k=10, parameters=parameters)

    '''
    def test_random500(self):

        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_500user.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        parameters = getparaters('MovieLens1M', 'RecommendRandom')
        RecommendAndParameter(data_std, 'RecommendRandom', repeat_k=10, parameters=parameters)



    def test_random100(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        parameters = getparaters('MovieLens1M', 'RecommendRandom')
        RecommendAndParameter(data_std, 'RecommendRandom', repeat_k=10, parameters=parameters)
'''
'''
    def test_result2log(self):
        num = Result2Log(0)
        self.assertEqual(num, 1)
'''
