import unittest
from recommendsystem.engine_tags import *


#构造原始数据集
raw_data1 = {
    "user1": ["如何学习python", "如何使用python编程", "Spark核心技术"],
    "user2": ["刀剑神域", "微波炉菜谱", "如何做饭"],
    "user3": ["Hadoop核心技术", "大数据处理", "刀剑神域"],
    "user4": ["python进行数据分析", "R语言数据分析", "大数据数据分析"],
    "user5": ["刀剑神域", "龙泉刀剑", "天线宝宝"]
}

item_tag ={
    "如何学习python":["python", "编程", "自学"],
    "如何使用python编程":["python", "编程", "自学"],
    "python进行数据分析":["python", "编程", "数据分析"],
    "大数据处理":["大数据", "Hadoop", "Spark"],
    "R语言数据分析":["R", "编程", "数据分析"],
    "大数据数据分析":["大数据", "数据分析"],
    "Hadoop核心技术":["Hadoop", "大数据"],
    "Spark核心技术":["Spark", "大数据"],
    "刀剑神域":["动画片", "刀剑"],
    "龙泉刀剑":["刀剑", "商品"],
    "天线宝宝":["动画片", "儿童"],
    "微波炉菜谱":["做饭", "生活", "菜谱"],
    "如何做饭":["做饭", "自学", "生活"]
}

tag_item ={
    "python":["如何学习python","如何使用python编程","python进行数据分析"],
    "编程":["如何学习python","如何使用python编程","python进行数据分析","R语言数据分析"],
    "自学":["如何学习python","如何使用python编程","如何做饭"],
    "数据分析":["python进行数据分析","R语言数据分析","大数据数据分析"],
    "大数据":["大数据处理","大数据数据分析","Hadoop核心技术","Spark核心技术"],
    "R":["R语言数据分析"],
    "Hadoop":["大数据处理","Hadoop核心技术"],
    "Spark":["大数据处理","Spark核心技术"],
    "动画片":["刀剑神域","天线宝宝"],
    "刀剑":["刀剑神域","龙泉刀剑"],
    "儿童":["天线宝宝"],
    "做饭":["微波炉菜谱","如何做饭"],
    "生活":["微波炉菜谱","如何做饭"],
    "菜谱":["微波炉菜谱"]
}

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

class SimilarityAndRecommendTest(unittest.TestCase):

    def test_item_similarity(self):
        item_tags = get_item_tags(user_item_tag)
        item_sim = ItemSimilarityTags(item_tags)
        self.assertEqual(item_sim['如何使用python编程']['python进行数据分析'], 0.5)
        item_sim2 = ItemSimilarityTags(item_tags, '如何使用python编程')
        self.assertEqual(item_sim2['python进行数据分析'], 0.5)


    def test_user_similarity(self):
        user_tags = get_user_tags(user_item_tag)
        user_sim = ItemSimilarityTags(user_tags)
        self.assertAlmostEqual(user_sim['user1']['user2'], 0.28867513)
        user_sim2 = ItemSimilarityTags(user_tags, 'user1')
        self.assertAlmostEqual(user_sim2['user2'], 0.28867513)


    def test_tags_similarity(self):
        tags_item = get_item_tags(user_item_tag).T
        tags_sim = TagsSimilarityByItem(tags_item)
        self.assertAlmostEqual(tags_sim['python']['编程'], 0.81649658)
        tags_sim2 = TagsSimilarityByItem(tags_item, 'python')
        self.assertAlmostEqual(tags_sim2['编程'], 0.81649658)


    def test_tags_similarity2(self):
        tags_user = get_user_tags(user_item_tag).T
        tags_sim = TagsSimilarityByUser(tags_user)
        self.assertAlmostEqual(tags_sim['python']['编程'], 0.57735026)
        tags_sim2 = TagsSimilarityByUser(tags_user, 'python')
        self.assertAlmostEqual(tags_sim2['编程'], 0.57735026)


    def test_Recommend(self):
        recommend = RecommendByTags(user_item_tag, 'user1')
        self.assertEqual(recommend,['python进行数据分析'])
        #recommend2 = RecommendByItemSimilarityTags(user_item_tag)
        #print(recommend2)

class RecommendTagTest(unittest.TestCase):

    def test_popular_tag(self):
        rank = RecommendPopularTags(user_item_tag)
        rank2 = RecommendPopularTags(user_item_tag, 2)
        self.assertEqual(rank, ['python'])
        self.assertEqual(rank2[0:1], ['python'])

    def test_item_popular_tag(self):
        rank = RecommendItemPopularTags(user_item_tag, '如何学习python')
        self.assertEqual(rank, ['python'])

    def test_user_popular_tag(self):
        rank = RecommendUserPopularTags(user_item_tag, 'user1', 2)
        self.assertEqual(set(rank), {'python', '编程'})

    def test_hybrid_popular_tag(self):
        result1 = RecommendHybridPopularTags('user2', '刀剑神域', user_item_tag,N=2)
        self.assertAlmostEqual(set(result1), {'大数据', '数据分析'})

    def test_similarity_tag(self):
        result1 = RecommendSimilarityTags(user_item_tag, 'python')
        self.assertAlmostEqual(result1, ['编程'])

    def test_recommend_tags(self):
        result = RecommendTags(user_item_tag)
        self.assertEqual(result, ['python'])
        #result1 = RecommendTags(user_item_tag, user='user1')
        #self.assertEqual(result1, ['python'])
        result2 = RecommendTags(user_item_tag, item='如何学习python')
        self.assertEqual(result2, ['python'])
        result3 = RecommendTags(user_item_tag, tag='python')
        self.assertEqual(result3, ['编程'])

if __name__ == '__main__':
    unittest.main()
