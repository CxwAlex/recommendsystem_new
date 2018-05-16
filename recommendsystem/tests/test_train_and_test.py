import os
import unittest
from conf.settings import *
from recommendsystem.ETL import *
from recommendsystem.TrainAndTestWorkflow import *

class RecommendAndParameterTest(unittest.TestCase):

    def test_user_cf(self):
        pwd = os.getcwd()
        project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        RecommendAndParameter(data_std, 'RecommendUserCF', repeat_k=10)
        #parameters = getparaters('MovieLens1M', 'RecommendUserCF')
        #RecommendAndParameter(data_std, 'RecommendUserCF', parameters=parameters, repeat_k=10)

    def test_result2log(self):
        num = Result2Log(0)
        self.assertEqual(num, 1)

