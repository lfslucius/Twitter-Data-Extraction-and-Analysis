"""
File: trendiness_postgres.py
Name: Group
---------------------------
This file compute the trendiness score by combining 
the works from previous part.The user will input a word 
and will return the trendiness score of that word.
"""

import argparse
import itertools
import collections
import pandas as pd
import psycopg
import datetime
import math

conn = psycopg.connect("dbname=tweets")

def get_most_recent_timestamp():
	cur = conn.cursor()
	
	query = """
	
	select time_stamp
	from tweets
	order by time_stamp desc
	limit 1
	"""
	
	cur.execute(query)
	for row in cur:
		time = row
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	
	current_time = time[0]
		
	return current_time


# Value for the Current Time	
def count_freq_word_current(word, time, res):
	wc_count = 0
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup1 = timestamp + datetime.timedelta(seconds = -timestamp.second)
	#print("Current Time Group:" , timegroup1)

	for i in res:
		if i[2] == word and i[1] == timegroup1:
			wc_count = wc_count + i[3]
	#print(wc_count)
	return(wc_count)
	 
def unique_vocabulary_size_current(time, res):	
	WORD_DICT = {}
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup1 = timestamp + datetime.timedelta(seconds = -timestamp.second)
	#print("Current Time Group:" , timegroup1)

	for i in res:
		if i[1] == timegroup1 and i[2] not in WORD_DICT:
			#vocabulary_size += 1
			WORD_DICT[i[2]] = 1   
		else:
			pass
	V1 = len(WORD_DICT)
	#print(V1)
	return(V1)	


def count_total_word_current(time, res):
	twc_count = 0
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup1 = timestamp + datetime.timedelta(seconds = -timestamp.second)
	#print("Current Time Group:" , timegroup1)

	for i in res:
		if i[1] == timegroup1:
			twc_count = twc_count + 1
	
	#print(twc_count)
	return(twc_count)	
	
# Value for the Prior Time	
def count_freq_word_prior(word, time, res):
	wp_count = 0
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup2 = timestamp + datetime.timedelta(minutes = -1, seconds = -timestamp.second)
	#print("Prior Time Group:" , timegroup2)

	for i in res:
		if i[2] == word and i[1] == timegroup2:
			wp_count = wp_count + i[3]

	#print(wp_count)
	return(wp_count)

def unique_vocabulary_size_prior(time, res):	
	WORD_DICT2 = {}
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup2 = timestamp + datetime.timedelta(seconds = -timestamp.second)
	#print("Prior Time Group:" , timegroup2)

	for i in res:
		if i[1] == timegroup2 and i[2] not in WORD_DICT2:
			#vocabulary_size += 1
			WORD_DICT2[i[2]] = 1   
		else:
			pass
	V2 = len(WORD_DICT2)
	#print(V2)
	return(V2)
def count_total_word_prior(time, res):
	twp_count = 0
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup2 = timestamp + datetime.timedelta(minutes = -1, seconds = -timestamp.second)
	#print("Prior Time Group:" , timegroup2)

	for i in res:
		if i[1] == timegroup2:
			twp_count = twp_count + 1

	#print(twp_count)
	return(twp_count)
	
def trendiness_score(wc_count, V1, twc_count, wp_count, V2, twp_count):
	Trendiness_Score = math.log10((1+wc_count)/(V1+twc_count))-math.log10((1+wp_count)/(V1+twp_count))
	return(Trendiness_Score)

# Prepare to Calculate Trendiness Score
def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-w','--word', type=str, help='enter your word -w word and phrase -w "phrase" ')
	#parser.add_argument('---timestamp', type=str, help='enter your word -timestamp "time"')
	args = parser.parse_args()
	
	word = args.word
	time= get_most_recent_timestamp()
	
	print("The Word is:", word)
	print("The Current Time is:", time)
	
	#load data from database
	cur = conn.cursor()
	
	query = """
	
	select time_stamp, time_group, word, word_count 
	from tweets;
	"""
	cur.execute(query)
	res = []
	for row in cur:
		#dic = dict(zip(keys, row))
		row = list(row)
		res.append(row)
	
	conn.commit()	
	cur.close()
		
	wc = count_freq_word_current(word, time, res)
	V1 = unique_vocabulary_size_current(time, res)	
	twc = count_total_word_current(time, res)
	wp = count_freq_word_prior(word, time, res)
	V2 = unique_vocabulary_size_prior(time, res)
	twp= count_total_word_prior(time, res)
	print("The Trendiness Score of", word, "is:", trendiness_score(wc, V1, twc, wp, V2, twp))
        
if __name__ == '__main__':
	main()	



