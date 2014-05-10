import re
import logging


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
