from nose.tools import assert_raises, assert_true
import sqlite3
from gathernews.gRSS import CaptureFeeds

class TestSlowgRSS:
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
        

class TestgRSSWithMocKData:
    def __init__(self):
        self.cls_initialized = False

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True

    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests
    def test_additional_table_creation(self):
        """ Make sure additional tables can be added """
        path = "/home/tyler/code/GatherNews/gathernews/tests/"
        capture_feeds = CaptureFeeds(path)
        try:
            assert len(capture_feeds.do_tables_exist()) > 0
        except:
            # Reset mock data
            f = open(path + "gathernews/" + "previous_feeds_list.txt", 'w')
            f.write("")
            f.close()
            # Alright, let's give it another go
            assert len(capture_feeds.do_tables_exist()) > 0
