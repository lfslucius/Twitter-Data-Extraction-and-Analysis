# Project Introduction
This project aims to score phrases and words based on their “trendiness” on Twitter by processing in three different ways: **data lake**, **data warehouse,** and **streaming message queue**. Suppose we choose a phrase and a specific point t in time. In that case, the trendiness score is the ratio which is the probability of seeing a phrase in the current minute at t relative to the probability of seeing the same phrase in the minute prior to *t.*

Our team for this project consists of seven members. I took responsible for **scraping and extracting data from twitter API, analyzing trendiness score with Python and SQL in data warehouse and stream, project management.** We separated this project into three milestones and determined the goal for each one.


# How to read the code

Please follow this README.md to read code in order.

## Milestone 1

In this milestone, the task is to read tweets from the Twitter API and write them to a file on a disk, our **data lake** for analysis. Then, we mainly utilized the **argparse** Python library to read from the file containing the JSON-formatted tweets and analyze the tweets by a simple calculation.

The detailed running code instruction is as follows:

  * In [**server.py**](./Milestone_1/server.py): Type "python server.py". Then we can type `ls` to see all files in the project and get the **tweets.txt**.
  
  ```
  python server.py
  ```

  * In [**word_count.py**](./Milestone_1/word_count.py): Type "python word_count.py -w word" // Type "python word_count.py -w "phrase phrase"'

    ('-w word' to count a word and '-w "phrase phrase"' to count a phrase)".
  ```
  python word_count.py -w word
  ```
  or
  ```
  python word_count.py -w "phrase phrase"
  ```

  * In [**vocabulary_size.py**](./Milestone_1/vocabulary_size.py): Type "python vocabulary_size.py".

  ```
  python vocabulary_size.py
  ```
  
## Milestone 2

In milestone 2, we used a designed **Postgre SQL database*** instead of a data lake to store data. Also, we applied the **psycopg** library into Python codes for invoking SQL queries to calculate trendiness scores and combined it with the **argparse library** for importing the words or phrases as the command.

  * To use [**schema_postgres.sql**](./Milestone_2/schema_postgres.sql):\
    Type `git clone git@github.com:DAL2611/GB-760-Project.git` to clone our project.  
    Type `psql` to get into the postgresSQL environment.  
    Type `create database tweets` to create a new database.  
    Type `\q` to exit from PostgreSQL.  
    Type `psql tweets < schema_postgres.sql` to create a new table named tweets  
    
  * To use [**server_postgres.py**](./Milestone_2/server_postgres.py): Type "python server_postgres.py"
  
  ```
  python server_postgres.py
  ```

<img width="786" alt="截屏2022-01-03 上午12 03 23" src="https://user-images.githubusercontent.com/97009411/147903154-1fe35d37-6907-4740-b4e3-634742b332e4.png">

  * In [**word_count_postgres.py**](./Milestone_2/word_count_postgres.py): Type "python word_count_postgres.py -w -word ("-word" is for a word and "--phrase phrase" is for a phrase)".

  ```
  python word_count_postgres -w word
  ```
  or
  ```
  python word_count_postgres -w "phrase phrase"
  ```

  * In [**vocabulary_size_postgres.py**](./Milestone_2/vocabulary_size_postgres.py): Type "python vocabulary_size_postgres.py -w -word ("-word" is for a word and "--phrase phrase" is for a phrase)".

  ```
  python vocabulary_size_postgres -w -word "your phrase"
  ```
  
  * In [**trendiness_postgres.py**](./Milestone_2/trendiness_postgres.py): Type "python trendiness_postgres.py -w -word ("-word" is for a word and "--phrase phrase" is for a phrase)".

  ```
  python trendiness_postgres -w -word "your phrase"
  ```

## Milestone 3

The goal in milestone 3 is to read tweets from Twitter API and realize real-time analysis continuously. We upgrade our codes to use **Kafka** as a streaming message queue.

  * sudo `systemctl start kafka` -> `sudo systemctl status kafka` (for checking)
  * Create Topics in your terminal: `~/kafka/bin/kafka-topics.sh --create --topic gb760 --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1`
  * Run [**server_to_kafka.py**](./Milestone_3/server_to_kafka.py)
  * Run [**server_from_kafka.py**](./Milestone_3/server_from_kafka.py)
  * Run [**trendiness_kafka.py**](./Milestone_3/trendiness_kafka.py): As long as this code runs, at each new minute, it should print the most up-to-date trendiness score
  
  ```
  python trendiness_postgres -w -word "your phrase"
  ```
<img width="995" alt="截屏2022-01-03 上午12 05 45" src="https://user-images.githubusercontent.com/97009411/147903257-ba1d7383-6379-4bfe-8dd8-3fd13ba66748.png">

