import feedparser
import sqlite3
from simpleflake import * 
import re

### WOW so this needs some improvements.
# Holy shit fix the doc strings
# several bugs have been documented, fix those
# for the love of god write more tests

## Point of departure
  # Bugs still remain, damnit!
  # Run tests specific to read_file() and go from there


class CaptureFeeds:
    """ Commits RSS news feeds to a SQLite3 database  """
    def __init__(self, path):
        self.path = path
        self.RSS_link_list = self.path + "feeds_list.txt"

    def read_file(self, path, your_file_name):
        """ Reads in file so that only rss links are included

        Unfortunately, .readlines() or .read() alone were sucking in extra
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
        pattern = re.compile("[http]+")
        clean_file = []
        if len(f) == 0:
            raise UserWarning("Could not recognize the file")
        # Make sure only rss feeds are returned
        for link in f:
            if pattern.search(link):
                clean_file.append(link)
        return clean_file
                
    def get_RSS_link(self):
        '''RSS links used to pull feeds'''
        f = self.read_file(self.path, "feeds_list.txt")
        return f

    def get_tablenames(self):
        ''' Table names are cleaned for SQL queries'''
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

    def do_tables_exist(self): 
        """ Checks to see if new tables should be created


        # This was failing silently so it's unplugged and here
        # to reference

        """
        previous_feeds_list = [elt for elt in
                               open(self.path + "gathernews/" +\
                                    "previous_feeds_list.txt", "r")]
        current_feeds_list = self.get_RSS_link()
        create_these_tables = []
        for RSS_link in current_feeds_list:
            if RSS_link not in previous_feeds_list and len(RSS_link) > 1:
                d = feedparser.parse(RSS_link)
                table_name = re.sub(r'\W+', '', d.feed.title)
                create_these_tables.append(table_name)
            elif RSS_link in previous_feeds_list:
                pass
            else:
                raise UserWarning("Blank entry found, can't make table_name")

        # update previous_feeds_list with info from current_feeds_list
        if len(create_these_tables) > 0:
            previous_feeds_list = current_feeds_list
            f = open(self.path + "gathernews/" +\
                     "previous_feeds_list.txt", 'w')
            for item in previous_feeds_list:
                f.write("%s" % item)
            f.close()
            
        return create_these_tables
        
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

    def strip_garbage(self, description):
        '''
        Article descriptions were returning some garbage
        '''
        # should include some if/else statements and check to see if the
        # length of the string is changing
        desc_length = len(description)
        sep = '<div'
        stripped = description.split(sep, 1)[0]
        if stripped < desc_length:
            return stripped
        elif stripped == desc_lenth:
            sep = '<img'
            stripped = description.split(sep, 1)[0]
            return stripped
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
        conn.close()
        print " rm_duplicates is complete"

    def populate_and_rm_duplicates(self):
        # open and close database within this method
        pass




