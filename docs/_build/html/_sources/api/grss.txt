API
===

Some of these methods can be used to interact with a SQLite3 database. Others
are useful if you'd like to interact with the article data.

gRSS
----

.. autoclass:: gathernews.gRSS.CaptureFeeds
   :members: load_db, fix_create_table_bug, create_tables, populate_db,
	     rm_duplicates, read_file, get_tablenames, get_RSS_link,
	     make_table_names, rss_feeds_data
	     
	       
