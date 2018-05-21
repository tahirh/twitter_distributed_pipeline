from __future__ import print_function
import sys
import json
import datetime
import random

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def get_polarity(tweet):
    # Later use natural lang but this
    # from textblob import TextBlob
    # try:
    #     tblob = TextBlob(tweet)
    #     return tblob.polarity()
    return get_ticker(tweet), random.random()


def get_ones(tweet):
    return get_ticker(tweet), 1


def get_ticker(tweet):
    if 'microsoft' in tweet.lower():
        return "msft"
    else:
        return "ibm"


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: consumer.py <kafka-host> <topic-name> <seconds>")
        exit(-1)

    kafka_host = sys.argv[1]
    topic_name = sys.argv[2]
    seconds = int(sys.argv[3])

    conf = SparkConf() \
        .setAppName("data_challenge")

    from pyspark_cassandra import CassandraSparkContext

    sc = CassandraSparkContext(conf=conf)
    sc.setLogLevel('ERROR')
    ssc = StreamingContext(sc, seconds)
    ssc.checkpoint('./output')

    d = dict()
    d['bootstrap.servers'] = kafka_host
    d['group.id'] = 'test-id'
    d['enable.auto.commit'] = 'false'

    kafka_stream = KafkaUtils.createDirectStream(ssc, [topic_name], d)

    # Parse messages as json
    tweets = kafka_stream.map(lambda v: json.loads(v[1]))
    tweets_text = tweets.map(lambda tweet: json.loads(tweet)['text'].encode('ascii', 'ignore'))

    totals = tweets_text \
        .map(lambda tweet: get_ones(tweet)) \
        .reduceByKey(lambda x, y: x + y)

    polars = tweets_text \
        .map(lambda tweet: get_polarity(tweet)) \
        .reduceByKey(lambda x, y: x + y)

    avgs = polars.join(totals).mapValues(lambda v: v[0] / v[1]).map(lambda x: (x[0], datetime.datetime.now(), x[1]))
    avgs.pprint()

    # Save result to cassandra
    from pyspark_cassandra.streaming import saveToCassandra
    # from cassandra import ConsistencyLevel

    # saveToCassandra(avgs, 'ratings', 'twitter', consistency_level=ConsistencyLevel.LOCAL_QUORUM)
    saveToCassandra(avgs, 'ratings', 'twitter', consistency_level=6)

    ssc.start()
    ssc.awaitTermination()
