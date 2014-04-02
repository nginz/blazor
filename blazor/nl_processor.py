import nltk
import simplejson
import preprocess
from postag import pos_tagger
from chunk_extract import chunker
from sentiment_analyze import sentiment_class

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

def traverse(t, phrases):
  try: 
    t.node 
  except AttributeError: 
    return 
  else: 
    if t.node == 'NP' or t.node == 'VP': 
      phrases.append([normalise(w) for w,tag in t.leaves()])
    else: 
      for child in t: 
        traverse(child, phrases) 

def process(raw_transcript):
  transcript_json = simplejson.loads(raw_transcript)
  utterances = preprocess.parse_transcript(transcript_json)
  pos_sent_count = 0
  neg_sent_count = 0
  phrases = []
  for utterance in utterances:
    for sentence in utterance.sentences:
      if len(sentence) > 10:
        sentence_words = nltk.word_tokenize(sentence)
        sentiment = sentiment_class(sentence_words)
        if sentiment == 'pos':
          pos_sent_count += 1
        else:
          neg_sent_count += 1
        tagged_words = pos_tagger.tag(sentence_words)
        ### Chunking
        chunks = chunker.parse(tagged_words)
        traverse(chunks, phrases)

  return (phrases, pos_sent_count, neg_sent_count)