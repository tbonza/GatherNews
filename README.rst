===========
GatherNews
===========

Gathers unstructured News data and commits it to a SQLite3 database.

News is valuable when it contains actionable information. Collecting the news
for text analytics should be easy; even if the news is unstructured data. The
goal for GatherNews is to quickly and simply gather News data. We want to
know who, what, when, where, why, and how. We want it in a SQL database.

GatherNews allows you to specify which News sites you want to capture by
providing the RSS link in "feeds_list.txt" like this:

    http://feeds.reuters.com/Reuters/worldNews
    
    http://rss.cnn.com/rss/money_latest.rss

You can then gather the news using these methods:

.. code-block:: pycon
		
    >>> # Create new tables if any new RSS feed addresses have been added
    >>> capture_feeds.create_tables()
    >>> # Populate all tables with RSS news feeds
    >>> capture_feeds.populate_db()
    >>> # Remove duplicate entries
    >>> capture_feeds.rm_duplicates()

The examples folder contains working code integrating each module.

Features
--------

- Parses RSS feeds and commits each news article to SQLite3 database
- Works around URL Encode Errors

Installation
------------

To install GatherNews use pip:

.. code-block:: bash
		
    $ pip install gathernews

Documentation
-------------

Documentation is available at https://github.com/Bonza-Times/GatherNews/wiki

Contribute
----------

#. Issue tracker is here: https://github.com/Bonza-Times/GatherNews/issues
#. Feel free to email tylers.pile@gmail.com about anything.
#. Fork it!











