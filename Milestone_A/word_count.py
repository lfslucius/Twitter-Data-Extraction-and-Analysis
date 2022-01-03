"""
File: word_count.py
Name: Group
---------------------------
This file compute frequencies of words and phrases 
by using argparse
"""

import argparse
import itertools
import collections
import pandas as pd
# ngram

FILENAME = 'tweets.txt'
WORD_DICT = {}


def count_freq_word(line):
	"""
	Count the frequency of the words
	"""
	word_ls = line[1].split(" ") 
	store_time_freq_ls = []
	for word in word_ls:

		if word not in WORD_DICT:
			if '@' in word:
				pass
			else:
				WORD_DICT[word] = 1

		else:
			WORD_DICT[word] += 1
	

def read_file(filename, word, mode='Word'):
	"""
	Read the file and count phrase frequency
	"""
	with open(filename, 'r') as f:
		count = 0
		for line in f:
			line = line.strip()

			# count frequency of phrase or word 
			if mode == 'Phrase':
				if word in line:
					count += 1
			if mode == 'Word':
				line_l = line.split(",")
				count_freq_word(line_l)

		if mode == 'Phrase':
			return count


def preprocess_dict():
	new_dict = {}
	for k, v in WORD_DICT.items():
		new_dict[k] = v

	return new_dict

def main():
	# create args
	parser = argparse.ArgumentParser()
	parser.add_argument('-w','--word', help='enter your word -w word and phrase -w "phrase" ', required=False)
	args = parser.parse_args()
	
	word = args.word
	
	# identify whether this is a phrase or word
	phrase = word.split(" ")
	count_phrase = 0
	if len(phrase) > 1:
		# if phrase
		count = read_file(FILENAME, word, mode='Phrase')
		print(f'The frequency of "{word}" : {count}')
	else:
		# if word
		read_file(FILENAME, word, mode='Word')
		if word in WORD_DICT:
			print(f'The frequency of {word} : {WORD_DICT[word]}')
		else:
			print(f'Cannot find the word "{word}"')
	

if __name__ == '__main__':
	main()	



