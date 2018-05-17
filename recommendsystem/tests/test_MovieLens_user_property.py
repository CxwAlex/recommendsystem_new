import os
import sys
pwd = os.getcwd()
project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.append(project_filepath)
import unittest
from recommendsystem.TrainAndTestWorkflow import *

class RecommendAndParameterTest(unittest.TestCase):
    '''
    def test_user1k(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_1kuser.dat'
        data_std = MovieLensRatings2Std(read_filepath, lines=100)
        read_filepath_users = project_filepath + '/dataset/MovieLens/1m/users.dat'
        data_std_user = MovieLensRatings2Std(read_filepath_users, lines=100)
        recommend_engine = 'RecommendUserProperty'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)
        RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_user=data_std_user, repeat_k=10, parameters=parameters)


    '''
    def test_user100(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        read_filepath_users = project_filepath + '/dataset/MovieLens/1m/users.dat'
        data_std_user = MovieLensRatings2Std(read_filepath_users, lines=100)
        recommend_engine = 'RecommendUserProperty'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)
        print(parameters)
        print(data_std_user)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_user=data_std_user, repeat_k=10, parameters=parameters)
