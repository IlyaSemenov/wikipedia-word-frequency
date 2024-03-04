# Wikipedia word frequency generator

This script processes wikipedia article dumps from https://dumps.wikimedia.org/enwiki/ and gathers the word frequency distribution data. The script uses [wikiextractor](https://github.com/attardi/wikiextractor) to fetch raw text, then strips punctuation marks and normalizes unicode dashes and apostrophes. The script then disregards words that have a digit in them, and only takes words that were used in at least 3 different articles.

The script was inspired by [this article](http://imonad.com/seo/wikipedia-word-frequency-list/) which unfortunately provided very inaccurate data with punctuation marks and other sorts of inaccuracies.

## Usage

The script needs Python 3. On macOS, [there is a known bug with Python 3.8](https://github.com/GoogleCloudPlatform/gsutil/issues/961#issuecomment-604648510), so you will need to use Python 3.7 or lower.

Install requirements:

```sh
pip install -r requirements.txt
```

Download the current Wikipedia dumps for the desired language:

```sh
WIKI=enwiki
wget -np -r --accept-regex \
  "https:\/\/dumps\.wikimedia\.org\/${WIKI}\/latest\/${WIKI}-latest-pages-articles[0-9]*\.xml.bz2" \
  https://dumps.wikimedia.org/${WIKI}/latest/
```

_Note that for enwiki (as of April 2023) this will require about 19 Gb of free space._

Parse dumps and save results:

```sh
python ./gather_wordfreq.py dumps.wikimedia.org/${WIKI}/latest/*.bz2 > wordfreq.txt
```

## Pre-generated word frequency data

The word frequency data for English, Spanish, French, German, Italian, Portuguese, Dutch, Arabic, Polish, Egyptian, Japanese, Russian, Cebuano, Swedish, Ukrainian, Vietnamese, Chinese, Waray, Afrikaans & Swahili are provided at [results](results).

English results:

* Total unique words appearing at least in 3 articles: 2747823
* Top 20 most popular words: the, of, in, and, a, to, was, is, on, for, as, with, by, he, that, at, from, his, it, an.
