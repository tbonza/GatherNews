from nose.tools import assert_raises, assert_true, assert_false, eq_
import sqlite3
from gathernews.gRSS import CaptureFeeds
import os

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
        self.path = os.path.abspath("") + "/GatherNews/gathernews/tests/"
        
        ## Instantiating CaptureFeeds
        self.capture_feeds = CaptureFeeds(self.path)
        
        
    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests

    def test_read_file(self):
        """ Make sure that only RSS links are read from feeds_list.txt

        A list of bad RSS links have been placed in 'feeds_list.txt' so
        we should expect nothing to be returned. 
        """
        # set parameters to test data
        path = self.path
        your_file_name = "bad_feeds_list.txt"
        # make sure that none of the bad RSS links were returned
        assert_raises(UserWarning, self.capture_feeds.read_file, path,
                      your_file_name)


    def test_update_feeds_json(self):
        """ Make sure you can create/update a JSON object in ~/tests """
        # set parameters to test data
        path = self.path
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
        path = self.path 
        your_file_name = 'previous_feeds_list.json'
        ## We're going to pretend the JSON object isn't there
        assert_true(self.capture_feeds.does_json_exist(path,
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
        self.db_path = os.path.abspath("") + "/GatherNews/examples/"
        
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

        
        
class TestNewTableCreation:
    """ Make sure you can create new tables after recieving new table
        names. """
    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = os.path.abspath("") + "/GatherNews/gathernews/tests/"
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
        """ Make sure an error is raised if no RSS links have been added to
        'feeds_list.txt' """
        # Set parameters
        current_feeds_list = []
        previous_feeds_list = [] # empty list should never be returned here
        # Run test
        assert_raises(UserWarning, self.capture_feeds.create_these_tables,
                      current_feeds_list, previous_feeds_list)


    def test_do_tables_exist(self):
        """ See if tables which should be created are not found when they
        do not exist

        The error should be raised here from read_file()
        """
        tables = self.capture_feeds.do_tables_exist
        assert_false(tables())

    def test_create_tables(self):
        """ See if Warning is raised when we don't know if tables should
        be created or left alone """
        tables = self.capture_feeds.create_tables
        assert_false(tables())

        

class TestPopulateExistingTables:
    """ Make sure existing tables can be successfully populated with new
        information. """
    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = os.path.abspath("") +"/GatherNews/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(self.path)
        

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests

    def test_strip_garbage(self):
        """ Make sure the garbage is outta here! """
        # Set parameters
        description = u'Nicholas Lowinger, 15, has provided new shoes to '\
        +'more than 10,000 homeless children since 2010.<div class="feedfla'\
        +'re">\n<a href="http://rss.cnn.com/~ff/rss/cnn_world?a=sY9UQhCaa'\
        +'Bs:D0GXstdA6xE:yIl2AUoC8zA"><img border="0" src="http://feeds.f'\
        +'eedburner.com/~ff/rss/cnn_world?d=yIl2AUoC8zA" /></a> <a href="'\
        +'http://rss.cnn.com/~ff/rss/cnn_world?a=sY9UQhCaaBs:D0GXstdA6xE:7'\
        +'Q72WNTAKBA"><img border="0" src="http://feeds.feedburner.com/~ff/'\
        +'rss/cnn_world?d=7Q72WNTAKBA" /></a> <a href="http://rss.cnn.com/~'\
        +'ff/rss/cnn_world?a=sY9UQhCaaBs:D0GXstdA6xE:V_sGLiPBpWU"><img bord'\
        +'er="0" src="http://feeds.feedburner.com/~ff/rss/cnn_world?i=sY9UQ'\
        +'hCaaBs:D0GXstdA6xE:V_sGLiPBpWU" /></a> <a href="http://rss.cnn.co'\
        +'m/~ff/rss/cnn_world?a=sY9UQhCaaBs:D0GXstdA6xE:qj6IDK7rITs"><img b'\
        +'order="0" src="http://feeds.feedburner.com/~ff/rss/cnn_world?d=qj'\
        +'6IDK7rITs" /></a> <a href="http://rss.cnn.com/~ff/rss/cnn_world?a'\
        +'=sY9UQhCaaBs:D0GXstdA6xE:gIN9vFwOqvQ"><img border="0" src="http:/'\
        +'/feeds.feedburner.com/~ff/rss/cnn_world?i=sY9UQhCaaBs:D0GXstdA6xE'\
        +':gIN9vFwOqvQ" /></a>\n</div><img height="1" src="http://feeds.fee'\
        +'dburner.com/~r/rss/cnn_world/~4/sY9UQhCaaBs" width="1" />'

        # Run test
        cleaned = self.capture_feeds.strip_garbage(description)
        assert_true(len(cleaned) == 95)


    def test_strip_garbage2(self):
        """ Here we're concerned with successfully handling a 'NoneType'
        object that's returned when a regular expression does not find a
        value"""
        # Set parameters
        description = "The lazy brown foxy jumps over the foxy lady!"

        # Run test
        cleaned = self.capture_feeds.strip_garbage(description)
        assert_true(len(cleaned) == 45)


    def test_strip_garbage3(self):
        """ We want to make sure a warning is logged to
        the console if the HTML garbage bug is not squashed. """
        
        # Set parameters
        description = "<p>The lazy brown fox jumps over the foxy lady!</p>"

        # Run test
        assert_true(self.capture_feeds.strip_garbage(description) == None)

        # Note that a logged warning is of type 'None'. I think this is a
        # good test because regex_match() returns 'False' if the regular
        # expression search returns no result.


   
