"""
========================================
Loading multiple RSS feeds into SQLite3 
========================================

An example showing how GatherNews can be used load news articles from
RSS feeds into a database. This example allows you to create new tables
and load a SQLite3 database with News from multiple RSS feeds. 

Feel free to contact me if you run into any problems. 
"""
print(__doc__)

# Author: Tyler Brown <tylers.pile@gmail.com>

# Import RSS feed capture class
from gathernews.gRSS import CaptureFeeds

# File path to where "feeds_list.txt" is located
file_path = "/home/tyler/code/GatherNews/examples/"
# Instantiate the class
capture_feeds = CaptureFeeds(file_path)
# Create tables, load database, remove duplicates
capture_feeds.load_db()



