"""
GB 760 Final Project
-----------------------------------------------
File : server_from_kafka.py
Name : Group 4
"""

from kafka import KafkaConsumer
from json import loads
import psycopg


consumer = KafkaConsumer(
    'gb760',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: x.decode('utf-8'))


def insert_to_table(time, time_group, phrase, count):
	"""
	insert data into database using psycopg
	"""
	conn = psycopg.connect("dbname=tweets")

	list1 = [time, time_group, phrase, count]
	cur = conn.cursor()

	query = """
	
	INSERT INTO tweets(time_stamp, time_group, word, word_count)
	VALUES (%t, %t, %s, %s);
	"""
	cur.execute(query, list1)
	conn.commit()	
	cur.close()
	
	list1 = []


def split_time_word(line, timegroup):
	"""
	split time and words
	"""
	time = line[0]
	words_ls = line[1]

	words_ls = words_ls.strip().split(' ')

	word_count = {}
	for word in words_ls:
		if word in word_count:
			word_count[word] += 1
		else:
			word_count[word] = 1

	for word, count in word_count.items():
		#print(time, timegroup, word, count)
		insert_to_table(time, timegroup, word, count)


def split_time_phrase(line, timegroup):
	"""
	split time and multi-phrase
	"""
	time = line[0]
	words_ls = line[1]

	words_ls = words_ls.strip().split(' ')

	# insert phrase into database
	for i in range(len(words_ls)):
		if i == len(words_ls) - 1:
			pass
		else:
			phrase = words_ls[i] + " " + words_ls[i+1]

			time_group = timegroup
			#print(time, time_group, phrase, 1)
			insert_to_table(time, time_group, phrase, 1)



def main():

	for message in consumer:
		# print(message.value)
		time_stamp = message.value[13:32]
		time_group = message.value[49:65]
		text = message.value[78:-2]
		line = [time_stamp, text]
		
		split_time_phrase(line, time_group)
		split_time_word(line, time_group)


if __name__ == '__main__':
    main()

