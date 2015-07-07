#!/usr/bin/env python3.4
from collections import defaultdict
import math
import pickle
import re
import subprocess
import sys


MIN_ARTICLES = 3
line_trans = str.maketrans('–’', "-\'")
words_split_re = re.compile(r'[^\w\-\']')
is_word_re = re.compile(r'^\w.*\w$')
not_is_word_re = re.compile(r'.*\d.*')


if not len(sys.argv) > 1:
	sys.stderr.write("Usage: %s dumps/*.bz2\n" % sys.argv[0])
	sys.exit(1)


# collect data

word_uses = defaultdict(int)
word_docs = {}

doc_no = 0
for fn in sys.argv[1:]:
	sys.stderr.write("Processing %s\n" % fn)
	with subprocess.Popen(
		"bzcat %s | wikiextractor/WikiExtractor.py --no-templates -o - -" % fn,
		stdout=subprocess.PIPE,
		shell=True
	) as proc:
		while True:
			line = proc.stdout.readline()
			if not line:
				break
			if line.startswith(b'<'):
				doc_no += 1
				continue
			line = line.decode('utf-8')
			line = line.translate(line_trans)
			line = line.lower()
			for word in filter(None, words_split_re.split(line)):
				if is_word_re.match(word) and not not_is_word_re.match(word):
					word_uses[word] += 1
					if not word in word_docs:
						word_docs[word] = {doc_no}
					elif len(word_docs[word]) < MIN_ARTICLES:
						word_docs[word].add(doc_no)

# remove words only used once

for word in list(word_uses.keys()):
	if len(word_docs[word]) < MIN_ARTICLES:
		del word_uses[word]

# save raw data

words = list(word_uses.keys())
words.sort(key=lambda w: word_uses[w], reverse=True)
with open('wordfreq.txt', 'w') as f:
	for word in words:
		f.write("%s %d\n" % (word, word_uses[word]))

# save logarithmic pickle for Viterbi

total_words = sum(word_uses.values())
word_freq_log = {}
for word in words:
	word_freq_log[word] = math.log(float(word_uses[word]) / total_words)
pickle.dump(word_freq_log, open('wordfreq_log.pickle', 'wb'))
