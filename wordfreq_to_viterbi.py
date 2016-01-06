#!/usr/bin/env python3
import math
import pickle
import sys


word_uses = {}

for line in sys.stdin:
	word, uses = line.split()
	word_uses[word] = int(uses)

total_words = sum(word_uses.values())
word_freq_log = {}
for word, uses in word_uses.items():
	word_freq_log[word] = math.log(float(uses) / total_words)
pickle.dump(word_freq_log, sys.stdout.buffer)
