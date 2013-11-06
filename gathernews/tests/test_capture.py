from nose.tools import assert_raises, assert_true

# capture feeds class imported for testing
from newsfind.capture_feed import CaptureFeeds

# Set filepath to your list of RSS feed addresses, use "feeds_list.txt"
path = "~/code/locomotion/examples/"

def test_sqlite3_connection(path):
    """ Does the sqlite3 database connect properly? """
    assert_raises(Exception,  sqlite3.connect(path + "FeedMe.db"))

def test_get_RSS_link(path):
    """ Can we find and load the text file for the RSS links?"""
    assert len(CaptureFeeds.get_RSS_link(path)) > 0

def test_do_tables_exist(path):
    """ Can we capture True, False, Error, conditions for do_tables_exist?"""
    RSS_links = CaptureFeeds.get_RSS_link(path)
    Table_Names = CaptureFeeds.get_tablenames()
    assert_raises(ValueError, len(RSS_links) == len(Table_Names))
    assert_raises(ValueError, capture_feed.do_tables_exist() != True)
    # Add an additional table name and see if it returns the correct value
    assert_raises(ValueError, len(capture_feed.do_tables_exist()) > 0,
                  capture_feed.get_tablenames().append("test_table"))


    
    
   
    
