import nltk.tag
from nltk.tag import brill
from nltk.corpus import brown
 
brown_train = brown.tagged_sents(categories=['reviews'])

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):
  if not backoff:
    backoff = tagger_classes[0](tagged_sents)
    del tagger_classes[0]

  for cls in tagger_classes:
    tagger = cls(tagged_sents, backoff=backoff)
    backoff = tagger

  return backoff

classifier_pos_tagger = nltk.data.load(nltk.tag._POS_TAGGER)

brill_templates = [
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,1)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (2,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,3)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,1)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (2,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,3)),
    brill.ProximateTokensTemplate(brill.ProximateTagsRule, (-1, -1), (1,1)),
    brill.ProximateTokensTemplate(brill.ProximateWordsRule, (-1, -1), (1,1))
]
 
pos_trainer = brill.FastBrillTaggerTrainer(classifier_pos_tagger, brill_templates)
pos_tagger = pos_trainer.train(brown_train, max_rules=100, min_score=3)