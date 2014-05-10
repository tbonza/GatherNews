from nose.tools import assert_raises, assert_true, assert_false, eq_
import os
from gathernews.bug_fixes import V1Bugs
from gathernews.gRSS import CaptureFeeds

class TestBugFixesV1(object):
    """ Make sure bug fixes are resolved for version 1 """

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

        ## Initializing V1Bugs
        self.v1_bugs = V1Bugs(self.path)
        
        
    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # The 'fix_create_table_bug' needs to be able to be called from both
    # gRSS, to be consistent with V0.2.1, and bug_fixes to be consistent
    # with versions going forward. These set of tests require a json file
    # to contain the same tables as the sqlite3 db; both are contained in
    # the test folder. 

    def test_fix_create_table_bug(self):
        """ Raise UserWarning: bug fix not needed """
        assert_raises(UserWarning, self.v1_bugs.fix_create_table_bug)
        assert_raises(UserWarning, self.capture_feeds.fix_create_table_bug)
