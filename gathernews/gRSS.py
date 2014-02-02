# gRSS.py
""" Module that lets you commit RSS feeds to a SQLite3 database

The module is designed to make it very easy for Python programmers to
load their selected RSS feeds into a SQLite3 database. This module arose
out of a need to create custom datasets that can be used for text analytics.

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).

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

DOCUMENTATION: For complete documentation, http://pythonhosted.org/GatherNews
"""

import feedparser
import sqlite3
from simpleflake import * 
import re
import json
import logging


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

    def read_file(self, path, your_file_name):
        """ Reads in file so that only rss links are included

        Unfortunately, .readlines() or .read() alone was sucking in extra
        '\n' symbols not related to the RSS links. This approach uses regular
        expressions to only list items that are consistent with an RSS feed
        link. 

        Args:
            path: the file path. Ex. "\home\tyler\Gathernews\gathernews\"
            your_file_name: name of file you want to read

        Returns:
            List of strings where each string is a link to an RSS feed

        Raises:
            UserWarning: "Could not recognize the file"
        """
        your_file = open(path + your_file_name, 'r').read()
        f = your_file.split("\n")
        pattern = re.compile("^[http]+")
        clean_file = []
        # Make sure only rss feeds are returned
        for link in f:
            if pattern.search(link):
                clean_file.append(link)
        if len(clean_file) == 0:
            raise UserWarning("Could not recognize the file")
        return clean_file


    def update_feeds_json(self, path, create_these_tables,
                          previous_feeds_list, current_feeds_list):
        """ A JSON object of table_names in the database is updated.

        Args:
            path: The filepath to the JSON object to be updated
            create_these_tables: A list of table names that will be entered
                                 into the database. 
            previous_feeds_list: A list of RSS feed links corresponding to
                                 table names that are in the database.
            current_feeds_list: A list of RSS feed links that may correspond
                                to table names that are not in the database.

        Returns:
            No items are returned. This method writes a JSON object to disk.
        """
        # update previous_feeds_list with info from current_feeds_list
        if len(create_these_tables) > 0:
            previous_feeds_list = create_these_tables
            # The list is written as a JSON object to your disk.

            # there will be a bug here if you don't resolve the file
            # path issue where feeds_lists.txt wants something different
            with open(path + 'previous_feeds_list.json',
                      mode = 'w') as f:
               return json.dump(previous_feeds_list, f)
        else:
            return False


    def does_json_exist(self, path, your_file_name):
        """ If a json object exists then return it

        Args:
            file_name: This is the name of your file.

        Returns:
            A json object from your specified path is returned.
        """
        try:
            with open(path + file_name, 'r') as f:
                return json.load(f)
        # At some point you should create a method that checks to see if the
        # file path given by the user is accurate. 
        except:
            return False


    def get_tablenames(self):
        """ All table names are extracted for use in SQL queries.

        Returns:
            revised_list: A list of all table names in the database is here.
        """
        # Init db locally 
        conn = sqlite3.connect(self.path + "FeedMe.db")
        c = conn.cursor()
        # List of tables to query
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # List of tables names that can be queried
        list_tables = c.fetchall()
        # Create a revised list for insert query
        revised_list = [str(list_tables[t_name]).strip('(')\
                        .strip(')').strip(',').strip('u').strip("'") 
                        for t_name in range(len(list_tables))]
        conn.close() # close sqlite3 db
        return revised_list

        
    def get_RSS_link(self):
        """RSS links used to pull feeds"""
        return self.read_file(self.path, "feeds_list.txt")

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
        table_name = re.sub(r'\W+', '', d.feed.title)

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
            if previous_feeds_list == False and len(RSS_link) > 1:
                self.make_table_names(RSS_link, create_these_tables)

            # If previous_feeds_list is not empty check RSS links against
            # previously used RSS links.
            elif RSS_link not in previous_feeds_list and len(RSS_link) > 1:
                self.make_table_names(RSS_link, create_these_tables)

            # When an RSS link is passed that is < 1 then read_file() is
            # working incorrectly and so a UserWarning is raised. 
            else:
                pass
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
        # If previous_feeds_list is empty then start a new list.
        if previous_feeds_list == False:
            previous_feeds_list = []
        
        # Load the RSS links from 'feeds_list.txt'.
        current_feeds_list = self.get_RSS_link()

        ## create_these_tables() goes about here
        create_these_tables = self.create_these_tables(current_feeds_list,
                                                       previous_feeds_list)
            
        ## update backup list for tables
        if create_these_tables >= 1:
            # Update running list of tables in the database
            self.update_feeds_json(self.previous_path, create_these_tables,
                                   previous_feeds_list, current_feeds_list)
            return create_these_tables
        else:
            return False # False, no new tables will be created

        
    def create_tables(self):
        """ Creates tables for RSS news feeds

        Sets up db tables where each RSS link feeds
        into a separate table because it's easier
        to aggregate then deaggregate.
        """
        if len(self.do_tables_exist()) > 0:
            # Open database locally
            conn = sqlite3.connect(self.path + "FeedMe.db")
            conn.isolation_level = None
            c = conn.cursor()
            transaction_query = "BEGIN; "
            for table_name in self.do_tables_exist():
                table = "CREATE TABLE " +  table_name + \
                        "( primary_key text, title text," + \
                        " description text, link text, published text); "
                transaction_query = transaction_query + table
                # Which tables are being entered?
                print "\t" + table_name
                
            transaction_query = transaction_query + " COMMIT;" 
            # Create table in sqlite3
            c.executescript(transaction_query)
            # close sqlite3 db
            conn.close()
        elif len(self.do_tables_exist()) == 0:
            print("No new tables need to be created\n")
        else:
            raise UserWarning("do_tables_exist() not returning a value")

