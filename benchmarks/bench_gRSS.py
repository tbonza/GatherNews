""" Benchmarks for methods in gRSS.py

The following methods gather news from specified RSS feeds:
    create_tables(): creates new tables in sqlite3 db
    populate_db(): puts news stories from RSS feeds into sqlite3 db
    rm_duplicates(): removes duplicate entries in the sqlite3 db

Each of these methods is timed. Methods supporting each of these three
methods are also timed to see where we have room for improvement.
"""

from gathernews.gRSS import CaptureFeeds
import time

class BenchmarkgRSS:
    def __init__(self):
        # File path to where "feeds_list.txt" is located
        file_path = "/home/tyler/code/GatherNews/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(file_path)
        
    def benchmark_create_tables(self):
        """ Test create_tables() method as well as supporting methods
        
            get_RSS_link()
            get_tablenames()
            # do_tables_exist() -- this is not working

        """
        start = time.time()
        self.capture_feeds.load_db()
        total = time.time() - start
        print "Elapsed time: ", total
        return total

# Let's make things interesting an run the version 0.2.0 against 0.1.0
# Benchmarks were run on my laptop. 

## version 0.1.0 ##
path = "/home/tyler/code/GatherNews/benchmarks/"

def do_everything(path):
    start = time.time() 
    capture_feeds = CaptureFeeds(path)
    capture_feeds.create_tables()
    capture_feeds.populate_db()
    capture_feeds.rm_duplicates()
    total = time.time() - start
    print "Elapsed time: ", total
    return total # database must be removed each time

# 105.97, 104.81, 103.53, 106.22, 105.70
# Mean: 105.246
# Standard deviation: 1.09701

def populate_and_rm_dups(path):
    start = time.time()
    capture_feeds = CaptureFeeds(path)
    capture_feeds.populate_db()
    capture_feeds.rm_duplicates()
    total = time.time() - start
    print "Elapsed time: ", total
    return total

def do_it_five(path):
    count = 0
    while count < 5:
        populate_and_rm_dups(path)
        count += 1

# 95.11, 97.16, 95.83, 96.73, 95.89
# Mean: 96.144
# Standard deviation: 0.8074528


## version 0.2.0

def do_everything2(path):
    """ load_db() in 0.2.0 achieves the same thing as the benchmark function
    populate_and_rm_dups() seen above """
    start = time.time() 
    capture_feeds = CaptureFeeds(path)
    capture_feeds.load_db()
    total = time.time() - start
    print "Elapsed time: ", total
    return total

# 84.68, 54.40, 25.47, 27.17, 34.08
# Mean: 45.16
# Standard deviation: 24.90638
    
def do_it_five(path):
    count = 0
    while count < 5:
        do_everything2(path)
        count += 1
    
# 16.39, 14.34, 20.58, 15.23, 15.96
# Mean: 16.5
# Standard deviation: 2.409803
