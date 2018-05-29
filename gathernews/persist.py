""" Persist results from news feeds. """
import json
import logging
import os

logger = logging.getLogger(__name__)

def write_json(obj: list, outpath: str):
    try:
        with open(outpath, "w") as outfile:
            json.dump(obj, outfile)

    except Exception as exc:
        logger.exception(exc)

def read_json(inpath):
    try:
        with open(inpath, "r") as infile:
            data = json.load(infile)

    except Exception as exc:
        logger.exception(exc)


def persist_json(obj, fpath):
    """ Create or update json used to persist rss feed results. """
    try:
        if os.path.exists(fpath):
            data = read_json(fpath)
            data.append(obj)
            write_json(data, obj)
            logger.info("Updated {}".format(fpath))

        else:
            write_json(data, obj)
            logger.info("Created {}".format(fpath))

    except Exception as exc:
        logger.exception(exc)
