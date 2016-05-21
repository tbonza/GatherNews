""" Handle parsing the RSS feed. """

import re

import feedparser


class FilterGarbage:
    """ Filter out any garbage from Feedparser input """


    def regex_match(self, regex):
        """ Return the regular expression match if it exists

        Args:
            regex: Includes the regular expression pattern and the phrase
                   to be checked.

        Returns:
            False if no match is found; otherwise, the first group is
            returned because we expect no more than one group in this
            module. 
        """
        if regex is None:
            return False
        return regex.group(0)

        
    def strip_garbage(self, description):
        """ Remove HTML garbage from the description

        Args:
            description: An article's description from the RSS Feed
        
        Returns:
            A string that does not include HTML garbage

        Raises:
            Warning: Logged when HTML garbage is not successfully removed.
        """
        # Check to see if HTML code is included in the description
        html_brackets = re.compile("[<].*[>]")
        if self.regex_match(html_brackets.search(description)) != False:
            
            # Use known patterns to solve the description bug
            pattern1 = re.compile("^.*?(?=<div)")
            pattern2 = re.compile("^.*?(?=<img)")

            # If known patterns are not able to resolve the description
            # bug then a warning will be logged to the user's console
            if self.regex_match(pattern1.search(description)) != False:
                return self.regex_match(pattern1.search(description))

            elif self.regex_match(pattern2.search(description)) != False:
                return self.regex_match(pattern2.search(description))
                
            else:
                logging.warning("HTML garbage not successfully removed\n"\
                                +" from the article description. Please\n"\
                                +" file a bug report using \n"\
                                +" 'https://github.com/Bonza-Times/Gath"\
                                +"erNews/issues'\n with this message: ")
                print description 
                
        else:
            return description


    def for_fucks_sake(self, description):
        """ This is apparently a bug fix for the description issue """
        fucking_hell = self.strip_garbage(description)
        return self.strip_garbage(fucking_hell)



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



