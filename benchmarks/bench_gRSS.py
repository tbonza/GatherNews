# Run each method then break down each method and time each piece
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
        self.capture_feeds.create_tables()
        total = time.time() - start
        print "Elapsed time: ", total
        return total
