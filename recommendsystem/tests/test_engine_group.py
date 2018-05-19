import os
import sys
pwd = os.getcwd()
project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.append(project_filepath)
import unittest

from recommendsystem.recommend_engine_group import *

def MovieLens1MParameters(recommend_engine):
    parameters = {}
    if recommend_engine == 'RecommendUserCF&UserProperty_similarity':
        parameters['similarity'] = 'downhot'
        parameters['k'] = [20,40]
        parameters['N'] = 16
        parameters['weight'] = [0, 0.3, 0.6, 0.3, 0.1]
    elif recommend_engine == 'RecommendUserCF&UserProperty_rank':
        parameters['similarity'] = 'downhot'
        parameters['k'] = [20,40]
        parameters['N'] = 16
        parameters['weight'] = [0, 0.3, 0.6, 0.3, 0.1]
    elif recommend_engine == 'RecommendUserCF&ItemCF_rank':
        parameters['k'] = [20,40]
        parameters['N'] = 16
    else:
        return None

    return parameters


def getparaters(recommend_engine):
    return MovieLens1MParameters(recommend_engine)


class RecommendAndParameterTest(unittest.TestCase):
    def test_usercf_property_sim(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        read_filepath_users = project_filepath + '/dataset/MovieLens/1m/users.dat'
        data_std_user = MovieLensRatings2Std(read_filepath_users, lines=100)

        recommend_engine = 'RecommendUserCF&UserProperty_similarity'
        parameters = getparaters(recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_user=data_std_user, repeat_k=3, parameters=parameters)

    def test_usercf_property_rank(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)
        read_filepath_users = project_filepath + '/dataset/MovieLens/1m/users.dat'
        data_std_user = MovieLensRatings2Std(read_filepath_users, lines=100)

        recommend_engine = 'RecommendUserCF&UserProperty_rank'
        parameters = getparaters(recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_user=data_std_user, repeat_k=3, parameters=parameters)

    def test_usercf_itemcf(self):
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100user.dat'
        data_std = MovieLensRatings2Std(read_filepath)

        recommend_engine = 'RecommendUserCF&ItemCF_rank'
        parameters = getparaters(recommend_engine)


        #RecommendAndParameterHighSpeed(data_std, recommend_engine, repeat_k=3, parameters=parameters)

    def test_dataframe(self):
        a = DataFrame([[1,1],[1,2]], columns=[1,0],index=[0,1])
        print(a)
        b = DataFrame(1, columns=[0, 1], index=[0, 1])
        print(b)
        b = a+b
        print(b)