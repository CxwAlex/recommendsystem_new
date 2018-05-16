# encoding=utf-8
import unittest
from recommendsystem.engine_social import *
from recommendsystem.utils import matrix2dataframe, raw2std, graph2dataframe

#构造原始数据集
raw_data_no = {
    "user1": ["user2", "user4", "user9"],
    "user2": ["user1"],
    "user3": ["user6", "user4"],
    "user4": ["user1", "user3", "user7"],
    "user5": ["user8", "user9"],
    "user6": ["user3"],
    "user7": ["user4", "user8", "user10"],
    "user8": ["user5", "user7"],
    "user9": ["user1", "user5", "user10"],
    "user10": ["user7", "user9"],
}

raw_data_yes = {
    "user1": ["user2", "user4", "user9"],
    "user2": ["user3", "user5", "user7"],
    "user3": ["user2", "user10"],
    "user4": ["user2"],
    "user5": ["user1", "user3", "user4", "user6", "user7", "user9"],
    "user6": ["user3", "user8"],
    "user7": ["user1", "user4", "user8"],
    "user8": ["user2","user10"],
    "user9": ["user1", "user4", "user7", "user10"],
    "user10": ["user5", "user8"],
}


#最简单的表示方法：邻接矩阵，一个矩阵把顶点、边还有方向、权重全部搞定

#无向图_列表
train_mat_no = [
    [0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 0]
]

#有向图_字典
train_mat_yes = {
    #         1  2  3  4  5  6  7  8  9  10
    "user1": [0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    "user3": [0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    "user5": [1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    "user6": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    "user7": [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    "user8": [0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    "user9": [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    "user10": [1, 1, 1, 0, 1, 0, 0, 1, 0, 0]
}

#用于生成推荐列表
train_user_item = {
    #         1  2  3  4  5  6  7  8  9  10
    "user1": [0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    "user3": [0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    "user5": [1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    "user6": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    "user7": [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    "user8": [0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    "user9": [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    "user10": [1, 1, 1, 0, 1, 0, 0, 1, 0, 0]
}

class Transform2DataframeTest(unittest.TestCase):

    def test_matrix2dataframe(self):
        dataframe1 = matrix2dataframe(train_mat_no)
        dataframe2 = matrix2dataframe(train_mat_yes)
        self.assertEqual(dataframe1[1][1], 0)
        self.assertAlmostEqual(dataframe2["user1"]["user2"], 1)


    def test_graph2dataframe(self):
        dataframe1 = graph2dataframe(raw_data_no)
        dataframe2 = graph2dataframe(raw_data_yes)
        self.assertEqual(dataframe1["user2"]["user1"], 1)
        self.assertEqual(dataframe2["user5"]["user6"], 1)
        #self.assertAlmostEqual(similarity["user1"]["user2"], 0.3333333)


class SimilarityTest(unittest.TestCase):

    def test_similarity(self):
        train = matrix2dataframe(train_mat_no)
        #print(train)
        similarity = social_similarity(train)
        #print(similarity)

    def test_similarity_no_direction(self):
        train = matrix2dataframe(train_mat_no)
        similarity = similarity_no_direction(train)
        similarity_8 = similarity_no_direction(train, user= 8)
        self.assertAlmostEqual(similarity[8][0], 0.89442719)
        self.assertAlmostEqual(similarity_8[7], 0.57735026)


    def test_similarity_no_direction2(self):
        train= graph2dataframe(raw_data_no)
        similarity = similarity_no_direction(train)
        similarity_8 = similarity_no_direction(train, user="user8")
        self.assertEqual(similarity["user8"]["user10"], 0.5)
        self.assertEqual(similarity_8["user10"], 0.5)


    def test_similarity_have_direction(self):
        train = graph2dataframe(raw_data_no)
        similarity = similarity_have_direction(train)
        self.assertAlmostEqual(similarity["user1"]["user3"], 0.40824829)


class FriendSuggestionTest(unittest.TestCase):

    def test_FriendSuggestion_no_direction(self):
        train = matrix2dataframe(train_mat_no)
        suggestion = FriendSuggestion(train)
        suggestion_N2 = FriendSuggestion(train, N= 2)
        suggestion_N2_8 = FriendSuggestion(train, N= 2, user=8)
        self.assertEqual(suggestion[8][0], 0)
        self.assertEqual(suggestion_N2[9][0], 2)
        self.assertEqual(suggestion_N2_8[1], 4)

    def test_FriendSuggestion_no_direction2(self):
        train= graph2dataframe(raw_data_no)
        suggestion = FriendSuggestion(train)
        suggestion_N2 = FriendSuggestion(train, N=2)
        suggestion_N2_8 = FriendSuggestion(train, N=2, user="user8")
        self.assertEqual(suggestion["user9"][0], "user2")
        self.assertEqual(suggestion_N2["user9"][0], "user2")
        self.assertEqual(suggestion_N2_8.tolist(), ['user10', 'user9'])

    def test_FriendSuggestion_have_direction(self):
        train = graph2dataframe(raw_data_no)
        suggestion = FriendSuggestion(train)
        suggestion_N2 = FriendSuggestion(train, N=2)
        suggestion_N2_8 = FriendSuggestion(train, user="user8", N=2)
        self.assertEqual(suggestion["user1"][0], "user10")
        self.assertEqual(suggestion_N2["user4"][0], "user6")
        self.assertEqual(suggestion_N2_8.tolist(), ['user10', 'user9'])


class SocialRecommendTest(unittest.TestCase):

    def test_FriendSuggestion_have_direction(self):
        train_uu = matrix2dataframe(train_mat_yes)
        train_ui = raw2std(train_user_item)
        result = RecommendSocial(train_uu, train_ui, N=4)
        print(result)
        self.assertEqual(result["user1"][0], 7)
        self.assertEqual(result["user9"][3], 7)

    def test_FriendSuggestion_no_direction(self):
        train_uu = graph2dataframe(raw_data_no)
        train_ui = raw2std(train_user_item)
        result = RecommendSocial(train_uu, train_ui, N=4)
        self.assertEqual(result["user1"][0], 7)
        self.assertEqual(result["user9"][3], 7)


if __name__ == '__main__':
    unittest.main()
