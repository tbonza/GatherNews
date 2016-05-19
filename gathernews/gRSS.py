# gRSS.py
""" Module that lets you commit RSS feeds to a SQLite3 database

The module is designed to make it very easy for Python programmers to
load their selected RSS feeds into a SQLite3 database. This module arose
out of a need to create custom datasets that can be used for text 
analytics.

LICENSE: MIT license (http://opensource.org/licenses/MIT)

PLATFORMS: This should run on any platform where the dependencies are
available.

OVERVIEW: There is one method in this library that should load your 
sqlite3 database; load_db(). This method checks to see if you need new 
tables created, creates those tables if necessary, populates your 
existing tables, and then removes any duplicate entries in those tables.

-------------------------------------------------------------------------
from gathernews.gRSS import CaptureFeeds

path = "/home/tyler/code/"
capture_feeds = CaptureFeeds(path)

capture_feeds.load_db()
-------------------------------------------------------------------------

The sqlite3 database is loaded using the following schema:
    CREATE TABLE ReutersWorldNews( primary_key text, title text,
    description text,link text, published text);

Each table is assigned a unique table name that's taken from the name of 
the designated RSS feed. 

DOCUMENTATION: http://gathernews.readthedocs.org/en/latest/
"""


import logging



class CaptureFeeds(object):
    """ Commits RSS news feeds to a SQLite3 database  """


    def __init__(self, path):
        self.path = path
        # Path corresponds to feeds_list.txt. 
        # Path corresponds to previous_feeds_list.json. 
        #self.previous_path = path
        # Sqlite3 IO
        #self.sqlite3_io = Sqlite3IO(self.path)
        # 

    def load_db(self):
        """ Loads the sqlite3 database """

        # This will serve as a main() method to load either sqlite3
        # or Mongo. As such, it's really just an abstraction layer
        # over the code located in sqlite3_io or mongo_io

        
        ## Check to see if you need new tables created.
        #self.do_tables_exist()
        
        ## Create those new tables if it is necessary.
        #self.sqlite3_io.create_tables()
        
        ## Populate your existing tables with your selected RSS feeds.
        #self.populate_db()
        
        ## Remove any duplicate entries in these tables. 
        #self.rm_duplicates()
       
    
    
