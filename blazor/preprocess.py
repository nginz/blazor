import re
from nltk import tokenize


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
    if utterance['sentiment'] == 'Positive':
      self.sentiment =  Sentiment.Positive
    elif utterance['sentiment'] == 'Negative':
      self.sentiment =  Sentiment.Negative
    else:
      self.sentiment = Sentiment.Unknown

    if utterance['gender'] == 'Male':
      self.gender =  Gender.Male
    elif utterance['gender'] == 'Female':
      self.gender =  Gender.Female

    self.sentences = []
    self.breath_count = 0
    self.silence_count = 0
    events = utterance['events']
    sentence_words = []
    vocal_tags = re.compile("^\+\+\D+\+\+$")
    #sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for event in events:
      word = event['word']
      if word == "++BRTH++":
        self.breath_count += 1
        if sentence_words:
          long_sentence = " ".join(sentence_words)
          subsentences = tokenize.sent_tokenize(long_sentence)
          self.sentences.extend(subsentences)
        sentence_words = []
      elif word == "<sil>":
        self.silence_count += 1
      elif vocal_tags.match(word) or word == "<s>" or word == "</s>":
        pass
      else:
        sentence_words.append(word)
    
    if sentence_words:
      self.sentences.append(" ".join(sentence_words))

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