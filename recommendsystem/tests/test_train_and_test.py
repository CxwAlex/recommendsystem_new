import unittest

class AssessmentTest(unittest.TestCase):

    def test_recall(self):
        train_dataframe = DataFrame(train)
        test_dataframe = DataFrame(test)
        recall = Recall(train_dataframe, test_dataframe)
        self.assertEqual(recall, 0.4)
        recall2 = Recall(train_dataframe, test_raw)
        self.assertEqual(recall2, 0.4)