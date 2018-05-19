import os
import sys
pwd = os.getcwd()
project_filepath = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")
sys.path.append(project_filepath)
import unittest

from recommendsystem.engine_user_property import *
from recommendsystem.ETL import MovieLensUsers2Std

data_raw = [
'1::F::1::10::48067',
'2::M::56::16::70072',
'3::M::25::15::55117',
'4::M::45::7::02460',
'5::M::25::20::55455',
'6::F::50::9::55117',
'7::M::35::1::06810',
'8::M::25::12::11413',
'9::M::25::17::61614',
'10::F::35::1::95370-111'
]

data_std = []
for i in data_raw:
    j = i.split('::')
    data_std.append(j)

class UserPropertyTest(unittest.TestCase):

    def test_user_property_rank(self):
        weight = [0, 0.3, 0.3, 0.3, 0.1]
        rank = UserSimilarityProperty(data_std, weight)
        self.assertAlmostEqual(rank['1']['2'], 0.08335214)

    def test_friend_suggstion(self):
        weight = [0, 0.3, 0.3, 0.3, 0.1]
        friend = FriendSuggestionUserProperty(data_std, weight, N=3)
        self.assertEqual(friend['1'][0], '10')