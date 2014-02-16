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


            # line 225 is crashing the ca
            # issue needs to be resolved here == current_feeds_list
            previous_feeds_list = current_feeds_list
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
            with open(path + your_file_name, 'r') as f:
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

    def fix_create_table_bug(self):
        """ Fix the create table bug

        In GatherNews 0.1.0, a bug was introduced that does not allow you
        to add new RSS feeds to the 'feeds_list.txt' after your initial
        call of the create_tables() method.

        This method was created because we have no way of knowing which
        RSS feed links match which RSS table names without making a call
        to each RSS feed and recreating each table name.

        If you have previously used GatherNews 0.1.0 you should call this
        method once before calling any other methods on your previously
        created 'FeedMe.db'. Once this method is called then the issue should
        be resolved.

        Returns:
            Writes a JSON object to your disk called 'previous_feeds_list'
            that will fix the create_table() bug.

        Raises:
            UserWarning: This bug fix is not needed
        """
        
        # get table names from the database
        db_names = self.get_tablenames()

        # get table names from RSS feeds
        create_these_tables = {}
        for RSS_link in self.read_file(self.path, "feeds_list.txt"):
            d = feedparser.parse(RSS_link)
            table_name = re.sub(r'\W+', '', d.feed.title)
            create_these_tables[table_name] = RSS_link

        # see if the links associated with the table names are already here
        path = self.path
        file_name = 'previous_feeds_list.json'
        with open(path + file_name, 'r') as f:
            current_backup = json.load(f)

        count = 0
        backup_count = len(current_backup) 
        for name in create_these_tables.keys():
            if create_these_tables[name] in current_backup:
                count += 1
                
        if count == backup_count:
            # Warn the user that this bug fix is not needed
            raise UserWarning("This bug fix is not needed")

        else:
                
            # see which names match
            correct_RSS_links = []
            for table in db_names:
                if table in create_these_tables:
                    correct_RSS_links.append(create_these_tables[table])
                elif table not in db_names:
                    print table, " was not found in feeds_list.txt'"

            # Write the JSON object to disk
            with open(path + 'previous_feeds_list.json',
                      mode = 'w') as f:
                return json.dump(correct_RSS_links, f)

                    
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

        
    def create_tables(self):
        """ Creates tables for RSS news feeds

        Creates db tables where each RSS link feeds
        into a separate table because it's easier
        to aggregate then deaggregate.
        """
        tables = self.do_tables_exist()
        if tables:
            # Open database locally
            conn = sqlite3.connect(self.path + "FeedMe.db")
            conn.isolation_level = None
            c = conn.cursor()
            transaction_query = "BEGIN; "
            for table_name in tables:
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
            return True
        elif tables is False:
            print("\n\tNo new tables need to be created")
            return False
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

            # If known patterns are not able to resolve the description
            # bug then a warning will be logged to the user's console
            if self.regex_match(pattern1.search(description)) != False:
                return self.regex_match(pattern1.search(description))

            elif self.regex_match(pattern2.search(description)) != False:
                return self.regex_match(pattern2.search(description))
                
            else:
                logging.warning("HTML garbage not successfully removed\n"\
                                +" from the article description. Please\n"\
                                +" file a bug report using \n"\
                                +" 'https://github.com/Bonza-Times/Gath"\
                                +"erNews/issues'\n with this message: ")
                print description 
                
        else:
            return description


    def for_fucks_sake(self, description):
        """ This is apparently a bug fix for the description issue """
        fucking_hell = self.strip_garbage(description)
        return self.strip_garbage(fucking_hell)


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
                title = article.title_detail.value
                # summary/description
                try:
                    description = self.for_fucks_sake(article.\
                                                      summary_detail.value)
                except:
                    description = ""
                # link
                article_link = article.links[0].href
                # published
                try:
                    published = article.published
                except:
                    published = ""

                data_hold.append((primary_key, title, description,
                                  article_link, published))

            ## Create transaction query for SQL database
            insert_query_table_name = re.sub(r'\W+', '',\
                                             the_articles.feed.title)
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
                

    def populate_db(self):
        ''' 
        Queries are matched with dict keys which then
        provides the values associated with each query by sharing
        the table names as a reference point. This allows rows to be 
        populated for each table leading to the population of the db.
        '''
        # Set up connection
        conn = sqlite3.connect(self.path + "FeedMe.db")
        c = conn.cursor()
        # Execute SQL script
        data = self.rss_feeds_data()
        for table in data.keys():
            c.executemany(table, data[table])
        conn.commit()
        # close sqlite3 db
        conn.close() 
        print("\tpopulate_db is complete")


#############################################################################
# Remove any duplicate entries in these tables.

    def rm_duplicates(self):
        '''
        Limitation of this duplicate removal approach is that only one
        duplicate entry will be removed (containing the lowest valued
        primary_key). If the number of  duplicate entries per item  > 2
        then that will introduce a bug. 
        '''
        # Set up connection
        conn = sqlite3.connect(self.path + "FeedMe.db")
        c = conn.cursor()
        # Remove duplicate queries
        dup_script = "BEGIN TRANSACTION; "
        for table_name in self.get_tablenames():
            query = "DELETE FROM " + table_name + " WHERE primary_key " \
                    "NOT IN " \
                    "(SELECT min(primary_key) FROM " + table_name + \
                    " GROUP BY title, published); "
            dup_script = dup_script + query
        dup_script = dup_script + "COMMIT TRANSACTION;"
        c.executescript(dup_script)
        conn.close()
        print("\trm_duplicates is complete")

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
       
    
    
