# Project Introduction
This project aims to score phrases and words based on their “trendiness” on Twitter by processing in three different ways: **data lake**, **data warehouse,** and **streaming message queue**. Suppose we choose a phrase and a specific point t in time. In that case, the trendiness score is the ratio which is the probability of seeing a phrase in the current minute at t relative to the probability of seeing the same phrase in the minute prior to *t.*


# How to read the code

We uploaded each file in each part of each milestone in this Final_version folder. Every file can be indexed by its commitment information. Please follow this README.md to read code in order.

## Milestone 1

The files of milestone 1 (M1) are about simply reading tweets from the Twitter API or a file and writting them to a file on disk, which is considered as our “data lake” in this project.

The detailed running code instruction is as follows:

  * In [**server.py**](server.py): Type "python server.py". Then we can type `ls` to see all files in the project and get the **tweets.txt**.
  
  ```
  python server.py
  ```

  * In [**word_count.py**](word_count.py): Type "python word_count.py -w word" // Type "python word_count.py -w "phrase phrase"'

    ('-w word' to count a word and '-w "phrase phrase"' to count a phrase)".
  ```
  python word_count.py -w word
  ```
  or
  ```
  python word_count.py -w "phrase phrase"
  ```

  * In [**vocabulary_size.py**](vocabulary_size.py): Type "python vocabulary_size.py".

  ```
  python vocabulary_size.py
  ```
  
## Milestone 2

Then, milestone 2 (M2) mainly consists of transitioning our code to use a PostgreSQL database instead of a data lake, continuing to read tweets from the Twitter API and writting them to our database using Python.

  * To use [**schema_postgres.sql**](schema_postgres.sql):\
    Type `git clone git@github.com:DAL2611/GB-760-Project.git` to clone our project.  
    Type `psql` to get into the postgresSQL environment.  
    Type `create database tweets` to create a new database.  
    Type `\q` to exit from PostgreSQL.  
    Type `psql tweets < schema_postgres.sql` to create a new table named tweets  
    
  * To use [**server_postgres.py**](server_postgres.py): Type "python server_postgres.py"
  
  ```
  python server_postgres.py
  ```

  * In [**word_count_postgres.py**](word_count_postgres.py): Type "python word_count_postgres.py -w -word ("-word" is for a word and "--phrase phrase" is for a phrase)".

  ```
  python word_count_postgres -w word
  ```
  or
  ```
  python word_count_postgres -w "phrase phrase"
  ```

  * In [**vocabulary_size_postgres.py**](vocabulary_size_postgres.py): Type "python vocabulary_size_postgres.py -w -word ("-word" is for a word and "--phrase phrase" is for a phrase)".

  ```
  python vocabulary_size_postgres -w -word "your phrase"
  ```
  
  * In [**trendiness_postgres.py**](trendiness_postgres.py): Type "python trendiness_postgres.py -w -word ("-word" is for a word and "--phrase phrase" is for a phrase)".

  ```
  python trendiness_postgres -w -word "your phrase"
  ```

## Milestone 3

Finally, the files of milestone 3 (M3) are about upgrading our code to use Kafka as a streaming message queue.

  * sudo `systemctl start kafka` -> `sudo systemctl status kafka` (for checking)
  * Create Topics in your terminal: `~/kafka/bin/kafka-topics.sh --create --topic gb760 --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1`
  * Run [**server_to_kafka.py**](server_to_kafka.py)
  * Run [**server_from_kafka.py**](server_from_kafka.py)
  * Run [**trendiness_kafka.py**](trendiness_kafka.py): As long as this code runs, at each new minute, it should print the most up-to-date trendiness score
  
  ```
  python trendiness_postgres -w -word "your phrase"
  ```
