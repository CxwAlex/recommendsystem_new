import unittest
from recommendsystem.utils import *

user_item_tag = [
    ["user1", "如何学习python", ["python", "编程", "自学"]],
    ["user1", "如何使用python编程", ["python",  "编程"]],
    ["user2", "Hadoop核心技术", ["Hadoop", "大数据"]],
    ["user2", "python进行数据分析", ["python", "数据分析"]],
    ["user2", "大数据数据分析", ["大数据", "数据分析"]],
    ["user3", "刀剑神域", ["动画片", "刀剑"]],
    ["user3", "如何学习python", ["python"]],
    ["user3", "微波炉菜谱", ["做饭", "生活", "菜谱"]]
]



class UtilsTest(unittest.TestCase):

    def test_count_set(self):
        train = [0, 1, 2, 3, 0]
        result = count_set(train)
        self.assertEqual(result, 3)

    def test_get_user_item_tag(self):
        result = get_user_item_tag(user_item_tag)
        #self.assertEqual(result[1][1],'微波炉菜谱')

    def test_get_user_tags(self):
        train = get_user_tags(user_item_tag)
        self.assertEqual(train["user2"]["数据分析"], 2)

    def test_get_item_tags(self):
        train = get_item_tags(user_item_tag)
        self.assertEqual(train["如何学习python"]["python"], 2)

    def test_get_user_item(self):
        train = get_user_item(user_item_tag)
        self.assertEqual(train["user3"]["微波炉菜谱"], 1)

    def test_count_tags(self):
        train = count_tags(user_item_tag)
        self.assertEqual(train["python"], 4)

    def test_split_data(self):
        #train,test = SplitData(user_item_tag)
        #print("test_split_data")
        #print(train)
        #print(test)
        return None

    def test_datediff(self):
        date1 = '2018-11-11'
        date2 = '2008-08-08'
        diff = datediff(date1, date2)
        self.assertEqual(diff, 3747)
        diff2 = datediff(date1, date2, return_type='year')
        self.assertEqual(diff2, 10.27)