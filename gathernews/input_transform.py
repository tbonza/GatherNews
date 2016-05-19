


class InputTransform(object):

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
