from nose.tools import assert_raises, assert_true, assert_false, eq_
from gathernews.sqlite3_io import Sqlite3IO
import os

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
        self.db_path = os.path.abspath("") + "/gathernews/tests/"
        
        ## Instantiating CaptureFeeds
        self.sqlite3_io = Sqlite3IO(self.db_path)
        
        
    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests
    
    def test_get_tablenames(self):
        """ Tests the SQLite3 connection as well as this method """
        # Now let's test the method for tables existing in the "~/examples/"
        # SQLite3 database
        assert_true(len(self.sqlite3_io.get_tablenames()) > 1)


    def test_create_tables(self):
        """ See if Warning is raised when we don't know if tables should
        be created or left alone """
        tables = self.sqlite3_io.create_tables
        assert_false(tables())


class TestNewTableCreation:
    """ Make sure you can create new tables after recieving new table
        names. """
    
    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = os.path.abspath("") + "/GatherNews/gathernews/tests/"
        self.sqlite3_io = Sqlite3IO(self.path)
        

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests
    pass

    


