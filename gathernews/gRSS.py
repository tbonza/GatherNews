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
import sqlite3
from simpleflake import * 
import re
import json
import logging

## custom modules

# clean input
from io import ReadFiles, WriteFiles
from rm_garbage import FilterGarbage
from bug_fixes import V1Bugs
# play well with DBs
from mongo_io import MongoIO
from sqlite3_io import Sqlite3IO
# handle requests quickly 
#from async import *
#from threads import *


class CaptureFeeds(object):
    """ Commits RSS news feeds to a SQLite3 database  """


    def __init__(self, path):
        self.path = path
        # Path corresponds to feeds_list.txt. 
        self.RSS_link_list = path + "feeds_list.txt"
        # Path corresponds to previous_feeds_list.json. 
        self.previous_path = path

############################################################################
# Check to see if you need new tables created.

    def fix_create_table_bug(self):
        """ Fix the create table bug V0.1.0

        This method is contained in this class to stay consistent with
        previous versions. All bug fixes after V0.2.1 are located in
        gathernews.bug_fixes
        """
        v1_bugs = V1Bugs(self.path)
        return v1_bugs.fix_create_table_bug()

        
    def read_file(self, path, your_file_name):
        """ Reads in file so that only rss links are included """
        read_files = ReadFiles(self.path)
        return read_files.read_file(path, your_file_name)
         

    def update_feeds_json(self, path, create_these_tables,
                          previous_feeds_list, current_feeds_list):
        """ A JSON object of table_names in the database is updated.

        This method is contained in this class to stay consistent with
        previous versions. All input/ouput after V0.2.1 is located in
        gathernews.io
        """
        write_files = WriteFiles(self.path)
        return write_files.update_feeds_json(path, create_these_tables,
                                             previous_feeds_list,
                                             current_feeds_list)

    def does_json_exist(self, path, your_file_name):
        """ If a json object exists then return it

        This method is contained in this class to stay consistent with
        previous versions. All input/ouput after V0.2.1 is located in
        gathernews.io
        """
        self.read_files = ReadFiles(self.path)
        return self.read_files.does_json_exist(path, your_file_name)

    def get_RSS_link(self):
        """ RSS links used to pull feeds

        This method is contained in this class to stay consistent with
        previous versions. All input/ouput after V0.2.1 is located in
        gathernews.io
        """
        read_files = ReadFiles(self.path)
        return read_files.get_RSS_link()
        
        
############################################################################
# Create the new tables if it is necessary.

    def make_table_names(self, RSS_link, create_these_tables):
        """ Make the table names for the sqlite3 database.

        Args:
            RSS_link: RSS_link from 'feeds_list.txt'
            create_these_tables: A list of table names to be created.

        Returns:
            The 'create_these_tables' list is returned with a table name
            appended to it.
        """
        # Parse the RSS link with the feedparser library.
        d = feedparser.parse(RSS_link)

        # Use regular expressions to create a table name for the sqlite3 db.
        try:
            table_name = re.sub(r'\W+', '', d.feed.title)
        except:
            table_name = "missing table name"

        # Append the new table name to the 'create_these_tables' list
        create_these_tables.append(table_name)
        return create_these_tables


    def create_these_tables(self, current_feeds_list, previous_feeds_list):
        """ Table names for new tables are generated.

        Args:
            current_feeds_list: List of RSS_links inputted by the user.
            previous_feeds_list: List of RSS_links generated by the program
                                 to keep track of tables currently in the
                                 database.
        
        Returns:
            A list of table names for tables that do not currently
            exist in the databases are created.
        
        Raises:
            UserWarning: RSS links have not been added to 'feeds_list.txt'
            UserWarning: Blank entry found, can't make table_name

        """
        # First, we need to know that the RSS links have been properly added.
        if len(current_feeds_list) == 0:
            raise UserWarning("RSS links have not been added to"\
                              + " 'feeds_list.txt'")

        # Second, we can now generate a list of table names. 
        create_these_tables = []
        for RSS_link in current_feeds_list:
            # If there is nothing in previous_feeds_list then append names.
            if previous_feeds_list == False:
                self.make_table_names(RSS_link, create_these_tables)

            # If previous_feeds_list is not empty check RSS links against
            # previously used RSS links.
            elif RSS_link not in previous_feeds_list:
                self.make_table_names(RSS_link, create_these_tables)
            # When no new tables need to be added return False
            else:
                pass

        # create no tables if they aren't needed
        if len(create_these_tables) == 0:
            return False
        else:
            return create_these_tables


    def do_tables_exist(self): 
        """ Checks to see if new tables should be created

        The real job of this is to probably set & reset
        previous_feeds_list.json which we haven't done yet. 

        Returns:
            A list of table names for tables that have not been created.
        """
        # Load the json object from the file if it exists. 
        previous_feeds_list = self.does_json_exist(self.path,
                                              "previous_feeds_list.json")
        
        # Load the RSS links from 'feeds_list.txt'.
        current_feeds_list = self.get_RSS_link()

        ## create_these_tables() goes about here
        create_these_tables = self.create_these_tables(current_feeds_list,
                                                       previous_feeds_list)
            
        ## update backup list for tables
        if create_these_tables != False:
            # Update running list of tables in the database
            self.update_feeds_json(self.previous_path, create_these_tables,
                                   previous_feeds_list, current_feeds_list)
            return create_these_tables
        else:
            return False # False, no new tables will be created

        


