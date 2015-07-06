#!/usr/bin/env python3.4
import math
import pickle
import re
import subprocess
import sys


if not len(sys.argv) > 1:
	sys.stderr.write("Usage: %s dumps/*.bz2\n" % sys.argv[0])
	sys.exit(1)


line_trans = str.maketrans('–’', "-\'")
words_split_re = re.compile(r'[^\w\-\']')
is_word_re = re.compile(r'^\w.*\w$')
not_is_word_re = re.compile(r'.*\d.*')


# collect data

word_freq = {}

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
				continue
			line = line.decode('utf-8')
			line = line.translate(line_trans)
			line = line.lower()
			for word in filter(None, words_split_re.split(line)):
				if is_word_re.match(word) and not not_is_word_re.match(word):
					if word in word_freq:
						word_freq[word] += 1
					else:
						word_freq[word] = 1

# save raw data

words = list(word_freq.keys())
words.sort(key=lambda w: word_freq[w], reverse=True)
with open('wordfreq.txt', 'w') as f:
	for word in words:
		f.write("%s %d\n" % (word, word_freq[word]))

# save logarithmic pickle for Viterbi

total_words = sum(word_freq.values())
for word in words:
	word_freq[word] = math.log(float(word_freq[word]) / total_words)
pickle.dump(word_freq, open('wordfreq_log.pickle', 'wb'))
