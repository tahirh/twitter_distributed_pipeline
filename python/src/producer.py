from __future__ import absolute_import, print_function
import json
from configparser import RawConfigParser
from kafka import KafkaProducer, SimpleClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

config = RawConfigParser()
config.read('data_challenge.properties')

kafka_config = config['kafka']
twitter_config = config['twitter']


class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send(kafka_config['topic.name'], data)
        print(data)

    # implement this in prod for twitter stream error handling
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    print('Starting Kafka Producer')

    client = SimpleClient(kafka_config['bootstrap.servers'])
    print("Topics found: " + ', '.join(client.topics))
    producer = KafkaProducer(bootstrap_servers=kafka_config['bootstrap.servers'],
                             compression_type=kafka_config['compression.type'],
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    auth = OAuthHandler(twitter_config['consumer.key'],
                        twitter_config['consumer.secret'])

    auth.set_access_token(twitter_config['access.token'],
                          twitter_config['access.token.secret'])

    listener = StdOutListener()
    stream = Stream(auth, listener)
    twitter_topics = config['twitter']['keywords'].split(';')
    stream.filter(track=twitter_topics, languages=['en'])
