import feedparser
import sqlite3
from simpleflake import * 
import re

class CaptureFeeds:
    """ Commits RSS news feeds to a SQLite3 database
    
    Additional documentation
    """
    def __init__(self, path):
        self.RSS_link_list = path + "feeds_list.txt"
        # Initialize sqlite3
        conn = sqlite3.connect(path + "FeedMe.db")
        self.c = conn.cursor()
        
    def get_RSS_link(self):
        '''RSS links used to pull feeds'''
        f = open(self.RSS_link_list, 'r').readlines()
        return f[0:len(f)-1] #Removes last \n to match len(cleaned_list)

    def get_tablenames(self):
        ''' Table names are cleaned for SQL queries'''
        # List of tables to query
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # List of tables names that can be queried
        list_tables = self.c.fetchall()
        # Create a revised list for insert query
        revised_list = \
                       [str(list_tables[t_name]).strip('(')\
                        .strip(')').strip(',').strip('u').strip("'") 
                        for t_name in range(len(list_tables))]
        return revised_list

    def do_tables_exist(self): # Error here
        """ Checks to see if new tables should be created


        # This was failing silently so it's unplugged and here
        # to reference

        """
        RSS_links = self.get_RSS_link()
        Table_Names = self.get_tablenames() # This looks like it's failing
        if len(RSS_links) == len(Table_Names):
            return True
        elif len(RSS_links) > len(Table_Names):
            new_table = len(Table_Names) - len(RSS_links)
            new_table_list = [new_table_list.append(table) for table \
                              in xrange(new_table)]
            return new_table_list
        else:
            raise TypeError("Table overload")
               
    def create_tables(self):
        """ Creates tables for RSS news feeds

        Sets up db tables where each RSS link feeds
        into a separate table because it's easier
        to aggregate then deaggregate.
        """
        for RSS_link in self.get_RSS_link():
            if len(RSS_link) != 1:
                # Make table name match RSS feed name
                d = feedparser.parse(RSS_link)
                table_name = re.sub(r'\W+', '', d.feed.title)
                # Creating string separately makes multiple table 
                # creation easier
                table = "CREATE TABLE " +  table_name + \
                        "( primary_key text, title text," + \
                        " description text, link text, published text)" 
                # Create table in sqlite3
                self.c.execute(table)
                # Which tables are being entered?
                print "\t" + table_name 
            elif len(RSS_link) == 1:
                # Save (commit) the changes
                self.conn.commit()
                # Close the connection to sqlite3

                # This part is failing
               # print "\n", len(self.do_tables_exist()), " new tables" \
                #    + " have been created"

    def strip_garbage(self, description):
        '''
        Article descriptions were returning some garbage
        '''
        sep = '<div'
        rest = description.split(sep, 1)[0]
        sep = '<img'
        rest = rest.split(sep, 1)[0]

        except(UnicodeEncodeError):
                description = description_junk
        return rest

    def articles(self, number):
        '''
        This should give me a list of tuples containing
        information on the articles for a given RSS feed
        '''
        links = self.get_RSS_link()
        d = feedparser.parse(links[number])
        new_list = []
        for article in range(len(d)):
            # Hack simpleflake for sqlite3
            primary_key = str(simpleflake()) 
            # Remaining columns are iterated from feed parse
            title = d.entries[article].title
            try:
                description_junk = str(d.entries[article].description)
                description = self.strip_garbage(description_junk)
            except(UnicodeEncodeError):
                description = description_junk
            link = d.entries[article].link
            published = d.entries[article].published
            new_list.append((primary_key,title,description,link,published))
        return new_list

    def match_names(self, query_name, db_name):
        """ Match SQL database table names to table names used for insert
        query """
        if :
            return True
        else:
            return False

    def articles(self):
        """ Same thing as above but returns a string """
        table_names = self.get_tablenames()
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
                article_link = entry.entries[number].links.[0].href
                # published
                published = entry[number].published

                ## Create transaction query for SQL database
                # check table names
                insert_query_table_name = re.sub(r'\W+', '', entry.feed.\
                                                 title)
                if self.match_names(insert_query_table_name, db_name)\
                   == True:
                    transaction_query = transaction_query + "INSERT INTO "\
                                        + insert_quer_table_name + \
                                        " VALUES(" + primary_key + "," +\
                                        title + "," + description + "," +\
                                        article_link + "," + published +\
                                        "; "
                else:
                    raise UserWarning("Something bad happened")
        
        transaction_query = transaction_query + " COMMIT;"
        return transaction_query



        
        
        
        
            
    def populate_db(self):
        # create a .sql script more or less
        # so we're going to create a string with each statement separated
        # by a semicolon. The string starts with BEGIN and ends with COMMIT
        # execute the script with BEGIN...COMMIT
        

    def populate_db(self):
        ''' 
        Queries are matched with dict keys which then
        provides the values associated with each query by sharing
        the table names as a reference point. This allows rows to be 
        populated for each table leading to the population of the db.
        '''
        # Insert queries across multiple tables
        for table_name in self.table().keys():
            self.c.execute("BEGIN; "\
                           

                           "COMMIT;")

            
            self.c.executemany(self.insert_query()[table_name],\
                          self.table()[table_name])
        print "\n populate_db is complete"

    def rm_duplicates(self):
        '''
        Limitation of this duplicate removal approach is that only one
        duplicate entry will be removed (containing the lowest valued
        primary_key). If the number of  duplicate entries per item  > 2
        then that will introduce a bug. 
        '''
        # Remove duplicate queries
        for table_name in self.table().keys():
            query = "DELETE FROM " + table_name + " WHERE primary_key " \
                    "NOT IN " \
                    "(SELECT min(primary_key) FROM " + table_name + \
                    " GROUP BY title, published);"
            self.c.execute(query)
            self.conn.commit()
        self.conn.close()
        print " rm_duplicates is complete"


