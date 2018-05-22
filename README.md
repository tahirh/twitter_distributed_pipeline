Data Challenge

Code repo for building streaming pipeline using twitter, kafka, spark and cassandra. 

Instructions to run the application: 

1) In docker-compose KAFKA_ADVERTISED_HOST_NAME with the ip of your machine. 
2) In the properties file, provide your twitter credentials.
3) docker compose up will lauch all the containers. 
4) In another window, start producer.py. This starts loading twitter stream data to kafka. 
5) Open a new windw and run the following command to create keyspace and table in cassandra 
````
docker exec -it cassandra-seed-node /usr/bin/env cqlsh -f /src/cassandra.cql
````
6) Next, execute the command below to run the spark job and load results into the cassandra db. 

````
docker-compose exec master spark-submit --jars /src/spark-streaming-kafka-0-8-assembly.jar --packages anguenot:pyspark-cassandra:0.7.0 --conf spark.cassandra.connection.host=cassandra -seed-node /src/consumer.py kafka:9092 twitter-data 2000
````
