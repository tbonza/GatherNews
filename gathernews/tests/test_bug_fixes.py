from nose.tools import assert_raises, assert_true, assert_false, eq_

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
        
        
    def tearDown(self):
        assert self.cls_initialized
        self.cls_initialized = False

    # actual tests

    def test_fix_create_table_bug(self):
        """ Raise UserWarning: bug fix not needed """
        pass
