import unittest
import os
from recommendsystem.ETL import *


class ReadFileTest(unittest.TestCase):

    def test_read_file(self):
        # 当前文件的路径
        pwd = os.getcwd()
        read_filepath = pwd + '/test_etl/ratings.dat'
        read = ReadFile(read_filepath, lines=3)
        self.assertEqual(read[1], '1::661::3::978302109\n')


    def test_write_file(self):
        pwd = os.getcwd()
        read_filepath = pwd + '/test_etl/ratings.dat'
        data = ReadFile(read_filepath)
        write_filepath = pwd + '/test_etl/testwritefile.txt'
        num = WriteFile(data, write_filepath)
        self.assertEqual(num, 29595176)


    def test_pickle_read_file(self):
        pwd = os.getcwd()
        read_filepath = pwd + '/test_etl/testwrite.pkl'
        read = PickleReadFile(read_filepath)
        self.assertEqual(read[9], '1::919::4::978301368\n')


    def test_pickle_write_file(self):
        pwd = os.getcwd()
        read_filepath = pwd + '/test_etl/ratings.dat'
        read = ReadFile(read_filepath, lines=10)
        write_filepath = pwd + '/test_etl/testwrite.pkl'
        PickleWriteFile(read, write_filepath)

class MovieLensTest(unittest.TestCase):

    def test_rating2dataframe(self):
        # 当前文件的路径
        pwd = os.getcwd()
        read_filepath = pwd + '/test_etl/ratings.dat'
        read_lines = 100
        dataframe = MovieLensRatings2Dataframe(read_filepath, read_lines)
        self.assertEqual(dataframe['1']['1'], 5)



if __name__ == '__main__':
    unittest.main()