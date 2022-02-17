from text.processing import SentenceProcessor, TokenProcessor, TextProcessor
from text.dataHandling import DataHandling
from text.vocabCounter import vocabCounter

import unittest
import pandas as pd
import numpy as np
import nltk
import argparse
import os

class TestSentenceProcessor(unittest.TestCase):

  def setUp(self):
    self.maxDiff = None

  def test_removelongText(self):
    inputText = 'An output of 315951902191635724521399682927361876787467787192396107787861735705962612844759868890550038365422912305053105735840459992872506431777973762075187750361154028889253332034865884696775241482787043755453723990431965375604929697182477126937542690960798607552510854577045604847663191743967817977276981018323510100453405993465673301531927132484001212447956029756006894146550149075547253584839396787157998345904468234062387886316262302234642708595037130199844690230096921117662711881376643102116108067517302984431499136320318687686996101876872813647486577614856732261054816728641106551695015268448457420949111487564540403817905570412049051809125328001375575829051169010292048982639028639653270512710495690024836063553031644891517479823081128725974403405518335006669153878666328183526643586093153221747263254818284842969377671982278882406699668925869245441239039036190489812571457709246963284246632200631838734594138737937938826345414431312130161187308272949843067420473791887350692821910336946943679489281554279071825641965311048459434678054908378469939653052141107969613571925187289512504737897752780513075227211625312849569500957446485762946690919132425939779931574200352055100649668942308049886358560241728174575487264048795434680452852007609836258881971386028021275236364102036493816368275017259937805531620704220364994294907354785817606863880529738821956150553984965355343161390503928153869135251308205974482751646492845368334711268025825205768064984125402377762503901078681009897888443989570556140241342601386176581732921963184181953232888236294156322202958108156648731933396962670851604138908048809977992721626808976365138469297625415414315271068859458541630531952329647001356395131467154847731584477681229204689617578036818075768138631614295042339934749878656487463421491870852702784748139601849948061893061164890653273864071074167837607852288321793624798376157161918710149131546815410140972670273026452412600968661831861649147928673717340104463046219277345727479192902377029686794221318858551231572906846850599186828645746886222719648967912561191055425373756265118502187930935754997295858614878207025683518026640437140809284016959863484099901320104510267234626815115225236554444791646084810405532875124856607611178696775835403846220353892905288477176589871460788256741644766105986512645102058414303319914628420231009446326258803435051451425931201173316548911742997927821107211021799062627634679457664083474311830194882285754515305040592906578025775978112458962400738230317903243639123158780005763776461979046074864617981018948273378590938362716322900418552641976749982367109961643172168367040522989035119488173670922999898496612499465926609474666136369242910174675121607561644384995787372311921370348309173010035189495952043863137930420186230423306608113286347298270166889761649712423052113341629528250896099303795847955592627523674586835320279542951360831860555971432257378748169081265039382375130759154077197046768675191662129754707347066596673645543851950723366157629860897106889452610371443711189502470312431376421650160707379412710667677739906156601921074867889854327595429486999075548042049015982592633006619785022824129800185592649950693365147286785490944000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 or more'
    outputText = 'An output of  or more'

    self.assertEqual(SentenceProcessor.removelongText(inputText),outputText)

  def test_removeURL(self):
    inputText = '[**@kanzure**](https://twitter.com/kanzure/). @John, See this URL:http://something.com/kanzure/abc. It is cool. What do you think @Bob?'
    outputText = '[**@kanzure**] @John, See this URL: It is cool. What do you think @Bob?'

    self.assertEqual(SentenceProcessor.removeURL(inputText),outputText)

  def test_removeHTMLCharacterEntities(self):
    inputText = '&gt;nbsp;amp; &amp;#x200B;the &gt; & #a;'
    outputText = ' the  & #a;'

    self.assertEqual(SentenceProcessor.removeHTMLCharacterEntities(inputText),outputText)

  def test_removeLineJump(self):
    inputText = 'perhaps\n there\nwere two of them \n or more \n\\ or so'
    outputText = 'perhaps  there were two of them   or more   or so'

    self.assertEqual(SentenceProcessor.removePunctuation(SentenceProcessor.removeLineJump(inputText)),outputText)

  def test_removeHandle(self):
    inputText = '[**@kanzure**] email john@pickering.com, tweet @John-34 or look at redditor /u/Bob-123, on /r/Bitcoin'
    outputText = ' email  tweet  or look at redditor  on '

    self.assertEqual(SentenceProcessor.removeHandle(inputText),outputText)

  def test_removeRemovedDeleted_noRemoved(self):
    inputText = 'COINBASE DRAINED MY ACCOUNT [removed they removed my removed] [removed]'
    outputText = 'COINBASE DRAINED MY ACCOUNT [removed they removed my removed] '

    self.assertEqual(SentenceProcessor.removeRemovedDeleted(inputText),outputText)

  def test_removeRemovedDeleted_noDeleted(self):
    inputText = 'COINBASE DRAINED MY ACCOUNT [deleted they deleted my deleted] [deleted]'
    outputText = 'COINBASE DRAINED MY ACCOUNT [deleted they deleted my deleted] '

    self.assertEqual(SentenceProcessor.removeRemovedDeleted(inputText),outputText)

  def test_removeNonASCII(self):
    inputText = 'Emoticons: 😁, 😈, 🙃, the word "naïve" and non-Roman text: 蝴蝶 and ذضثيسس'
    outputText = 'Emoticons: , , , the word "naive" and non-Roman text:  and '

    self.assertEqual(SentenceProcessor.removeNonASCII(inputText),outputText)

  def test_removePunctuation(self):
    inputText = "``` `and **then** he ate** all of the [*apples*] at ~6 o'clock, \"meaning\" -20 (fewer) of them! \\Here [is] some j!bb~sh. Ensure this price doesn't change: $20 \\"
    outputText = " and then he ate all of the apples at 6 o'clock meaning 20 fewer of them Here is some jbbsh Ensure this price doesn't change $20 "

    self.assertEqual(SentenceProcessor.removePunctuation(inputText),outputText)

  def test_removeQuotes(self):
    inputText = "'Hey' So Bob said 'that's cool with me'"
    outputText = "Hey So Bob said that's cool with me"

    self.assertEqual(SentenceProcessor.removeQuotes(inputText),outputText)

  def test_aggregateNumberTypes_dollar(self):
    inputText = "The prices are $ 100 or $1 sometimes 100000$ or 100 $ alternatives might be 10 us dollars 10 dollars 10usd 10 usd usd10 usd 10"
    outputText = "The prices are dollar_marker_symbol 100 or dollar_marker_symbol 1 sometimes 100000 dollar_marker_symbol or 100 dollar_marker_symbol alternatives might be 10 dollar_marker_symbol 10 dollar_marker_symbol 10 dollar_marker_symbol 10 dollar_marker_symbol dollar_marker_symbol 10 dollar_marker_symbol 10"

    #The additional spaces introduced are ignored:
    self.assertEqual(' '.join(SentenceProcessor.aggregateNumberTypes(inputText).split()), outputText)

  def test_standardiseBitcoin(self):
    inputText = "there is btc xbt 100btc bitcoin"
    outputText = "there is bitcoin bitcoin 100 bitcoin bitcoin"

    #The additional spaces introduced are ignored:
    self.assertEqual(' '.join(SentenceProcessor.standardiseBitcoin(inputText).split()),outputText)

  def test_standardiseTransactions(self):
    inputText = "tx 20 tx, not somewordtx or txword tx."
    outputText = "transaction 20 transaction, not somewordtx or txword transaction."
    
    self.assertEqual(SentenceProcessor.standardiseTransactions(inputText), outputText)


  def test_LightningNetwork(self):
    inputText = "ln is the same as ln, lightning network, but not Koln but yes lightning networks"
    outputText = "ln is the same as ln, ln, but not Koln but yes ln"

    self.assertEqual(SentenceProcessor.aggregateLN(inputText), outputText)

  def test_phoneNumber(self):
    inputText = "telephone number phone number number"
    outputText = "phone_number phone_number number"

    self.assertEqual(SentenceProcessor.phoneNumber(inputText), outputText)



