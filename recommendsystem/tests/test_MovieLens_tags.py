import unittest
import os
import sys
pwd = os.getcwd()
project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.append(project_filepath)
from recommendsystem.ETL import MovieLensMovies2Std
from recommendsystem.engine_tags import ItemSimilarityTagsList
from recommendsystem.TrainAndTestWorkflow import RecommendAndParameterHighSpeed
from conf.settings import getparaters
'''
class MovieLensTagTest(unittest.TestCase):

    def test_moviesimilarity_tag(self):
        # 当前文件的路径
        read_filepath = project_filepath + '/dataset/MovieLens/1m/movies.dat'
        read_lines = 100
        dataframe = MovieLensMovies2Std(read_filepath, read_lines)
        movie_similarity = ItemSimilarityTagsList(dataframe, '1')
        self.assertEqual(movie_similarity['13'], 0.2)
'''

class MovieLensTagRecommendTest(unittest.TestCase):

    def test_user1k(self):
        # 当前文件的路径
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_1kuser.dat'
        data_std = MovieLensMovies2Std(read_filepath)

        read_filepath_item = project_filepath + '/dataset/MovieLens/1m/movies.dat'
        data_std_item = MovieLensMovies2Std(read_filepath_item)

        recommend_engine = 'RecommendByTags'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_item=data_std_item, parameters=parameters, repeat_k=10)

    def test_user100(self):
        # 当前文件的路径
        read_filepath = project_filepath + '/dataset/MovieLens/1m/ratings_100.dat'
        data_std = MovieLensMovies2Std(read_filepath)

        read_filepath_item = project_filepath + '/dataset/MovieLens/1m/movies.dat'
        data_std_item = MovieLensMovies2Std(read_filepath_item)

        recommend_engine = 'RecommendByTags'
        dataset_name = 'MovieLens1M'
        parameters = getparaters(dataset_name, recommend_engine)

        RecommendAndParameterHighSpeed(data_std, recommend_engine, data_std_item=data_std_item, parameters=parameters, repeat_k=10)




if __name__ == '__main__':
    unittest.main()