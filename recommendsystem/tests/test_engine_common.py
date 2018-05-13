import unittest
from recommendsystem.engine_common import *
from recommendsystem.utils import raw2std, list2dataframe_time

train1 = {
    #         0  1  2  3  4  5  6  7  8  9
    "user1": [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    "user2": [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    "user3": [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    "user4": [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    "user5": [1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
}


raw_data1 = [
    ["user1", "item1", '2018-05-09'],
    ["user1", "item5", '2018-05-11'],
    ["user1", "item2", '2018-05-01'],
    ["user2", "item2", '2018-05-07'],
    ["user2", "item3", '2018-04-01'],
    ["user2", "item5", '2018-04-1'],
    ["user3", "item1", '2018-05-07'],
    ["user3", "item4", '2018-03-21'],
    ["user3", "item2", '2018-05-01']
]


class TransformTest(unittest.TestCase):

    def test_recommend_random(self):
        items = ["item1", "item2", "item3", "item4", "item5"]
        result = RecommendRandom(items, 3)
        self.assertEqual(len(result), 3)

    def test_recommend_cold_start(self):
        train = raw2std(train1)
        cold_start_items = []
        for i in train.index:
            if train.ix[i].any() == 0:
                cold_start_items.append(i)
        result = RecommendRandom(cold_start_items, 3)
        self.assertEqual(len(result), 3)
        self.assertGreater(result[1], 4)

class MostHotTest(unittest.TestCase):

    def test_most_hot(self):
        train = raw2std(train1)
        result = RecommendMostHotEver(train)
        self.assertEqual(result[0], 1)

    def test_most_hot_today(self):
        train = list2dataframe_time(raw_data1)
        result = RecommendMostHotDay(train, date_now='2018-05-11')
        self.assertEqual(result[0], 'item5')

    def test_most_hot_week(self):
        train = list2dataframe_time(raw_data1)
        result = RecommendMostHotWeek(train, date_now='2018-05-11')
        self.assertEqual(result[0], 'item1')


    def test_most_hot_month(self):
        train = list2dataframe_time(raw_data1)
        result = RecommendMostHotMonth(train, date_now='2018-05-11')
        self.assertEqual(result[0], 'item2')

if __name__ == '__main__':
    unittest.main()