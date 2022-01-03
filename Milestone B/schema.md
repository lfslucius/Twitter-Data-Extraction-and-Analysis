# Schema Structure

**tweets** (time_stamp, time_group, word, word_count)

# Explanation

We built a single-entity schema to show the internal structure of 'tweets' database. There is a table 'tweets' stored in database to present the basic information of tweets, including timestamp, belonged time group, content of word or phrase and its count. After extracting the above information from streaming tweets, we can calculate and load it into database for further analysis.
