""" Handle parsing the RSS feed. """

import re

import feedparser


class ParseFeed(object):
    """ Parse RSS feed for fields of interest. """

    def title(self, size):
        """ Syncs up with xml_settings to return title """
        try:
            title = article.title_detail.value
        except:
            title = ""
            logging.warning("title not found")

        
    def description(self, size):
        """ Syncs up with xml_settings to return description """
        # summary/description
        try:
            description = self.for_fucks_sake(article.\
                                              summary_detail.value)
        except:
            description = ""
            logging.warning("description not found")


    def article_link(self, size):
        """ Syncs up with xml_settings to return article_link """
        # link
        try:
            article_link = article.links[0].href
        except:
            article_link = ""
            logging.warning("article link not found")


    def date_published(self, size):
        """ Syncs up with xml_settings to return date published """
        # published
        try:
            published = article.published
        except:
            published = ""
            logging.warning("date/time published not found")


        def make_tuple(self, size):
        """ Return a tuple to be appended to a list of News tuples """
        return (self.unique_id(),
                self.title(size),
                self.description(size),
                self.article_link(size),
                self.date_published(size))

        
    def add_tuples(self, key):
        """ Returns a list of tuples as a value for the primary key """
        size = 0
        list_of_tuples = []
        while size < self.num_rss_items_returned():
            list_of_tuples.append(self.make_tuple(size))
            size += 1
            
        return list_of_tuples

         

    def rss_feeds_data(self):
        """ Returns data structure used for loading db in GatherNews """
        load_this_data = {}
        count = 0
        while count < number_of_rss_feeds:
            load_this_data[key] = self.add_tuples(key)
            count += 1

        return load_this_data

    def primary_key(self):
        """ Returns primary key to map onto values """
        return uuid.uuid1()



