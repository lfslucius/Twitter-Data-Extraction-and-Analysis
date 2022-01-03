"""
GB 760 Final Project
-----------------------------------------------
File : server_postgres.py
Name : Group 4
This file read the tweets from twitter and 
load into database.
"""

import tweepy
import time
import re
import json
import argparse
import spacy
import en_core_web_sm
import psycopg

consumer_key = '55iKh2vnoNjRNldmBRi1SAT3e'
consumer_secret = 'eFIqDQn8mkf0jaXB1PUgtjPHWmDqLewFJTJMVHdxkhcdrgPVKe'
access_key= '1435726675925405696-rPMEdVKvBBAIMVSWqioNfdf9Rlq0ef'
access_secret = 'NJAhAqMjYIyoAevVA7t8QWiboX1LVBwr513xNBTRokSyE' 
regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

nlp = spacy.load('en_core_web_sm',  disable=['parser', 'ner'])

class TweetPrinter(tweepy.Stream):

	def disconnect(self):
		super()
		self.fileWriter.close()

	def clean_text(self, text):

	  	if type(text) != str:
	  		text = text.decode("utf-8")
	  	doc = re.sub(regex, '', text, flags=re.MULTILINE) # remove URLs
	  
	  	sentences = []
	  	for sentence in doc.split("\n"):
	  		if len(sentence) == 0:
	  			continue
	  		sentences.append(sentence)
	  	doc = nlp("\n".join(sentences))
	  	
	  	doc = " ".join([token.lemma_.lower().strip() for token in doc
	  					if (not token.is_stop)
	  						and (not token.like_url)
	  						and (not token.lemma_ == "-PRON-")
	  						and (not len(token) < 4)])
	  	 
	  	return doc


	def split_time_phrase(self, line, timegroup):
		"""
		split time and multi-phrase
		and insert into database
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
				self.insert_to_table(time, time_group, phrase, 1)


	def split_time_word(self, line, timegroup):
		"""
		split time and words
		and insert into database
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
			self.insert_to_table(time, timegroup, word, count)


	def insert_to_table(self, time, time_group, phrase, count):
		"""
		insert into database using psycopg
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


	def on_data(self, data):
		decodedData = json.loads(data)
		createdAt = decodedData['created_at']
		# formattedCreatedAt = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))
		# timegroup = time.strftime("%Y-%m-%d-%H-%M", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))
		formattedCreatedAt = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))
		timegroup = time.strftime("%Y-%m-%d %H:%M", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))

		text = decodedData['text']
		text = self.clean_text(text)
		line = [formattedCreatedAt, text]

		self.split_time_phrase(line, timegroup)
		self.split_time_word(line, timegroup)


	def on_connection_error(self, status_code):
		self.disconnect()
        

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file')
	args = parser.parse_args()

	if args.file is not None:
		pass
		# for line in args.file:
		# 	decodedData = json.loads(lines)
		# 	createdAt = decodedData['created_at']
		# 	formattedCreatedAt = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))
		# 	text = decodedData['text']
		# 	text = self.clean_text(text)

	else:
		printer = TweetPrinter(consumer_key, consumer_secret,access_key, access_secret)
		#printer.on_data()
		try:			
			printer.sample(languages=['en'])

		except:
			printer.disconnect()


if __name__ == '__main__':
    main()
