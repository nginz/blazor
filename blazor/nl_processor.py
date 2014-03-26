import nltk
import simplejson
import preprocess
from postag import pos_tagger
from chunk_extract import chunker
from sentiment_analyze import sentiment_class


mongo_client = MongoClient()
nlpdb = mongo_client.nlpdb

db_calls = nlpdb.calls

call_id = 45
call = {'id': call_id}

with open('AEP.2007.Q1.json') as transcript_file:    
  transcript_json = simplejson.loads(transcript_file.read())

utterances = preprocess.parse_transcript(transcript_json)

call['utterances'] = [utterance.dictify() for utterance in utterances]
call_dbid = nlpdb.calls.insert(call)
print call_dbid

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

phrases = []
def traverse(t): 
  try: 
    t.node 
  except AttributeError: 
    return 
  else: 
    if t.node == 'NP' or t.node == 'VP': 
      phrases.append([normalise(w) for w,tag in t.leaves()])
    else: 
      for child in t: 
        traverse(child) 

pos_sent_count = 0
neg_sent_count = 0
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
      traverse(chunks)

total_sent_count = pos_sent_count + neg_sent_count
pos_sent_percent = pos_sent_count / total_sent_count
neg_sent_percent = neg_sent_count / total_sent_count
print "Positive Sentiment Percentage: "
print pos_sent_percent
print "Negative Sentiment Percentage: "
print neg_sent_percent
nlpdb.calls.update({'_id': call_dbid}, {"$set": {"phrases": phrases}})
