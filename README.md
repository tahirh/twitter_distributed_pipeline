Data Challenge

Code repo for building streaming pipeline using twitter, kafka, spark and cassandra. 

This application has been tested on Python 3.6.3, Docker 17.12.0-ce and docker-compose 1.18.0 on Windows 10 machine. 

Browse in the python folder and follow the instructions to run the application: 

1) Install all python packages listed in requirements.txt.
````
pip install -r requirements.txt
````
2) In docker-compose KAFKA_ADVERTISED_HOST_NAME should contain ip of your machine. 
3) In the properties file, provide your twitter credentials.
4) docker compose up will lauch all the containers. 
5) In another window, start producer.py. This starts loading twitter stream data to kafka. 
6) Open a new windw and run the following command to create keyspace and table in cassandra 
````
docker exec -it cassandra-seed-node /usr/bin/env cqlsh -f /src/cassandra.cql
````
7) Next, execute the command below to run the spark job and load results into the cassandra db. 
````
docker-compose exec master spark-submit --jars /src/spark-streaming-kafka-0-8-assembly.jar --packages anguenot:pyspark-cassandra:0.7.0 --conf spark.cassandra.connection.host=cassandra-seed-node /src/consumer.py kafka:9092 twitter-data 2000
````
