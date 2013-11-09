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
        file_path = "/home/tyler/code/GatherNews/examples/"
        self.capture_feeds = CaptureFeeds(file_path)
        
    def benchmark_create_tables(self):
        """ Test create_tables() method as well as supporting methods
        
            get_RSS_link()
            get_tablenames()
            # do_tables_exist() -- this is not working

        """
        timing_list = []
        try:
            # create_tables()
            start = time.time()
            self.capture_feeds.create_tables()
            timing_list.append(("create_tables()", time.time() - start))
        except:
            raise TypeError
        try:
            # get_RSS_link()
            start = time.time()
            self.capture_feeds.get_RSS_link()
            timing_list.append(("get_RSS_link()", time.time() - start))
        except:
            raise TypeError
        try:
            # get_tablenames()
            start = time.time()
            self.capture_feeds.get_tablenames()
            timing_list.append(("get_tablenames()", time.time() - start))
        except:
            raise TypeError
        return timing_list

    def benchmark_populate_db(self):
        """ Test populate_db() method as well as supporting methods

            insert_query()
            strip_garbage()
            articles()
            table()

        """
        timing_list = []
        try:
            start = time.time()
            self.capture_feeds.populate_db()
            timing_list.append(("populate_db()", time.time() - start))
        except:
            raise TypeError
        try:
            start = time.time()
            self.capture_feeds.insert_query()
            timing_list.append(("insert_query()", time.time() - start))
        except:
            raise TypeError
        try:
            start = time.time()
            self.capture_feeds.strip_garbage()
            timing_list.append(("strip_garbage()", time.time() - start))
        except:
            raise TypeError
        try:
            start = time.time()
            self.capture_feeds.articles()
            timing_list.append(("articles()", time.time() - start))
        except:
            raise TypeError
        try:
            start = time.time()
            self.capture_feeds.table()
            timing_list.append(("table()", time.time() - start))
        except:
            raise TypeError
        return timing_list

    def benchmark_rm_duplicates(self):
        """ benchmark rm_duplictes(), no supporting methods """
        timing_lis
        try:
            start = time.time()
            self.capture_feeds.rm_duplicates()
            timing_list.append(("rm_duplicates()",time.time() - start))
        except:
            raise TypeError
        return timing_list
            


for tableA in self.benchmark_create_tables():
    print tableA

for tableB in self.benchmark_populate_db():
    print tableB

for tableC in self.benchmark_rm_duplicates():
    print tableC
