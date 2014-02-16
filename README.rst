===========
GatherNews
===========

Gathers unstructured news data and commits it to a SQLite3 database.The goal
for GatherNews is to quickly and simply capture news data.

GatherNews allows you to specify which News sites you want to capture by
providing the RSS link in "feeds_list.txt" like this:

.. code-block:: pycon
		
    http://feeds.reuters.com/Reuters/worldNews
    http://rss.cnn.com/rss/money_latest.rss

You can then gather the news using the load_db() method:

.. code-block:: pycon
		
    >>> # Create new tables if any new RSS feed addresses have been added
    >>> # Populate all tables with RSS news feeds
    >>> # Remove duplicate entries
    >>> capture_feeds.load_db()

The examples folder contains working code for each module.

Features
--------

- Creates tables with a predefined schema
- Populates each table in the SQLite3 database with articles
- Removes duplicate articles from each table
- Includes bug fixes for issues raised about version 0.1.0
- Faster than version 0.1.0, see the benchmarks!

Installation
------------

To install GatherNews use pip:

.. code-block:: bash
		
    $ pip install gathernews

Testing
-------

After installation, you can launch the test suite from outside the source
directory (you will need to have nosetests installed):

.. code-block:: bash

    $ nosetests --exe GatherNews

Bug Resolution
--------------

In GatherNews 0.1.0, a bug was introduced that does not allow you to add new
RSS feeds to the ‘feeds_list.txt’ after your initial call of the
create_tables() method. Before using version 0.2.0 on a preexisting database
call the following method.

.. code-block:: pycon

    >>> path = "path/to_your/existing_sqlite3_db/
    >>> from gathernews.gRSS import CaptureFeeds
    >>> capture_feeds = CaptureFeeds(path)
    >>> capture_feeds.fix_create_table_bug()

If this gives you any problems, email me directly (tylers.pile@gmail.com).
Thanks.
 
Documentation
-------------

Documentation is available at http://gathernews.readthedocs.org/en/latest/

Contribute
----------

#. Issue tracker is here: https://github.com/Bonza-Times/GatherNews/issues
#. Fork it!











