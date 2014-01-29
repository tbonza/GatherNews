from nose.tools import assert_raises, assert_true, assert_false
import sqlite3
from gathernews.gRSS import CaptureFeeds

class TestNewTablesCreated:
    """ Check to see if new tables names are created when new RSS links
        are added."""
    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True

        ## Setting file paths
        # File path to feeds_list.txt
        self.path = "/home/tyler/code/GatherNews/gathernews/tests/"
        # File path to previous_feeds_list.json
        self.json_path = "/home/tyler/code/GatherNews/gathernews/"\
                         + "tests/gathernews/"
        
        ## Instantiating CaptureFeeds
        self.capture_feeds = CaptureFeeds(self.path)
        
        
    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests

    def test_read_file(self):
        """ Make sure that only RSS links are read from feeds_list.txt"""
        # set parameters to test data
        path = self.path
        your_file_name = "feeds_list.txt"
        # make sure the 8 rss links were returned
        assert_true(len(self.capture_feeds.read_file(path,
                                                     your_file_name)) == 8)

    def test_update_feeds_json(self):
        """ Make sure you can create/update a JSON object in ~/tests """
        # set parameters to test data
        path = self.json_path
        # Set create_these_tables to 0 so False is returned
        create_these_tables = []
        # Let's assume we haven't created tables previously. 
        previous_feeds_list = []
        # This list matches '~/tests/feeds_list.txt'
        current_feeds_list = ["http://feeds.reuters.com/reuters/topNews",
                              "http://feeds.reuters.com/Reuters/worldNews",
                              "http://rss.cnn.com/rss/money_latest.rss",
                              "http://rss.cnn.com/rss/cnn_showbiz.rss",
                              "http://rss.cnn.com/rss/cnn_topstories.rss",
                              "http://rss.cnn.com/rss/cnn_world.rss"]
        ## We don't need to create a table so this is returned false
        assert_false(self.capture_feeds.\
                     update_feeds_json(path, create_these_tables,
                                       previous_feeds_list,
                                       current_feeds_list))

    def test_does_json_exist(self):
        """ Make sure you can access the JSON object """
        # set parameters to test data
        path = self.json_path 
        your_file_name = 'previous_feeds_list.json'
        ## We're going to pretend the JSON object isn't there
        assert_false(self.capture_feeds.does_json_exist(path,
                                                        your_file_name))
class TestNewTablesCreated2:
    """ Check to see if new tables names are created when new RSS links
        are added BUT use instantiate the class with a different file
        path to test methods against SQLite3 FeedMe.db."""

    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True

        ## Setting file paths
        # File path to FeedMe.db
        self.db_path = "/home/tyler/code/GatherNews/examples/"
        
        ## Instantiating CaptureFeeds
        self.capture_feeds = CaptureFeeds(self.db_path)
        
        
    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests
    
    def test_get_tablenames(self):
        """ Tests the SQLite3 connection as well as this method """
        # Now let's test the method for tables existing in the "~/examples/"
        # SQLite3 database
        assert_true(len(self.capture_feeds.get_tablenames()) > 1)

        
        
class TestNewTableCreation:
    """ Make sure you can create new tables after recieving new table
        names. """
    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = "/home/tyler/code/GatherNews/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(self.path)
        

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests

    def test_make_table_names(self):
        """ Parse an RSS link and create a table name """
        # Set parameters
        RSS_link = "http://feeds.reuters.com/Reuters/worldNews"
        create_these_tables = []
        # Run test
        assert_true(self.capture_feeds.make_table_names(RSS_link,
                                                        create_these_tables)\
                    [0] == "ReutersWorldNews")


    def test_create_these_tables(self):
        pass


class TestPopulateExistingTables:
    """ Make sure existing tables can be successfully populated with new
        information. """
    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = "/home/tyler/code/GatherNews/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(self.path)
        

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests


class TestDuplicateRemoval:
    """ Make sure duplicate entries can be successfully removed. """
        
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = "/home/tyler/code/GatherNews/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(self.path)
        

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests
