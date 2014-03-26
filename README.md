Blazor
======
A Voci V-Blaze Natural Language Processor

Prerequisites
-------------
- **Python 2.7**
- **NLTK 2.0** (with data)
- **simplejson**

Installation
-------------
 > pip install blazor

NLTK data packages are required as well. For installation instructions see http://www.nltk.org/data.html.

----------
The transcript output of the V-Blaze web service is parsed and processed as follows:

Preprocessing
-------------
This is where the transcript generated from the Voci V-Blaze is loaded, tokenized into full sentences and cleaned from vocal tags (`<s>`, `++BRTH++`, `++AH++`, etc.). Call is divided into `Utterance`s, each utterance contains its respective properties (`id`, `confidence`, `start`, `end`, `channel`, `sentiment`, `gender`, `breath_count`, `silence_count`, and `sentences`).

Part of Speech Tagging
----------------------
In this step, each word in each sentence is assigned its respective [Treebank POS][1] tag in preparation for chunck extraction. 

Chunk Extraction
----------------
POS Tags generated are utilized by a Chunk Parser to extract Noun Phrases and Verb Phrases from sentences which are traversed and saved to be later indexed.

Sentiment Analysis
------------------
A Sentiment Analyzer is trained on movie reviews and then utilized to classify (using NaiveBayesClassifier) each utterance sentence to one of `pos` or `neg` classes. Positive and Negative fractions are then stored for later indexing.


  [1]: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html/%22Treebank%20POS%22