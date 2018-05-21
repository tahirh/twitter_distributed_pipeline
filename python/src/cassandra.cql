CREATE KEYSPACE ratings
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

USE ratings;

CREATE TABLE twitter (
ticker_id text,
rating_time timestamp,
rating float,
PRIMARY KEY (ticker_id, rating_time)
)
WITH CLUSTERING ORDER BY (rating_time DESC);

use ratings;
INSERT INTO twitter(ticker_id,rating_time,rating)
VALUES ('msft','2013-04-03 07:03:00',0.9);