class TestTokenProcessor(unittest.TestCase):

  def test_removeStopwords(self):
    inputText = nltk.word_tokenize("she's there you said the watch isn't there at two o'clock")
    outputText = ["said", "watch", "two", "o'clock"]

    self.assertEqual(TokenProcessor.removeStopwords(inputText),outputText)

  def test_lemmatizeAndStem_not_affect_values(self):
    inputList = ["dollar_marker_symbol", "going", "bitcoins"] 
    outputList = ["dollar_marker_symbol", "go", "bitcoin"]

    self.assertEqual(TokenProcessor.lemmatizeAndStem(inputList),outputList)


  def test_mineMinerAgg(self):
    inputList = ["mine", "miner", "miner", "bitcoin"] 
    outputList = ["mine", "mine", "mine", "bitcoin"]

    self.assertEqual(TokenProcessor.mineMinerAgg(inputList), outputList)

class TestTextProcessor(unittest.TestCase):

  def test_1(self):
    inputColumn = ['To me pls.', '[**@kanzure**](https://twitter.com/kanzure/)', "Thanks"]
    expectedOutput = pd.Series([['pls'],  [], ['thank']])
    textSeries = TextProcessor(pd.Series(inputColumn)).processText()
    pd.testing.assert_series_equal(textSeries, expectedOutput) 
    
  def test_2(self):
    inputColumn = [
      "Are you thinking that DNA said someone was naïve? Because he didn't. He was saying that someone else was saying that those who thought the internet was a fad were naïve. (http://www.bbc.co.uk/news/world-europe-45753455)",
      "Some emoticons: 😁, 😈, 🙃",
      "@John, See this URL: https://twitter.com/kanzure/. It is cool. What do you think @Bob?",
      '"It\'s a HUGE deal. It\'s a HUGE, HUGE, HUGE deal" - Billionaire investor in Bitcoin',
      'Plateform...🤦\u200d♂️.',
      "I'm The Lightning Network is cool - ln forever!"

      ]

    expectedOutput = [['think', 'dna', 'say', 'someon', 'naiv', 'say', 'someon', 'els', 'say', 'think', 'internet', 'fad', 'naiv'], 
    ['emoticon'],
    ['see', 'url', 'cool', 'think'],
    ['huge', 'deal', 'huge', 'huge', 'huge', 'deal', 'billionair', 'investor', 'bitcoin'],
    ['plateform'], ['ln', 'cool', 'ln', 'forev']]

    textSeries = TextProcessor(pd.Series(inputColumn)).processText()

    pd.testing.assert_series_equal(textSeries, pd.Series(expectedOutput) )


  def test_3(self):
    inputColumn = [
      'Will BITCOIN put to shame Gold price (1 oc $1,152.06) in Q1 of 2017?',
    "BTCC's 2016: $158 billion worth of bitcoins traded, $138 million worth of bitcoins mined.",
    "There was ~200USD **and then** -1000 USD, then $ - 100 - but btc isn't 'super' volatile?"
    ]

    expectedOutput = [
      ['bitcoin', 'put', 'shame', 'gold', 'price', '1', 'oc', 'dollar_marker_symbol', '115206', 'q1', '2017'],
      ['btcc', '2016', 'dollar_marker_symbol', '158', 'billion', 'worth', 'bitcoin', 'trade', 'dollar_marker_symbol', 
      '138', 'million', 'worth', 'bitcoin', 'mine'],
      ['200', 'dollar_marker_symbol', '1000', 'dollar_marker_symbol', 'dollar_marker_symbol', '100', 'bitcoin', 'super',
      'volatil']

    ]

    textSeries = TextProcessor(pd.Series(inputColumn)).processText()

    pd.testing.assert_series_equal(textSeries, pd.Series(expectedOutput) )   

  def test_4(self):
    inputColumn = ["Here's the truth: I'll be buying lots of bitcoins tomorrow at 2 o'clock; that'll be nice as long as it isn't going to fall",
    'COINBASE DRAINED MY ACCOUNT. [removed]']
    expectedOutput = [
      ['truth','buy','lot','bitcoin','tomorrow','2',"o'clock",'nice', 'long', 'go', 'fall'], 
      ['coinbas', 'drain', 'account']
    ]

    textSeries = TextProcessor(pd.Series(inputColumn)).processText()

    pd.testing.assert_series_equal(textSeries, pd.Series(expectedOutput) )

