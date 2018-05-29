""" Handle parsing the RSS feed. """

from datetime import datetime
import logging
import re

import feedparser

from gathernews.template import ITEM

logger = logging.getLogger(__name__)


def get_source(fp: feedparser.FeedParserDict()) -> str:
    try:
        return fp['feed']['title_detail']['base']
    except Exception as ex:
        logger.exception(ex)
        return ""

def left_pad(num: int) -> str:
    if len(str(num)) == 1:
        return "0" + str(num)
    else:
        return str(num)

def get_datetime(fp: feedparser.FeedParserDict()) -> str:
    try:
        tm = fp['feed']['updated_parsed']
        return str(tm.year) + left_pad(tm.month) + left_pad(tm.day) + \
            left_pad(tm.hour) + left_pad(tm.minute)

    except Exception as exc:
        logger.exception(exc)
        tm = datetime.now()
        return str(tm.year) + left_pad(tm.month) + left_pad(tm.day) + \
            left_pad(tm.hour) + left_pad(tm.minute)

def get_title(entry: feedparser:FeedParserDict()) -> str:
    try:
        return entry['title']

    except Exception as exc:
        logger.exception(exc)
        return ""

def get_summary(entry: feedparser.FeedParserDict()) -> str:
    try:
        return entry['summary']

    except Exception as exc:
        logger.exception(exc)
        return ""

def get_rss_link(entry: feedparser.FeedParserDict()) -> str:
    try:
        return entry['link']

    except Exception as exc:
        logger.exception(exc)
        return ""

def get_date_published(entry: feedparser.FeedParserDict()) -> str:
    try:
        return entry['published']

    except Exception as exc:
        logger.exception(exc)
        return ""


def map_rss(fp: feedpaser.FeedParserDict()) -> list:
    """ Map rss entry items to data template. """
    items = []

    for entry in fp['entries']:
    
        item = ITEM.copy()
        
        item['source'] = get_source(fp)
        item['extract_datetime'] = get_datetime(fp)
        item['title'] = get_title(entry)
        item['summary'] = get_summary(entry)
        item['rss_link'] = get_rss_link(entry)
        item['published'] = get_date_published(entry)

        items.append(item)

    return items

