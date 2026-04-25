# Wikipedia word frequency generator

This script processes wikipedia article dumps from https://dumps.wikimedia.org/enwiki/ and gathers the word frequency distribution data. The script uses [wikiextractor](https://github.com/attardi/wikiextractor) to fetch raw text, then strips punctuation marks and normalizes unicode dashes and apostrophes. The script then disregards words that have a digit in them, and only takes words that were used in at least 3 different articles.

The script was inspired by [this article](http://imonad.com/seo/wikipedia-word-frequency-list/) which unfortunately provided very inaccurate data with punctuation marks and other sorts of inaccuracies.

## Usage

### Option 1: Docker (Recommended)
Using Docker is the easiest way to run this project. It handles all dependencies, bypasses OS-specific bugs (like the macOS Python 3.8 issue), and uses Docker volumes to safely manage the large dump files.

#### 1.Build the Docker Image
From the root of your project directory, run:

```sh
docker build -t wiki-wordfreq .
```

#### 2. Run the Container
Because Wikipedia dumps are huge (e.g., ~19 GB for English), we mount a local ./output directory to the container using -v. This ensures your hard drive doesn't fill up the Docker internal storage and allows you to easily access the results.

Download the current Wikipedia dumps:

```sh
# Create a local output directory
mkdir -p output

# Run the download script (e.g., for English Wikipedia)
docker run -v $(pwd)/output:/data wiki-wordfreq /app/wiki-dump.sh --wiki enwiki
```

Parse dumps and save results:

```sh
docker run -v $(pwd)/output:/data wiki-wordfreq python /app/gather_wordfreq.py /data/dumps.wikimedia.org/enwiki/latest/*.bz2 > output/wordfreq.txt
(Note: You can change enwiki to any other language code, like dewiki or frwiki, in both commands).
```

### Option 2: Local Installation

The script needs Python 3. On macOS, [there is a known bug with Python 3.8](https://github.com/GoogleCloudPlatform/gsutil/issues/961#issuecomment-604648510), so you will need to use Python 3.7 or lower.

Install requirements:

```sh
pip install -r requirements.txt
```

Download the current Wikipedia dumps for the desired language:

```sh
./wiki-dump.sh --wiki enwiki
```

(You can also use the raw wget command directly if you prefer).


_Note that for enwiki (as of April 2023) this will require about 19 Gb of free space._

Parse dumps and save results:

```sh
python ./gather_wordfreq.py dumps.wikimedia.org/${WIKI}/latest/*.bz2 > wordfreq.txt
```

## Pre-generated word frequency data

Word frequency data for the following languages is available in [results](results):

* Afrikaans
* Arabic
* Cebuano
* Chinese
* Dutch
* English
* French
* German
* Italian
* Japanese
* Persian
* Polish
* Portuguese
* Russian
* Spanish
* Swahili
* Swedish
* Ukrainian
* Vietnamese

English results:

* Total unique words appearing at least in 3 articles: 2747823
* Top 20 most popular words: the, of, in, and, a, to, was, is, on, for, as, with, by, he, that, at, from, his, it, an.
