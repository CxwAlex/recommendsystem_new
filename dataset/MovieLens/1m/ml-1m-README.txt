概要
================================================== ==============================

这些文件包含大约3,900部电影的1,000,209个匿名评级
由2000年加入MovieLens的6,040名MovieLens用户制作。


引用
================================================== ==============================

要承认在出版物中使用数据集，请引用以下内容
纸：

F. Maxwell Harper和Joseph A. Konstan。 MovieLens数据集：历史
和上下文。 ACM交互式智能系统（TiiS）交易5，4，
第19条（2015年12月），19页。 DOI = HTTP：//dx.doi.org/10.1145/2827872


评分文件描述
================================================== ==============================

所有的评级都包含在文件“ratings.dat”中，并在
格式如下：

用户名:: MovieID ::评级::时间戳

- 用户标识介于1和6040之间
- MovieID的范围介于1和3952之间
- 评分是按5星级评分（仅限全星级评分）
- 时间戳记由时间（2）返回时代以秒为单位表示，
- 每个用户至少有20个评分

用户文件描述
================================================== ==============================

用户信息位于文件“users.dat”中，如下所示
格式：

用户名::性别：年龄::职业::邮政编码

所有人口统计信息由用户自愿提供，并且是
没有检查准确性。只有提供了一些人口统计的用户
信息包含在这个数据集中。

- 性别由男性表示为“M”，女性表示为“F”
- 年龄从以下范围中选择：

* 1：“18岁以下”
* 18：“18-24”
* 25：“25-34”
* 35：“35-44”
* 45：“45-49”
* 50：“50-55”
* 56：“56+”

- 职业选择如下选择：

* 0：“其他”或未指定
* 1：“学术/教育者”
* 2：“艺术家”
* 3：“文员/管理员”
* 4：“大学/研究生”
* 5：“客户服务”
* 6：“医生/保健”
* 7：“行政/管理”
* 8：“农民”
* 9：“家庭主妇”
* 10：“K-12学生”
* 11：“律师”
* 12：“程序员”
* 13：“退休”
* 14：“销售/市场营销”
* 15：“科学家”
* 16：“个体经营”
* 17：“技术人员/工程师”
* 18：“匠人/工匠”
* 19：“失业”
* 20：“作家”

712/5000
电影文件描述
================================================================================

电影信息在文件“movies.dat”中，并且具有以下格式：
MovieID :: Title :: Genres
-标题与由IMDB提供的标题相同（包括发行年份） 
- 流派由管道分隔并且从 以下类型：
*动作
*冒险
*动画
*儿童
*喜剧
*犯罪
*纪录片
*戏剧
*幻想
*电影黑色
*恐怖
*音乐
*神秘
*浪漫
*科幻
*惊悚
*战争
*西方 
- 一些MovieIDs不对应 由于偶然重复入场和/或测试条目而导致的电影 - 电影大部分是手工输入的，因此可能存在错误和不一致