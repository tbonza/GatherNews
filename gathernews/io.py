import re
import json

class ReadFiles(object):
    """ Does anything related to reading from file storage """

    def __init__(self, path):
        self.path = path
        # Path corresponds to feeds_list.txt. 
        self.RSS_link_list = path + "feeds_list.txt"
        # Path corresponds to previous_feeds_list.json. 
        self.previous_path = path

    
    def read_file(self, path, your_file_name):
        """ Reads in file so that only rss links are included

        Unfortunately, .readlines() or .read() alone was sucking in extra
        '\n' symbols not related to the RSS links. This approach uses regular
        expressions to only list items that are consistent with an RSS feed
        link. 

        Args:
            path: the file path. Ex. "\home\tyler\Gathernews\gathernews\"
            your_file_name: name of file you want to read

        Returns:
            List of strings where each string is a link to an RSS feed

        Raises:
            UserWarning: "Could not recognize the file"
        
        """
        your_file = open(path + your_file_name, 'r').read()
        f = your_file.split("\n")
        pattern = re.compile("^[http]+")
        clean_file = []
        # Make sure only rss feeds are returned
        for link in f:
            if pattern.search(link):
                clean_file.append(link)
        if len(clean_file) == 0:
            raise UserWarning("Could not recognize the file")
        return clean_file


    def does_json_exist(self, path, your_file_name):
        """ If a json object exists then return it

        Args:
            file_name: This is the name of your file.

        Returns:
            A json object from your specified path is returned.
        """
        try:
            with open(path + your_file_name, 'r') as f:
                return json.load(f)
        # At some point you should create a method that checks to see if the
        # file path given by the user is accurate. 
        except:
            return False

    
    def get_RSS_link(self):
        """RSS links used to pull feeds"""
        return self.read_file(self.path, "feeds_list.txt")
        

class WriteFiles(ReadFiles):
    """ Does anything related to writing from file storage """
    # Not sure what this will inherit for a file_path from ReadFiles
    # under which conditions, but hey, isn't learning fun
    
    def update_feeds_json(self, path, create_these_tables,
                          previous_feeds_list, current_feeds_list):
        """ A JSON object of table_names in the database is updated.

        Args:
            path: The filepath to the JSON object to be updated
            create_these_tables: A list of table names that will be entered
                                 into the database. 
            previous_feeds_list: A list of RSS feed links corresponding to
                                 table names that are in the database.
            current_feeds_list: A list of RSS feed links that may correspond
                                to table names that are not in the database.

        Returns:
            No items are returned. This method writes a JSON object to disk.
        """
        # update previous_feeds_list with info from current_feeds_list
        if len(create_these_tables) > 0:


            # line 225 is crashing the ca
            # issue needs to be resolved here == current_feeds_list
            previous_feeds_list = current_feeds_list
            # The list is written as a JSON object to your disk.

            # there will be a bug here if you don't resolve the file
            # path issue where feeds_lists.txt wants something different
            with open(path + 'previous_feeds_list.json',
                      mode = 'w') as f:
               return json.dump(previous_feeds_list, f)
        else:
            return False