#############################################################################
# Populate your existing tables with your selected RSS feeds.

    def regex_match(self, regex):
        """ Return the regular expression match if it exists

        Args:
            regex: Includes the regular expression pattern and the phrase
                   to be checked.

        Returns:
            False if no match is found; otherwise, the first group is
            returned because we expect no more than one group in this
            module. 
        """
        if regex is None:
            return False
        return regex.group(0)
            
    def strip_garbage(self, description):
        """ Remove HTML garbage from the description

        Args:
            description: An article's description from the RSS Feed
        
        Returns:
            A string that does not include HTML garbage

        Raises:
            Warning: Logged when HTML garbage is not successfully removed.
        """
        # Check to see if HTML code is included in the description
        html_brackets = re.compile("[<].*[>]")
        if self.regex_match(html_brackets.search(description)) != False:
            
            # Use known patterns to solve the description bug
            pattern1 = re.compile("^.*?(?=<div)")
            pattern2 = re.compile("^.*?(?=<img)")

            # Take the length of the description to see if we are
            # resolving the bug
            desc_length = len(description)

            # When the desc_length is reduced then we assume the bug
            # is resolved
            description = self.regex_match(pattern1.search(description))

            if description != False:
                return description

            elif description == False:
                description = self.regex_match(pattern2.search(description))
                if description != False:
                    return description

            else:
                if len(html_brackets.search(description).group(0)) > 0:
                    logging.warning("HTML garbage not successfully removed"\
                                    +"from the article description. Please"\
                                    +"file a bug report using "\
                                    +"'https://github.com/Bonza-Times/Gath"\
                                    +"erNews/issues'")
                else:
                    pass
                
        else:
            return description


    def match_names(self, query_name):
        """ Match SQL database table names to table names used for insert
        query """
        table_names = self.get_tablenames()
        if query_name in table_names:
            return True
        else:
            return False
#### Point of departure for next test #################!!!!!
    def transaction_query(self):
        """ Same thing as above but returns a string """
        # create a .sql script more or less
        # so we're going to create a string with each statement separated
        # by a semicolon. The string starts with BEGIN and ends with COMMIT
        # execute the script with BEGIN...COMMIT
        links = self.get_RSS_link()
        transaction_query = "BEGIN "
        for each_link in links:
            the_articles = feedparser.parse(each_link)
            # make sure link matches tablename
            for article in enumerate(the_articles.entries):
                number, entry = article
                ## Use simpleflake for the primary key
                primary_key = str(simpleflake())
                ## Remaining columns are from feedparser
                # title
                title = entry.entries[number].title_detail.value
                # summary/description
                description = self.strip_garbage(entry.entries[number].\
                                                 summary_detail.value)
                # link
                article_link = entry.entries[number].links[0].href
                # published
                published = entry[number].published

                ## Create transaction query for SQL database
                insert_query_table_name = re.sub(r'\W+', '', entry.feed.\
                                                 title)
                # Insert table_name must be in database already
                if self.match_names(insert_query_table_name) == True:
                    transaction_query = transaction_query + "INSERT INTO "\
                                        + insert_quer_table_name + \
                                        " VALUES(" + primary_key + "," +\
                                        title + "," + description + "," +\
                                        article_link + "," + published +\
                                        "; "
                else:
                    raise UserWarning("Something bad happened")
        # complete concatenation of transaction query after all articles
        # have been added for all links by ending statement with 'COMMIT;'
        transaction_query = transaction_query + " COMMIT;"
        return transaction_query


    def populate_db(self):
        ''' 
        Queries are matched with dict keys which then
        provides the values associated with each query by sharing
        the table names as a reference point. This allows rows to be 
        populated for each table leading to the population of the db.
        '''
        self.c.executescript(self.transaction_query())
        print("\n populate_db is complete")


#############################################################################
# Remove any duplicate entries in these tables.

    def rm_duplicates(self):
        '''
        Limitation of this duplicate removal approach is that only one
        duplicate entry will be removed (containing the lowest valued
        primary_key). If the number of  duplicate entries per item  > 2
        then that will introduce a bug. 
        '''
        # probably turn this into a transaction query
        # Remove duplicate queries
        for table_name in self.table().keys():
            query = "DELETE FROM " + table_name + " WHERE primary_key " \
                    "NOT IN " \
                    "(SELECT min(primary_key) FROM " + table_name + \
                    " GROUP BY title, published);"
            self.c.execute(query)
            self.conn.commit()
        conn.close()
        print " rm_duplicates is complete"

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
       
    
    
