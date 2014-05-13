from nose.tools import assert_raises, assert_true, assert_false, eq_
import os
from gathernews.gRSS import CaptureFeeds
from gathernews.rm_garbage import FilterGarbage


class TestFilterGarbage:
    """ Make sure garbage is successfully filtered out. """
    
    def __init__(self):
        self.cls_initialized = False        

        
    def setUp(self):
        assert not self.cls_initialized
        self.cls_initialized = True
        self.path = os.path.abspath("") +"/GatherNews/gathernews/tests/"
        self.capture_feeds = CaptureFeeds(self.path)
        self.rm_garbage = FilterGarbage()
        

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
        cleaned = self.rm_garbage.strip_garbage(description)
        assert_true(len(cleaned) == 95)


    def test_strip_garbage2(self):
        """ Here we're concerned with successfully handling a 'NoneType'
        object that's returned when a regular expression does not find a
        value"""
        # Set parameters
        description = "The lazy brown foxy jumps over the foxy lady!"

        # Run test
        cleaned = self.rm_garbage.strip_garbage(description)
        assert_true(len(cleaned) == 45)


    def test_strip_garbage3(self):
        """ We want to make sure a warning is logged to
        the console if the HTML garbage bug is not squashed. """
        
        # Set parameters
        description = "<p>The lazy brown fox jumps over the foxy lady!</p>"

        # Run test
        assert_true(self.rm_garbage.strip_garbage(description) == None)

        # Note that a logged warning is of type 'None'. I think this is a
        # good test because regex_match() returns 'False' if the regular
        # expression search returns no result.


    def test_regex_match(self):
        """ Regex match will break with more than 1 group matching
            or if an arbitrary string is passed """
        assert_raises(AttributeError, self.rm_garbage.regex_match, "")


    def test_for_fucks_sake(self):
        """ Perhaps this method isn't entirely necessary; let's check """
        pass # will have to look more into this with xml_settings
