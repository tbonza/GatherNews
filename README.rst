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

.. code-block:: pycon
		
    http://feeds.reuters.com/Reuters/worldNews
    http://rss.cnn.com/rss/money_latest.rss

You can then gather the news using the load_db() methods:

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

Documentation
-------------

Documentation is available at http://pythonhosted.org/GatherNews/

Contribute
----------

#. Issue tracker is here: https://github.com/Bonza-Times/GatherNews/issues
#. Feel free to email tylers.pile@gmail.com about anything.
#. Fork it!











