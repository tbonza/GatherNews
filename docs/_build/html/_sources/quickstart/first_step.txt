Start Quickly
=============

Alright, let's get you going. I'm assuming that your operating system is a
debian linux distribution like Ubuntu_, that you're using Python_ version
2.7, and that you are able to access your terminal_. We are going to load a
sqlite3 database with news articles from several RSS feeds.

Installation
------------

If you haven't already, you can install GatherNews via pip:

.. code-block:: console

    $ pip install gathernews

Project Setup
-------------

Now let's set up a project.

.. code-block:: console

    $ mkdir my_project
    $ cd my_project
    $ touch feeds_list.txt

Add the RSS feeds you want to "feeds_list.txt". Here are some that you may
want to use:

    * http://feeds.reuters.com/reuters/businessNews
    * http://feeds.reuters.com/reuters/entertainment
    * http://feeds.reuters.com/reuters/topNews
    * http://feeds.reuters.com/Reuters/worldNews
    * http://rss.cnn.com/rss/money_latest.rss
    * http://rss.cnn.com/rss/cnn_showbiz.rss
    * http://rss.cnn.com/rss/cnn_topstories.rss
    * http://rss.cnn.com/rss/cnn_world.rss

Load a SQLite3 database
-------------------------

Now, we're ready to load the SQLite3 database with articles from the RSS
feeds we've previously specified.

.. code-block:: console

    $ # First, let's get our project path and make note of it.
    $ pwd
    $ # Now we're ready to start up Python
    $ python

.. code-block:: python

    >>> from gathernews.gRSS import CaptureFeeds
    >>> capture_feeds = CaptureFeeds("/home/tyler/my_project/")
    >>> capture_feeds.load_db()

We've now created a new table for each one of the RSS feeds you previously
specified, populated each table, and removed any duplicate entries in those
tables.

Anytime you want to load the database with new articles from your RSS feeds,
we can just use the same method. Let's say you add additional tables to your
"feeds_list.txt", just use the same method; load_db().
		
.. _Ubuntu: http://www.ubuntu.com/
.. _Python: http://python.org/download/
.. _terminal: https://help.ubuntu.com/community/UsingTheTerminal