#############################################################################
# Populate your existing tables with your selected RSS feeds.

   


    def match_names(self, query_name):
        """ Match SQL database table names to table names used for insert
        query """
        table_names = self.get_tablenames()
        if query_name in table_names:
            return True
        else:
            return False


    def rss_feeds_data(self):
        """ Dictionary of table names mapped to a list of tuples for articles

        This data structure is the 'last stop' before the article information
        is loaded into the SQL database. As such, it can also be called by
        itself; if loading a database is not what we want to do.
        
        Returns:
            Each key is a table name in the SQL database. The table name is
            mapped to a list of tuples. Each tuple in the list contains one
            string for every field in the database schema. The tuple is:
            (article title, article description, article link, date/time
            article published)
        """

        ## Data structure is a article graph
        insert_this_data = {}

        links = self.get_RSS_link()
        # Begin transaction query
        for each_link in links:
            data_hold = [] # place to put article info
            the_articles = feedparser.parse(each_link)
            for article in the_articles.entries:
                ## Use simpleflake for the primary key
                primary_key = str(simpleflake())
                ## Remaining columns are from feedparser
                # title
                try:
                    title = article.title_detail.value
                except:
                    title = ""
                    logging.warning("title not found")
                # summary/description
                try:
                    description = self.for_fucks_sake(article.\
                                                      summary_detail.value)
                except:
                    description = ""
                    logging.warning("description not found")
                    # link
                try:
                    article_link = article.links[0].href
                except:
                    article_link = ""
                    logging.warning("article link not found")
                # published
                try:
                    published = article.published
                except:
                    published = ""
                    logging.warning("date/time published not found")
                data_hold.append((primary_key, title, description,
                                  article_link, published))

            ## Create transaction query for SQL database
            try:
                insert_query_table_name = re.sub(r'\W+', '',\
                                                 the_articles.feed.title)
            except:
                insert_query_table_name = "table_name_not_found"
                
            if self.match_names(insert_query_table_name) == True:
                insert_query = "INSERT INTO " + insert_query_table_name + \
                               " VALUES (?,?,?,?,?)"

                # unicode to ascii so life can go on.......
                insert_query = insert_query.encode('ascii')
                
                # Populate data structure
                insert_this_data[insert_query] = data_hold 
                    
            else:
                raise UserWarning("Something bad happened")
            
        return insert_this_data
                

#############################################################################
# Remove any duplicate entries in these tables.

    
############################################################################
# Put everything together in load_db().

    def load_db(self):
        """ Loads the sqlite3 database """
        ## Check to see if you need new tables created.
        #self.do_tables_exist()
        
        ## Create those new tables if it is necessary.
        self.create_tables()
        
        ## Populate your existing tables with your selected RSS feeds.
        self.populate_db()
        
        ## Remove any duplicate entries in these tables. 
        self.rm_duplicates()
       
    
    
