import re
from nltk import tokenize

class TimedString(str):
  _t = 0

  def __new__(cls, string, time):
    ob = super(TimedString, cls).__new__(cls, string)
    ob.time = time
    return ob

  @property
  def time(self):
    return self._t
  @time.setter
  def time(self, val):
    self._t = val

class Sentence(list):
  _s = 0
  _e = 0
  _confidence = 0
  _gender = None
  _channel = 0
  _sentiment = None
  _calculated_sentiment = None
  _emotion = None

  def __new__(cls, lst):
    ob = super(Sentence, cls).__new__(cls, lst)
    return ob

  @property
  def start(self):
    return self._s

  @start.setter
  def start(self, val):
    self._s = val

  @property
  def end(self):
    return self._e

  @end.setter
  def end(self, val):
    self._e = val

  @property
  def confidence(self):
    return self._confidence

  @confidence.setter
  def confidence(self, val):
    self._confidence = val

  @property
  def gender(self):
    return self._gender

  @gender.setter
  def gender(self, val):
    self._gender = val

  @property
  def channel(self):
    return self._channel

  @channel.setter
  def channel(self, val):
    self._channel = val

  @property
  def sentiment(self):
    return self._sentiment

  @sentiment.setter
  def sentiment(self, val):
    self._sentiment = val

  @property
  def calculated_sentiment(self):
    return self._calculated_sentiment

  @calculated_sentiment.setter
  def calculated_sentiment(self, val):
    self._calculated_sentiment = val

  @property
  def emotion(self):
    return self._emotion

  @emotion.setter
  def emotion(self, val):
    self._emotion = val

# Preprocessing & Sentence Tokenization
def Enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

Sentiment = Enum('Positive', 'Negative', 'Unknown')
Gender = Enum('Male', 'Female')
class Utterance:
  def __init__(self, utterance):
    self.id = int(utterance['metadata']['uttid'])
    self.confidence = float(utterance['confidence'])
    self.start = float(utterance['start'])
    self.end = float(utterance['end'])
    self.channel = int(utterance['metadata']['channel'])
    self.emotion =  utterance['emotion']
    self.sentiment =  utterance['sentiment']
    self.gender = utterance['gender']
    self.sentences = []
    self.breath_count = 0
    self.silence_count = 0
    events = utterance['events']
    sentence_words = []
    vocal_tags = re.compile("^\+\+\D+\+\+$")
    #sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for event in events:
      word = event['word']
      time = event['start']
      if word == "++BRTH++":
        self.breath_count += 1
        #if sentence_words:
          #long_sentence = " ".join([w for (w, t) in sentence_words])
          #subsentences = tokenize.sent_tokenize(long_sentence)
          #self.sentences.extend(subsentences)
        if len(sentence_words) > 2:
          sentence = Sentence(sentence_words)
          sentence.start = sentence[0].time
          sentence.end = sentence[-1].time
          sentence.emotion = self.emotion
          sentence.gender = self.gender
          sentence.channel = self.channel
          sentence.confidence = self.confidence
          sentence.sentiment = self.sentiment
          self.sentences.append(sentence)
          sentence_words = []
      elif word == "<sil>":
        self.silence_count += 1
      elif vocal_tags.match(word) or word == "<s>" or word == "</s>":
        pass
      else:
        sentence_words.append(TimedString(word, time))

    if sentence_words:
      sentence = Sentence(sentence_words)
      sentence.start = sentence[0].time
      sentence.end = sentence[-1].time
      sentence.emotion = self.emotion
      sentence.gender = self.gender
      sentence.channel = self.channel
      sentence.confidence = self.confidence
      sentence.sentiment = self.sentiment
      self.sentences.append(sentence)
      sentence_words = []

  def dictify(self):
    return {
      'id': self.id,
      'confidence': self.confidence,
      'start': self.start,
      'end': self.end,
      'channel': self.channel,
      'sentiment': self.sentiment,
      'gender': self.gender,
      'sentences': self.sentences,
      'breath_count': self.breath_count,
      'silence_count': self.silence_count
    }
   

def parse_transcript(transcript):
  utterances = []
  for utterance_json in transcript:
    utterance = Utterance(utterance_json)
    utterances.append(utterance)
  return utterances