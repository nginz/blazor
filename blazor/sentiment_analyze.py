import collections, itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist


class SentimentAnalyzer():

  def __init__(self):
    ## Best words feature extraction
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
     
    for word in movie_reviews.words(categories=['pos']):
      word_fd.inc(word.lower())
      label_word_fd['pos'].inc(word.lower())
     
    for word in movie_reviews.words(categories=['neg']):
      word_fd.inc(word.lower())
      label_word_fd['neg'].inc(word.lower())

    pos_word_count = label_word_fd['pos'].N()
    neg_word_count = label_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count
     
    word_scores = {}
     
    for word, freq in word_fd.iteritems():
      pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],
        (freq, pos_word_count), total_word_count)
      neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],
        (freq, neg_word_count), total_word_count)
      word_scores[word] = pos_score + neg_score
     
    best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:10000]
    self.bestwords = set([w for w, s in best])
    self.train_classifier()
 
  def best_word_feats(self, words):
    return dict([(word, True) for word in words if word in self.bestwords])

  def train_classifier(self):
    # Training
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(self.best_word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(self.best_word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    self.sentiment_classifier = NaiveBayesClassifier.train(trainfeats)

  def sentiment_class(self, words):
    features = self.best_word_feats(words)
    class_label = self.sentiment_classifier.classify(features)
    class_prob = self.sentiment_classifier.prob_classify(features).prob(class_label)
    return class_label if class_prob > 0.6 else 'neutral'