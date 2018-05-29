from nose.tools import assert_raises, assert_true, assert_false, eq_
import sqlite3
from gathernews.gRSS import CaptureFeeds
import os


class TestNewTableCreation:
    """ Make sure you can create new tables after recieving new table
        names. """
    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        #self.path = os.path.abspath("") + "/GatherNews/gathernews/tests/"
        self.path = os.path.abspath("") + "/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(self.path)
        

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False


    def test_make_table_names(self):
        """ Parse an RSS link and create a table name """
        # Set parameters
        RSS_link = "http://feeds.reuters.com/Reuters/worldNews"
        create_these_tables = []
        # Run test
        assert_true(self.capture_feeds.make_table_names(RSS_link,
                                                        create_these_tables)\
                    [0] == "ReutersWorldNews")

    def test_match_names(self):
        """ Make sure a SQL database table name can be matched to a table
        name used in an insert query. """

        # Set parameters
        query_name = "ReutersWorldNews"

        # Run test
        assert_true(self.capture_feeds.match_names(query_name) == True)

        # Note that this method is actually part of the
        # PopulateExistingTables() test class. However, the file path
        # used for testing is shared with the TestNewTablesCreated2()
        # class so here we've arrived.


    def test_do_tables_exist(self):
        """ See if tables which should be created are not found when they
        do not exist

        The error should be raised here from read_file()
        """
        tables = self.capture_feeds.do_tables_exist
        assert_false(tables())


    def test_create_these_tables(self):
        """ Make sure an error is raised if no RSS links have been added to
        'feeds_list.txt' """
        # Set parameters
        current_feeds_list = []
        previous_feeds_list = [] # empty list should never be returned here
        # Run test
        assert_raises(UserWarning, self.capture_feeds.create_these_tables,
                      current_feeds_list, previous_feeds_list)
        
    


    

    


        
        



    
        




   
