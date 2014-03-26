import nltk.chunk
from nltk.corpus import conll2000

test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP', 'VP'])
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP', 'VP'])


class ChunkParser(nltk.chunk.ChunkParserI):
  def __init__(self, train_sents):
    train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
    u_chunker = nltk.tag.UnigramTagger(train_data)
    ut_chunker = nltk.tag.TrigramTagger(train_data, backoff=u_chunker)
    utb_chunker = nltk.tag.BigramTagger(train_data, backoff=ut_chunker)
    self.tagger = utb_chunker

  def parse(self, sentence):
    pos_tags = [pos for (word,pos) in sentence]
    tagged_pos_tags = self.tagger.tag(pos_tags)
    chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
    conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
    return nltk.chunk.util.conlltags2tree(conlltags)

chunker = ChunkParser(train_sents)