# encoding=utf-8
import unittest

'''
#records[i] = [u, i, rui, pui]
records = [
    [1, 1, 2, 0],
    [1, 2, 1, 1],
    [2, 1, 0, 0],
    [2, 2, 0, 0]
]

test = [
    [1,[1,1,1,1],[0,0,1,1]],
    [2,[0,0,0,0],[1,1,0,0]]
]

p1 = [
    [1, 0.5],
    [2, 0.5]
]
class NumTest(unittest.TestCase):

    def test_rmse_and_mae(self):
        rmse = RMSE(records)
        mae = MAE(records)
        self.assertEqual(rmse, 1)
        self.assertEqual(mae, 0.5)

    def test_precision_and_recall(self):
        result = PrecisionRecall(test, 4)
        precison = result[0]
        recall = result[1]
        self.assertEqual(precison, 0.5)
        self.assertEqual(recall, 0.5)
    '''
'''
    def test_gini(self):
        gini1 = GiniIndex(p1)
        #mae = MAE(records)
        self.assertEqual(gini1, 0)
        #self.assertEqual(mae, 6)
    '''
'''
# encoding=utf-8
import unittest
import os

from book.cf2 import *


#构造原始数据集
raw_data1 = {
    "user1": ["item1", "item2", "item3"],
    "user2": ["item1", "item4", "item5"],
    "user3": ["item2", "item6", "item7"],
    "user4": ["item3", "item4", "item6"],
    "user5": ["item5", "item6", "item7"]
}

raw_data2 = {
    "user1": [1, 1, 1, 0, 0, 0, 0],
    "user2": [1, 0, 0, 1, 1, 0, 0],
    "user3": [0, 1, 0, 0, 0, 1, 1],
    "user4": [0, 0, 1, 1, 0, 1, 0],
    "user5": [0, 0, 0, 0, 1, 1, 1]
}


std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7"]


class SplitDataTest(unittest.TestCase):

    def test_split_data(self):
        data = [
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]
        ]
        result = SplitData(data, 10, 3)
        len_train = len(result[0])
        len_test = len(result[1])
        print(len_test, len_train)
        self.assertEqual(len_train, 66)

class DataTest(unittest.TestCase):

    def test_recall(self):
        train = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        test = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        recall = Recall(train, test, 3)
        self.assertEqual(recall, 1)


    def test_precision(self):
        train = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        test = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        precision = Precision(train, test, 3)
        self.assertEqual(precision, 1)

    def test_coverage(self):
        train = {
            1: [0, 1, 2],
            2: [3, 4, 5],
            3: [6, 7, 8],
            4: [9, 0, 1]
        }
        coverage = Coverage(train, 3)
        self.assertEqual(coverage, 0.1)

    def test_popularity(self):
        train = {
            1: [0, 1, 2],
            2: [3, 4, 5],
            3: [6, 7, 8],
            4: [9, 0, 1]
        }
        popularity = Popularity(train, 3)
        print(popularity)
        #self.assertEqual(popularity, 1)
'''

if __name__ == '__main__':
    unittest.main()
