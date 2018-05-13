import unittest
import datetime
from recommendsystem.engine_common import *
from recommendsystem.ETL import raw2std

train1 = {
    #         0  1  2  3  4  5  6  7  8  9
    "user1": [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    "user2": [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    "user3": [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    "user4": [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    "user5": [1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
}


raw_data1 = [
    ["user1", "item1", 0],
    ["user1", "item5", 1],
    ["user2", "item2", 0],
    ["user2", "item3", 2],
    ["user2", "item5", 5],
    ["user3", "item1", 2],
    ["user3", "item3", 3],
    ["user3", "item4", 4]
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
        result = RecommendMostHot(train)
        self.assertEqual(result[0], 1)

    def test_most_hot_today(self):
        a = '2018-5-12'
        b = datetime.date(a)
        print(b)
        '''
        转成datetime处理，处理好了再转成字符串
import datetime
 
b = datetime.datetime.strptime("2016-3-1", "%Y-%m-%d")
c = b + datetime.timedelta(days=-2)
print(c.strftime("%Y-%m-%d"))

>>> a='2015-6-9'

>>> datetimeObj = time.strptime(a, "%Y-%m-%d")

>>> datetimeObj
(2015, 6, 9, 0, 0, 0, 1, 160, -1)
>>> time.strftime("%Y%m%d",datetimeObj)
'20150609'

        '''
        return None

    def test_most_hot_week(self):
        return None

    def test_most_hot_month(self):
        return None

    def test_most_hot_year(self):
        return None

if __name__ == '__main__':
    unittest.main()