"""
File: vocabulary_size.py
Name: Group
---------------------------
This file compute and print the number of unique words
used in all the tweets stored in tweets.txt
"""

filename = 'tweets.txt'

WORD_DICT = {}


def count_freq_word(line):
	
	word_ls = line[1].split(" ")  
	for word in word_ls:

		if word not in WORD_DICT:
			if '@' in word:
				pass
			else:
				WORD_DICT[word] = 1   
		else:
			pass


def main():
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			line_l = line.split(",")
			count_freq_word(line_l)

	print('The number of unique word is:', len(WORD_DICT))
 

if __name__ == '__main__':
    main()
	

