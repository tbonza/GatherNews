"""
========================================
Loading multiple RSS feeds into SQLite3 
========================================

An example showing how the News-Project can be used load news articles from
RSS feeds into a database. This example allows you to create new tables
and load a SQLite3 database with News from multiple RSS feeds. 

The list of RSS feeds is located at "~/examples/feeds_list.txt". The sqlite3
database is located at "~/examples/FeedMe.db".

Before running, go to "~/newsfind/capture.py" and adjust the name of your
filepath located in the __init__() method. Your filepath needs to point at
both 'feeds_list.txt' and 'FeedMe.db'.

Feel free to contact me if you run into any problems. 
"""
print(__doc__)

# Author: Tyler Brown <tylers.pile@gmail.com>

# Import RSS feed capture class
from gathernews.capture import CaptureFeeds

# File path to where "feeds_list.txt" is located
file_path = "/home/tyler/code/GatherNews/examples/"
# Instantiate the class
capture_feeds = CaptureFeeds(file_path)

# Create new tables if any new RSS feed addresses have been added
print " Checking for new tables"
capture_feeds.create_tables()
# Populate all tables with RSS news feeds
print " Populating the SQLite3 database"
capture_feeds.populate_db()
# Remove duplicate entries
print " Removing duplicate entries from SQLite3 database"
capture_feeds.rm_duplicates()



