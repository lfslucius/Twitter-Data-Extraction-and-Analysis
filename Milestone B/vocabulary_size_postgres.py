"""
File: vocabulary_size_postgres.py
Name: Group
---------------------------
This file calculate the vocabulary size in the current minute. The user need to input a time and will return the vocabulary size.
"""

import argparse
import itertools
import collections
import pandas as pd
import psycopg
import datetime
from time import gmtime, strftime

conn = psycopg.connect("dbname=tweets")

def cal_vocabulary_size(time):
	"""
	calculate the vocabulary sizein the current minute
	"""
	# write your psycopg query here fighting :) 
	# the input time will be "timestamp"
	# so look like below
	# query = """
	#	select * from table where time_stamp == {time}
	# 
	# 	"
	cur = conn.cursor()
	
	query = """
	
	select time_stamp, time_group, word, word_count 
	from tweets;
	
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
	
	WORD_DICT = {}
	#timestamp = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
	timestamp = time
	timegroup = timestamp + datetime.timedelta(seconds = -timestamp.second)
	
	print("Current Time Group:" , timegroup)

	for i in res:
		if i[1] == timegroup and i[2] not in WORD_DICT:
			#vocabulary_size += 1
			WORD_DICT[i[2]] = 1   
		else:
			pass
	
	print('The Vocabulary Size in Current Time Group is', len(WORD_DICT))

	#pass

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
	args = parser.parse_args()
	
	time = get_most_recent_timestamp()
	
	cal_vocabulary_size(time)


        
if __name__ == '__main__':
	main()	



