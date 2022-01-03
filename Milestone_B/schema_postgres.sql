DROP TABLE tweets;

CREATE TABLE tweets (
   time_stamp		TIMESTAMP		NOT NULL,  
   time_group		TIMESTAMP		NOT NULL,   
   word				varchar(1000)	NOT NULL,
   word_count		INT				NOT NULL);
