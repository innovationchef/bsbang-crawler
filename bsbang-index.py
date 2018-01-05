#!/usr/bin/env python3

import argparse
import contextlib
import json
import logging
import os
import sqlite3

import bioschemas.indexers


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MAIN
parser = argparse.ArgumentParser('Index extracted JSONLD into Solr.')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store crawl information.')
args = parser.parse_args()

if not os.path.exists(args.path_to_crawl_db):
    logger.error('Crawl database %s does not exist', args.path_to_crawl_db)
    exit(1)

config = bioschemas.DEFAULT_CONFIG.copy()
config.update({
    'post_to_solr': True,
    'solr_json_doc_update_path': 'http://localhost:8983/solr/bsbang/update/json/docs'
})

indexer = bioschemas.indexers.SolrIndexer(config)

with sqlite3.connect(args.path_to_crawl_db) as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row

    with contextlib.closing(conn.cursor()) as curs:
        for row in curs.execute('SELECT jsonld, url FROM jsonld'):
            # print(row['jsonld'])
            logger.info('Indexing %s', row['url'])
            indexer.index(json.loads(row['jsonld']))
