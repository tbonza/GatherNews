from nose.tools import assert_raises, assert_true
import sqlite3
from gathernews.gRSS import CaptureFeeds


class TestgRSS:
    def __init__(self):
        self.cls_initialized = False

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = "/home/tyler/code/GatherNews/"
        self.capture_feeds = CaptureFeeds(self.path)

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests

    def test_sqlite3_connection(self):
        """ Does the sqlite3 database connect properly? """
        assert_raises(Exception, sqlite3.connect(self.path + "FeedMe.db"))

    def test_get_RSS_link(self):
        """ Can we find and load the text file for the RSS links?"""
        assert len(self.capture_feeds.get_RSS_link()) > 0

    def test_do_tables_exist(self):
        """ Can we capture True, False, Error, conditions for
        do_tables_exist?
        """
        pass

    
        


    


