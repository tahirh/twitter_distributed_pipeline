#  My Cheat Sheet


Login to bash:
````
docker-compose exec kafka /usr/bin/env bash
````
or
````
docker exec -it cassandra-seed-node /bin/bash
````

Create topic:
````
docker-compose exec kafka /opt/kafka_2.11-0.10.1.1/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic twitter-data
````

List topics:
````
docker-compose exec kafka /opt/kafka_2.11-0.10.1.1/bin/kafka-topics.sh --list --zookeeper zookeeper:2181
````

Get producer:
````
docker-compose exec kafka /opt/kafka_2.11-0.10.1.1/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic twitter-data
````

Get consumer:
````
docker-compose exec kafka /opt/kafka_2.11-0.10.1.1/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic twitter-data --from-beginning
````

Submit job to spark:

````
docker-compose exec master spark-submit --jars /src/spark-streaming-kafka-0-8-assembly.jar --packages anguenot:pyspark-cassandra:0.7.0 --conf spark.cassandra.connection.host=cassandra -seed-node /src/consumer.py kafka:9092 twitter-data 2000
````

Launching PySpark with cassandra support: 
````
docker-compose exec master pyspark --jars /src/spark-streaming-kafka-0-8-assembly.jar --packages anguenot:pyspark-cassandra:0.7.0 --conf spark.cassandra.connection.host=cassandra-seed-node
````

Cassandra seed node login: 
````
docker exec -it cassandra-seed-node /usr/bin/env bash
````

Cassandra create keyspace and table: 
````
docker exec -it cassandra-seed-node /usr/bin/env cqlsh -f /src/cassandra.cql
````