class TestDataHandling(unittest.TestCase):

  def setUp(self):
    self.testInput = pd.DataFrame(dict(
      author =     ['rBitcoinMod',    'John',     'John',     'Alice',            'Alice',                     'Ron',                      'Alex'],
      time_stamp = [1,                     2,          3,           4,                  5,                         6,                           7],
      text =       ['moderation', 'bitcoin!', 'bitcoin!', '[deleted]', 'bitcoin[deleted]', 'bitcoins are everywhere', 'ethereum bitcoin litecoin']
    ))
    
    self.testDataObj = DataHandling(data_frame=self.testInput)


  def test_removeExcludedRowsProcessing(self):
    """
    Checks correct rows are excluded
    """
    expectedOutput = pd.DataFrame(dict(
      author = ['John', 'Alice', 'Ron', 'Alex'],
      time_stamp = [2,5, 6, 7],
      text = ['bitcoin!','bitcoin[deleted]', 'bitcoins are everywhere', 'ethereum bitcoin litecoin']
    ))

    self.testDataObj.removeExcludedRows()

    pd.testing.assert_frame_equal(self.testDataObj.getDataList()[0], expectedOutput)
    
  def test_removeExcludedRowsIndex(self):
    """
    Checks index remains from 0 to length of dataset
    """

    self.testDataObj.removeExcludedRows()

    data = self.testDataObj.getDataList()[0]

    self.assertEqual(list(data.index), list(range(len(data))))


  def test_splitData(self):
    """
    Checks data split correctly using step
    """
    expectedOutput = [
      pd.DataFrame(dict(
      author =     ['rBitcoinMod',    'John',    ],
      time_stamp = [1,                     2,    ],
      text =       ['moderation', 'bitcoin!',    ]
    )),
    pd.DataFrame(dict(
      author =     ['John',     'Alice'],
      time_stamp = [3,           4     ],
      text =       ['bitcoin!', '[deleted]']
    )),
    pd.DataFrame(dict(
      author =     ['Alice',                     'Ron'],
      time_stamp = [5,                         6      ],
      text =       ['bitcoin[deleted]', 'bitcoins are everywhere']
    )),
    pd.DataFrame(dict(
      author =     ['Alex'],
      time_stamp = [7],
      text =       ['ethereum bitcoin litecoin']
    ))

    ]

    self.testDataObj.splitData(step=2)

    for i, df in enumerate(self.testDataObj.getDataList()):
      pd.testing.assert_frame_equal(df, expectedOutput[i])


  def test_selectFirstFrame(self):
    """
    Checks error raised when applying single dataframe operation to many
    """
    self.testDataObj.splitData(step=2)
    self.failUnlessRaises(Exception, self.testDataObj.selectFirstFrame)

  def test_aggData(self):
    self.testDataObj.splitData(step=2)
    self.testDataObj.aggData()
    pd.testing.assert_frame_equal(self.testDataObj.selectFirstFrame(), self.testInput)

  def test_collectData(self):
    expectedOutput = [
      pd.DataFrame(dict(
      author =     ['rBitcoinMod',    'John',    ],
      time_stamp = [1,                     2,    ],
      text =       ['moderation', 'bitcoin!',    ]
    ))]

    self.testDataObj.splitData(step=2)
    self.testDataObj.outputDataFrames(folder = 'testing', label = 'test')

    self.testDataObj.collectData(dataPath='/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/', regexpr='test_0', verbose=False)

    pd.testing.assert_frame_equal(self.testDataObj.getDataList()[0], expectedOutput[0])

    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_0.pkl')
    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_1.pkl')
    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_2.pkl')
    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_3.pkl')



  def test_outputDataFrames(self):
    expectedOutput = [
      pd.DataFrame(dict(
      author =     ['rBitcoinMod',    'John',    ],
      time_stamp = [1,                     2,    ],
      text =       ['moderation', 'bitcoin!',    ]
    )),
    pd.DataFrame(dict(
      author =     ['John',     'Alice'],
      time_stamp = [3,           4     ],
      text =       ['bitcoin!', '[deleted]']
    )),
    pd.DataFrame(dict(
      author =     ['Alice',                     'Ron'],
      time_stamp = [5,                         6      ],
      text =       ['bitcoin[deleted]', 'bitcoins are everywhere']
    )),
    pd.DataFrame(dict(
      author =     ['Alex'],
      time_stamp = [7],
      text =       ['ethereum bitcoin litecoin']
    ))

    ]

    self.testDataObj.splitData(step=2)
    self.testDataObj.outputDataFrames(folder = 'testing', label = 'test')

    for i, df in enumerate([pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_0.pkl'), 
                            pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_1.pkl'),
                            pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_2.pkl'),
                            pd.read_pickle('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_3.pkl')]):
      pd.testing.assert_frame_equal(df, expectedOutput[i])

    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_0.pkl')
    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_1.pkl')
    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_2.pkl')
    os.remove('/mnt/c/Users/charl/Desktop/finance_perso/BurnieYilmazRS19/dataPrep/REDDIT/data/processing/testing/test_3.pkl')

