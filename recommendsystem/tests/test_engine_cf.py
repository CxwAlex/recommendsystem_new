import unittest
from recommendsystem.engine_cf import *
from recommendsystem.utils import raw2std
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

std_data = raw2std(raw_data2, index= std_index)

class SimilarityTest(unittest.TestCase):

    def test_usersimilarity(self):
        train = std_data
        similarity = UserSimilarityCF(train)
        self.assertEqual(similarity["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity["user1"]["user2"], 0.3333333)

    def test_user_similarity_back(self):
        train = std_data
        similarity_back = UserSimilarityBackCF(train)
        self.assertEqual(similarity_back["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity_back["user1"]["user2"], 0.3333333)

    def test_usersimilarity_down_hot(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index= std_index)
        rank = UserSimilarityDownHotCF(train)
        self.assertAlmostEqual(rank["user1"]["user2"], 0.39509830)

    def test_itemsimilarity(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index= std_index)
        result = ItemSimilarityCF(train)
        self.assertAlmostEqual(result["item1"]["item5"], 0.66666666)

    def test_itemsimilarity_down_hot(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index=std_index)
        result = ItemSimilarityDownHotCF(train)
        #归一化之后的
        #self.assertAlmostEqual(result["item1"]["item8"], 0.56125476)
        #未归一化的
        self.assertAlmostEqual(result["item1"]["item8"], 0.29669934)



class UserCFTest(unittest.TestCase):

    def test_user_recommend(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        #std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        #train = raw2std(train, index= std_index)
        train = raw2std(train)
        print(train)
        result = RecommendUserCF(train, k=2, N=3)
        print(result)
        #self.assertEqual(result["user1"][0], "item8")
        result2 = RecommendUserCF(train, user='user2', k=2, N=3)
        #self.assertEqual(result2[0], "item3")

    def test_recommendation_itemcf(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index=std_index)
        rank = RecommendItemCF(train)
        #self.assertAlmostEqual(rank["user1"]["item5"], 3.15470053)


    def test_PersonalRank(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index=std_index)
        rank = PersonalRank(train, 0.8, 10000)
        self.assertAlmostEqual(rank["user1"]["item1"], 0)
        #注意，随机游走算法的结果会变化，但是随着训练次数的增多，理论上应该不会错
        self.assertGreater(rank["user1"]["item5"], 0.4)

if __name__ == '__main__':
    unittest.main()
