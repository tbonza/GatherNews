from nose.tools import assert_raises, assert_true, assert_false, eq_
from gathernews.gRSS import CaptureFeeds
from gathernews.io import ReadFiles, WriteFiles
import json
import re
import os


class TestReadFiles(object):
    """ Test anything associated with ReadFiles() """

    def __init__(self):
        self.cls_initialized = False
        

    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True

        ## Setting file paths
        # File path to feeds_list.txt
        #self.path = os.path.abspath("") + "/GatherNews/gathernews/tests/"
        self.path = os.path.abspath("") + "/gathernews/tests/"
        
        ## Instantiating classes
        #self.capture_feeds = CaptureFeeds(self.path)
        self.read_files = ReadFiles(self.path)
        self.write_files = WriteFiles(self.path)
        
        
    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False


    def test_read_file(self):
        """ Make sure that only RSS links are read from feeds_list.txt

        A list of bad RSS links have been placed in 'feeds_list.txt' so
        we should expect nothing to be returned. 
        """
        # set parameters to test data
        path = self.path
        your_file_name = "bad_feeds_list.txt"
        # make sure that none of the bad RSS links were returned
        #assert_raises(UserWarning, self.capture_feeds.read_file, path,
         #             your_file_name)
        # can also access in gathernews.io
        assert_raises(UserWarning, self.read_files.read_file, path,
                      your_file_name)

    def test_does_json_exist(self): ## Find out what's going on with this 
        """ Make sure you can access the JSON object """
        # set parameters to test data
        path = self.path 
        your_file_name = "previous_feeds_list.json"
        ## We're going to pretend the JSON object isn't there
        #assert_false(self.capture_feeds.does_json_exist(path,
        #                                                your_file_name))
        # can also access in gathernews.io
        assert_false(self.read_files.does_json_exist(path, your_file_name))

        
    def test_get_RSS_link(self):
        """ read_file() can be accessed gRSS and io """
        # gathernews.gRSS
        #assert_true(len(self.capture_feeds.get_RSS_link()) == 8)
        # gathernews.io
        assert_true(len(self.read_files.get_RSS_link()) == 8) 

    
class TestWriteFiles(TestReadFiles):
    """ Test anything associated with WriteFiles() """

    
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
        #assert_false(self.capture_feeds.\
        #             update_feeds_json(path, create_these_tables,
        #                               previous_feeds_list,
        #                               current_feeds_list))
        # Make sure it's also working for gathernews.io
        assert_false(self.write_files.\
                     update_feeds_json(path, create_these_tables,
                                       previous_feeds_list,
                                       current_feeds_list))

        
