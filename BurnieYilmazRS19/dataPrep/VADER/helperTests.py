import unittest
import pandas as pd
from helper.helper import helper

class TestHelper(unittest.TestCase):

    def test_sentimentLabeller(self):
        self.assertEqual(helper.sentimentLabeller(-0.9), "NEG")
        self.assertEqual(helper.sentimentLabeller(-0.6), "NEG")
        self.assertEqual(helper.sentimentLabeller(-0.3), "NEG")
        self.assertEqual(helper.sentimentLabeller(-0.2), "NEU")
        self.assertEqual(helper.sentimentLabeller(0.2), "POS")
        self.assertEqual(helper.sentimentLabeller(0.3), "POS")
        self.assertEqual(helper.sentimentLabeller(0.6), "POS")

    def test_labelCounter(self):
        self.testInput = pd.DataFrame(dict(
            time_stamp = [1, 2,3,4,5,6,7],
            VADER =       ['NEG', 'NEG', 'NEG', 'POS', 'POS', 'NEU', 'NEU']
            ))

        processed = helper.labelCounter(self.testInput,1)

        self.assertEqual(processed['EpochDate'], 1)
        self.assertEqual(processed['NEG'], 3)
        self.assertEqual(processed['POS'], 2)
        self.assertEqual(processed['NEU'], 2)

    def test_labelCounterTerms(self):
        self.testInput = pd.DataFrame(dict(
            time_stamp = [1, 2,3,4,5,6,7],
            tax_VADER =       ['POS', 'NEG', 'NEG', 'POS', 'POS', 'NEU', 'NEU'],
            ban_VADER =       ['NEG', 'NEG', 'NEG', 'POS', 'POS', 'NEU', 'NEU'],
            DMS_VADER =       ['NEU', 'NEG', 'NEG', 'POS', 'POS', 'NEU', 'NEU'],
            bitcoin_VADER =   ['POS', 'POS', 'POS', 'POS', 'POS', 'NEU', 'NEU'],
            ))

        processed = helper.labelCounterTerms(self.testInput,1) 

        self.assertEqual(processed['EpochDate'], 1)
        self.assertEqual(processed['tax_POS'], 3)
        self.assertEqual(processed['ban_NEG'], 3)
        self.assertEqual(processed['DMS_NEU'], 3)
        self.assertEqual(processed['bitcoin_POS'], 5)

    def test_submission_filterer1(self):
        self.testInput = "tax and ban on bitcoin"
        self.assertTrue(helper.submission_filterer(self.testInput , term="tax"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="ban"))
        self.assertFalse(helper.submission_filterer(self.testInput , term="DMS"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="bitcoin"))

    def test_submission_filterer2(self):
        self.testInput = "ban or tax btch in $"
        self.assertTrue(helper.submission_filterer(self.testInput , term="tax"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="ban"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="DMS"))
        self.assertFalse(helper.submission_filterer(self.testInput , term="bitcoin"))

    def test_submission_filterer3(self):
        self.testInput = "For my taxi bank $ or xbt"
        self.assertFalse(helper.submission_filterer(self.testInput , term="tax"))
        self.assertFalse(helper.submission_filterer(self.testInput , term="ban"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="DMS"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="bitcoin"))

    def test_submission_filterer4(self):
        self.testInput = "something in btc"
        self.assertFalse(helper.submission_filterer(self.testInput , term="tax"))
        self.assertFalse(helper.submission_filterer(self.testInput , term="ban"))
        self.assertFalse(helper.submission_filterer(self.testInput , term="DMS"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="bitcoin"))

    def test_submission_filterer5(self):
        self.testInput = "ban of bitcoin"
        self.assertFalse(helper.submission_filterer(self.testInput , term="tax"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="ban"))
        self.assertFalse(helper.submission_filterer(self.testInput , term="DMS"))
        self.assertTrue(helper.submission_filterer(self.testInput , term="bitcoin"))



    def test_categoriser(self):
        def testFilter(submission_text,term): return(True)
        def testProcessor(submission_text): return(1)

        self.assertEqual(helper.categoriser("", filterer=testFilter, processor=testProcessor), 1)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHelper)
    unittest.TextTestRunner(verbosity=2).run(suite)