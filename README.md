# What is this?

This script processes wikipedia article dumps from https://dumps.wikimedia.org/enwiki/ and gathers the word frequency distribution data. The script uses [wikiextractor](https://github.com/attardi/wikiextractor) to fetch raw text, then strips punctuation marks and normalizes unicode dashes and apostrophes. The script then disregards words that have a digit in them, and only takes words that were used in at least 3 different articles.

The script was inspired by [this article](http://imonad.com/seo/wikipedia-word-frequency-list/) which unfortunately provided very inaccurate data with punctuation marks and other sorts of inaccuracies.

# Usage

Install Git submodules:

    git submodule init && git submodule update

Download the current Wikipedia dumps:

    wget -np -r --accept-regex 'https://dumps.wikimedia.org/enwiki/20150602/enwiki-20150602-pages-articles[0-9].*' https://dumps.wikimedia.org/enwiki/20150602/
    
Collect data:
    
    ./gather_wordfreq.py dumps.wikimedia.org/enwiki/20150602/*.bz2 > wordfreq.txt

# Results

The word frequency data for `enwiki-201506` is provided at [results/enwiki-20150602-words-frequency.txt](results/enwiki-20150602-words-frequency.txt).

# Viterbi data

There is a handly little script included that converts text data into pickled dict of the logarithm of every word's probability, which can further be used for splitting **combinedwords** using Viterbi algorithm.

    ./wordfreq_to_viterbi.py < wordfreq.txt > wordfreq_log.pickle
