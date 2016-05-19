""" Handle database interactions. """

import sqlite3
import uuid


class SqliteDB(object):
    """ Handle interactions with SQLite3 database. """

    def __init__(self):
        sqlite3.register_converter('GUID',
                                   lambda b: uuid.UUID(bytes_le=b))
        sqlite3.register_adapter(uuid.UUID,
                                 lambda u: buffer(u.bytes_le))

        self.conn = sqlite3.connect('Feeds.db',
                                    detect_types=sqlite3.PARSE_DECLTYPES)
    
    def get_tablenames(self):
        """ All table names are extracted for use in SQL queries.

        Returns:
            revised_list: A list of all table names in the database.
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

    def create_tables(self):
        """ Creates tables for RSS news feeds

        Creates db tables where each RSS link feeds
        into a separate table because it's easier
        to aggregate then deaggregate.
        """
        tables = self.capture_feeds.do_tables_exist()
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

    def transaction_query(self):
        """ Snagged this from gRSS, not at all working """
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

    def process_metadata(self):
        """ Generate metadata from input text file. """
        self.RSS_link_list = path + "feeds_list.txt"



    def metadata(self):
        """ Maintain a metadata table. """
        pass


    def feed_data(self):
        """ Maintain list of RSS feeds in sqlite3 table. """
        pass
                