class TestVocabCounter(unittest.TestCase):

  def setUp(self):
    self.testInput = pd.DataFrame(dict(
      author =     ['rBitcoinMod',    'John',     'John',     'Alice',            'Alice',                     'Ron',                      'Alex'],
      time_stamp = [1,                     2,          3,           4,                  5,                         6,                           7],
      text =       [['a', 'b', 'c', 'd'], ['a', 'b', 'c'], ['a', 'b'] , ['a', 'a', 'a'], ['b', 'b'], ['c'], ['d']]
    ))

    self.vc = vocabCounter(
      rawData = self.testInput,
      start = 1,
      end = 8,
      step = 1
    )

  def test_init_w_vocab(self): self.assertListEqual(self.vc.getVocab(), ['a', 'b', 'c', 'd'])

  def test_init_w_days(self): self.assertTrue(all(self.vc.getDays() == np.array([[1], [2], [3], [4], [5], [6], [7]])))

  def test_oneTokenPerSubmission(self):
    self.vc.oneTokenPerSubmission()
    for a_list in (self.vc.getRaw().text.tolist()):
      a_list.sort()
    self.assertListEqual(self.vc.getRaw().text.tolist(), [['a', 'b', 'c', 'd'], ['a', 'b', 'c'], ['a', 'b'] , ['a'], ['b'], ['c'], ['d']])

  def test_createCountData(self):
    self.vc.oneTokenPerSubmission()
    self.vc.createCountData(verbose=False)
    pd.testing.assert_frame_equal(
      self.vc.getCountData().loc[:,['a', 'b', 'c', 'd', 'day_time_stamp', 'no_submissions']], 
      pd.DataFrame(dict(
        a =              [1, 1, 1, 1, 0, 0, 0],
        b =              [1, 1, 1, 0, 1, 0, 0],
        c =              [1, 1, 0, 0, 0, 1, 0],
        d =              [1, 0, 0, 0, 0, 0, 1],
        day_time_stamp = [1, 2, 3, 4, 5, 6, 7],
        no_submissions = [1, 1, 1, 1, 1, 1, 1]
      ), dtype='int64')
      )

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--testing', choices=['SentenceProcessor', 'TokenProcessor', 'TextProcessor', 'DataHandling', 'vocabCounter', 'all'], default = 'all')
  args = parser.parse_args()

  if parser.parse_args().testing == 'SentenceProcessor' or parser.parse_args().testing == 'all':
    print("Testing Sentence Processing\n--------------------------- \n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSentenceProcessor)
    unittest.TextTestRunner(verbosity=2).run(suite)

  if parser.parse_args().testing == 'TokenProcessor' or parser.parse_args().testing == 'all':
    print("Testing Token Processing\n--------------------------- \n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTokenProcessor)
    unittest.TextTestRunner(verbosity=2).run(suite)

  if parser.parse_args().testing == 'TextProcessor' or parser.parse_args().testing == 'all':
    print("Testing Text Processing\n--------------------------- \n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTextProcessor)
    unittest.TextTestRunner(verbosity=2).run(suite)

  if parser.parse_args().testing == 'DataHandling' or parser.parse_args().testing == 'all':
    print("Testing Data Handling\n--------------------------- \n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataHandling)
    unittest.TextTestRunner(verbosity=2).run(suite)

  if parser.parse_args().testing == 'vocabCounter' or parser.parse_args().testing == 'all':
    print("Testing vocabCounter functions\n--------------------------- \n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVocabCounter)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
