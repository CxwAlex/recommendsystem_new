import unittest

from recommendsystem.summary_log import *

log_path = 'Log_usercf1000/'

filepath = [
    'RecommendUserCF_k=5_N=5_similarity=downhot.log',
'RecommendUserCF_k=10_N=5_similarity=downhot.log',
'RecommendUserCF_k=20_N=5_similarity=downhot.log',
'RecommendUserCF_k=40_N=5_similarity=downhot.log'
]


class SummaryLogTest(unittest.TestCase):
    def test_summary_log(self):
        result = {}
        for i in filepath:
            read_filepath = 'F:/' + log_path + i
            result[i] = SummaryLog(read_filepath)
            print(i, result[i])