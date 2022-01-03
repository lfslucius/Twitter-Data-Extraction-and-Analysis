"""
GB 760 Final Project
File: word_count_postgres.py
Name: Group
---------------------------
This file compute frequencies of words and phrases 
by using psycopg. The user will input a word and will
return the frequency of that word.
"""

import argparse
import itertools
import collections
import pandas as pd
import psycopg
import datetime
from time import gmtime, strftime

conn = psycopg.connect("dbname=tweets")

def count_freq_word(word, time):
	"""
	count the frequency of that word in the current minute
	"""

	cur = conn.cursor()
	
	query = """
	
	select time_stamp, time_group, word, word_count 
	from tweets
	"""
	
	cur.execute(query)
	res = []
	#keys = {"time_stamp","time_group", "word_or_phrase", "count"}
	#keys = {"count", "time_stamp", "word_or_phrase", "time_group"}
	#value = {1,2,3,4}
	#res = dict(zip(keys, value))
	for row in cur:
		#dic = dict(zip(keys, row))
		row = list(row)
		res.append(row)
	
	conn.commit()	
	cur.close()
	
	count = 0
    #word_dict = {}
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup = timestamp + datetime.timedelta(seconds = -timestamp.second)
	print("Current Time Group:" , timegroup)

	for i in res:
		if i[2] == word and i[1] == timegroup:
			count = count + i[3]
	return count

def get_most_recent_timestamp():
	cur = conn.cursor()
	
	query = """
	
	select time_stamp
	from tweets
	order by time_stamp desc
	limit 1;
	"""
	
	cur.execute(query)
	for row in cur:
		time = row
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	
	current_time = time[0]
		
	return current_time

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-w','--word', type=str, help='enter your word -w word and phrase -w "phrase" ')
	#parser.add_argument('---timestamp', type=str, help='enter your word -timestamp "time"')
	args = parser.parse_args()
	
	
	word = args.word
	time = get_most_recent_timestamp()
	print(word)
	print(count_freq_word(word, time))     



        
if __name__ == '__main__':
	main()	



