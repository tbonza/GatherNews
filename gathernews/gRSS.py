# gRSS.py
""" Module that lets you commit RSS feeds to a SQLite3 database

The module is designed to make it very easy for Python programmers to
load their selected RSS feeds into a SQLite3 database. This module arose
out of a need to create custom datasets that can be used for text analytics.

LICENSE: MIT license (http://opensource.org/licenses/MIT)

PLATFORMS: This should run on any platform where the dependencies are
available.

OVERVIEW: There is one method in this library that should load your sqlite3
database; load_db(). This method checks to see if you need new tables
created, creates those tables if necessary, populates your existing tables,
and then removes any duplicate entries in those tables.

----------------------------------------------------------------------------
from gathernews.gRSS import CaptureFeeds

path = "/home/tyler/code/"
capture_feeds = CaptureFeeds(path)

capture_feeds.load_db()
----------------------------------------------------------------------------

The sqlite3 database is loaded using the following schema:
    CREATE TABLE ReutersWorldNews( primary_key text, title text,
    description text,link text, published text);

Each table is assigned a unique table name that's taken from the name of the
designated RSS feed. 

DOCUMENTATION: http://gathernews.readthedocs.org/en/latest/
"""

import feedparser
#import sqlite3
#from simpleflake import * 
import re
#import json
import logging

## custom modules

# clean input
#from io import ReadFiles, WriteFiles
#from rm_garbage import FilterGarbage
#from gathernews.bug_fixes import V1Bugs
# play well with DBs
#from mongo_io import MongoIO
#from sqlite3_io import Sqlite3IO
# handle requests quickly 
#from async import *
#from threads import *


# All captureFeeds should really do is load the data from the RSS feeds
# into a dictionary of feed_ids, present in a relations table or similar
# mongo data model, mapped to a list of tuples containing field information
# missing values will be 'None' values



class CaptureFeeds(object):
    """ Commits RSS news feeds to a SQLite3 database  """


    def __init__(self, path):
        self.path = path
        # Path corresponds to feeds_list.txt. 
        self.RSS_link_list = path + "feeds_list.txt"
        # Path corresponds to previous_feeds_list.json. 
        #self.previous_path = path
        # Sqlite3 IO
        #self.sqlite3_io = Sqlite3IO(self.path)
        # 

        
    def primary_key(self):
        """ Returns primary key to map onto values """
        pass # feed_id


    def unique_id(self):
        """ Returns unique identifier for each story in the db """
        ## Use simpleflake for the unique id
        primary_key = str(simpleflake())

        
    def title(self, size):
        """ Syncs up with xml_settings to return title """
         # title
         try:
             title = article.title_detail.value
         except:
             title = ""
             logging.warning("title not found")

        
    def description(self, size):
        """ Syncs up with xml_settings to return description """
        # summary/description
        try:
            description = self.for_fucks_sake(article.\
                                              summary_detail.value)
        except:
            description = ""
            logging.warning("description not found")


    def article_link(self, size):
        """ Syncs up with xml_settings to return article_link """
        # link
        try:
            article_link = article.links[0].href
        except:
            article_link = ""
            logging.warning("article link not found")


    def date_published(self, size):
        """ Syncs up with xml_settings to return date published """
        # published
        try:
            published = article.published
        except:
            published = ""
            logging.warning("date/time published not found")

        
    def num_rss_items_returned(self):
        """ Returns number of items, stories, in a RSS feed """
        pass

    def make_tuple(self, size):
        """ Return a tuple to be appended to a list of News tuples """
        return (self.unique_id(),
                self.title(size),
                self.description(size),
                self.article_link(size),
                self.date_published(size))

        
    def add_tuples(self, key):
        """ Returns a list of tuples as a value for the primary key """
        size = 0
        list_of_tuples = []
        while size < self.num_rss_items_returned():
            list_of_tuples.append(self.make_tuple(size))
            size += 1
            
        return list_of_tuples

         
    def late_tuples(self, key):
        """ Return a tuple to the dictionary if it arrives late """
        pass
        

    def rss_feeds_data(self):
        """ Returns data structure used for loading db in GatherNews """
        load_this_data = {}
        count = 0
        while count < number_of_rss_feeds:
            load_this_data[key] = self.add_tuples(key)
            count += 1

        return load_this_data
                

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
       
    
    
