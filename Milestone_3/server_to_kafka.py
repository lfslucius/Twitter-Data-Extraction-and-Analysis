"""
GB 760 Final Project
-----------------------------------------------
File : server_to_kafka.py
Name : Group 4
"""

import tweepy
import time
import re
import json
import argparse
import spacy
import en_core_web_sm
from kafka import KafkaProducer
from json import dumps

#consumer_key = '55iKh2vnoNjRNldmBRi1SAT3e'
#consumer_secret = 'eFIqDQn8mkf0jaXB1PUgtjPHWmDqLewFJTJMVHdxkhcdrgPVKe'
#access_key= '1435726675925405696-rPMEdVKvBBAIMVSWqioNfdf9Rlq0ef'
#access_secret = 'NJAhAqMjYIyoAevVA7t8QWiboX1LVBwr513xNBTRokSyE' 

#consumer_key = '3qWrvwLm9zvnoCyzWLTeR2aId'
#consumer_secret = 'XkTyMQA6UuHDDCGAfFFkYwnq8GFBGufNl9wp2xVwVySgcMUaS0'
#access_key= '1446345551512064001-hF45KENRsXreXQM8fpTMvpqzVjT1cu'
#access_secret = 'Y3EJJ8H2HyQTsPo64cOHVyfodIfkSXIlw5TkLoOc5soPG'

#consumer_key = 'MdPT8FE1medRs4qiGcO5DpCoj'
#consumer_secret = 'o3GAUbb4CszRfg4NYLiT2dI3ZDsKUwi1OUhBET3v8Ab2bpZEmy'
#access_key= '1449101893096071173-Emyuopb5HowwBVLcVqfAiF4WYDQFAV'
#access_secret = 'wYOuQ63STmz31FigUBuWaqhi1zVLUapCiMAfHOEvl8aDI'

consumer_key = 'IPKRCR69GUCKpnaQAqF4s6jRb'
consumer_secret = 'sdTTSjqJon380s2l0d4J32xK3kmfUk4Kcg0cCOQvfI2uAyntYM'
access_key= '1053094051-fKLrJf9fLnggAMLbWGorLVQJzoj3KJ2bMmxB6P9'
access_secret = 'zL3IEZT4mdkmlWnkCzDS6hGS6JNzon4WSXAwJXEpEJh7B'


regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

nlp = spacy.load('en_core_web_sm',  disable=['parser', 'ner'])
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:  
                         dumps(x).encode('utf-8'))

class TweetPrinter(tweepy.Stream):
	def disconnect(self):
		super()

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

	def on_data(self, data):
		decodedData = json.loads(data)
		createdAt = decodedData['created_at']
		formattedCreatedAt = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))
		timegroup = time.strftime("%Y-%m-%d %H:%M", time.strptime(str(createdAt), "%a %b %d %H:%M:%S +0000 %Y"))

		text = decodedData['text']
		text = self.clean_text(text)

		producer.send('gb760', {"created": formattedCreatedAt, "timegroup": timegroup, "tweet":  text})

		# self.split_time_phrase(line, timegroup)
		# self.split_time_word(line, timegroup)


	def on_connection_error(self):
		self.disconnect()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file')
	args = parser.parse_args()

	if args.file is not None:
		pass
	else:
		printer = TweetPrinter(consumer_key, consumer_secret,access_key, access_secret)
		try:			
			printer.sample(languages=['en'])
		except:
			printer.disconnect()


if __name__ == '__main__':
    main()

