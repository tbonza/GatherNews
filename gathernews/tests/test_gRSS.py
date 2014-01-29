from nose.tools import assert_raises, assert_true
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
        self.path = "/home/tyler/code/GatherNews/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(self.path)
        

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests


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
