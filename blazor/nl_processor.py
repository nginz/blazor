import nltk
import preprocess
from preprocess import TimedString
from preprocess import Sentence
from sentiment_analyze import SentimentAnalyzer

class NLProcessor:
  def __init__(self):
    self.sentiment_analyzer = SentimentAnalyzer()
    print "  * NL Processor Initialized."

  def process(self, transcript_json):
    print ' Blazor processor started...'
    utterances = preprocess.parse_transcript(transcript_json)
    pos_sent_count = 0
    neg_sent_count = 0
    sentences = []
    for utterance in utterances:
      for sentence in utterance.sentences:
        # sentence is a TimedString[]
        if len(sentence) > 2:
          sentences.append(sentence)
          sentiment = self.sentiment_analyzer.sentiment_class(sentence)
          if sentiment == 'pos':
            sentence.calculated_sentiment = "Positive"
          elif sentiment == 'neg':
            sentence.calculated_sentiment = "Negative"
          else:
            sentence.calculated_sentiment = "Neutral"
    return sentences