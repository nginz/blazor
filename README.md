Blazor
======
A [Voci V-Blaze][1] Natural Language Processor

Prerequisites
-------------
- **Python 2.7**
- **NLTK 2.0** (with data)

Installation
-------------
 > pip install blazor

NLTK data packages are required as well. For installation instructions see http://www.nltk.org/data.html.

----------
The transcript output of the V-Blaze web service is parsed and processed as follows:

Preprocessing
-------------
This is where the transcript generated from the Voci V-Blaze is loaded, tokenized into full sentences and cleaned from vocal tags (`<s>`, `++BRTH++`, `++AH++`, etc.). Call is divided into `Utterance`s, each utterance contains its respective properties (`id`, `confidence`, `start`, `end`, `channel`, `sentiment`, `gender`, `breath_count`, `silence_count`, and `sentences`).

Sentiment Analysis
------------------
A Sentiment Analyzer is trained on movie reviews and then utilized to classify (using NaiveBayesClassifier) each utterance sentence to one of `pos` or `neg` classes. Positive and Negative fractions are then stored for later indexing.


  [1]: http://www.vocitec.com/solutions/compare.php#blaze