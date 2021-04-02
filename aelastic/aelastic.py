"""A Aminer-Elasticsearch importer

This module provides a class that starts a scheduler. This
scheduler queries the elasticsearch database in a specific
intervall and writes the results into the aminer unix-domain-socket.

TODOS
-----
* Make the programm stable with KeyboardInterrupt
* Create real elastic-search queries
"""
import threading
import logging
import json
import copy
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchException


class Aelastic:
    """
    A Aminer-Elasticsearch importer

    Attributes
    ----------
    timer : threading.timer
        timer for the scheduler
    stopper : boolean
        stops the scheduler
    sock : socket
        unix-domain-socket of aminer
    elasticsearch : Elasticsearch
        elasticsearch object
    savestate: boolean
        Enable persistence of the state
    timestamp: str
        Elasticsearch-field with the timestamp(for sorting)
    sleeptime: int
        Throttle-time if elasticsearch fails(reduces error-messages)
    output: boolean
        Prints _id and @timestamp to stdout if set to True

    Methods
    -------
    handler()
        scheduler-function that queries the elasticsearch database
    run()
        this function starts the scheduler
    close()
        this function closes the socket and stops the timer
    """
    DEFAULT_CONFIG = {
        'unixsock': '/var/lib/aelastic/aminer.sock',
        'host': 'http://localhost:9200',
        'searchsize': 100,
        'index': 'aminer',
        'statefile': '/var/lib/aelastic/state',
        'savestate': True,
        'timestamp': '@timestamp',
        'output': False,
        'sleeptime': 5
    }

    def __init__(self, **configs):
        self.config = copy.copy(self.DEFAULT_CONFIG)
        self.timer = None
        self.stopper = False
        self.sort = None
        self.sock = None
        self.logger = logging.getLogger(__name__)

        for key in self.config:
            if key in configs:
                self.config[key] = configs[key]

        self.elasticsearch = Elasticsearch([self.config['host']])
        self.loadstate()
        self.logger.debug(self.sort)

    def setlogger(self, logger):
        """Define a logger for this module
        """
        self.logger = logger

    def handler(self):
        """Scheduler-function that queries elasticsearch

        """
        try:
            self.elasticsearch.indices.refresh(index=self.config['index'])
            if self.sort is None:
                res = self.elasticsearch.search(index=self.config['index'],
                                                body={"query": {"match_all": {}},
                                                      "size": self.config['searchsize'],
                                                      "sort": [{self.config['timestamp']: "asc"}]})
            else:
                res = self.elasticsearch.search(index=self.config['index'],
                                                body={"query": {"match_all": {}},
                                                      "size": self.config['searchsize'],
                                                      "sort": [{self.config['timestamp']: "asc"}],
                                                      "search_after": self.sort})

            if res['hits']['hits']:
                self.sort = res['hits']['hits'][-1]["sort"]
                self.savestate()

            if self.config['output'] is True:
                print("######################################################################")
            for hit in res['hits']['hits']:
                if self.config['output'] is True:
                    print("%s - %s" % (hit['_id'],hit['_source']['@timestamp']))
                self.logger.debug(json.dumps(hit).encode("ascii"))
                self.sock.send(json.dumps(hit).encode("ascii"))
                self.sock.send("\n".encode())
                self.sock.send("\n".encode())


        except ElasticsearchException:
            self.logger.error("Error in elasticsearch-request", exc_info=False)
            self.sock.send("\n".encode())
            time.sleep(self.config['sleeptime'])
        except BrokenPipeError:
            self.logger.error("Client disconnected", exc_info=False)
            self.stopper = True

    def setsock(self, sock):
        """Setter for the unix-socket
        """
        self.sock = sock

    def savestate(self):
        """Save the search-state so that the search
           starts from the last looked up element
        """
        if self.config['savestate'] == 'True':
            try:
                filehandle = open(self.config['statefile'], 'w')
                json.dump(self.sort, filehandle)
                filehandle.close()
            except (IOError, json.JSONDecodeError):
                self.logger.error("Could not save state", exc_info=False)

    def loadstate(self):
        """Load the state and start from the last
           looked up element
        """
        try:
            filehandle = open(self.config['statefile'], 'r')
            self.sort = json.load(filehandle)
            self.logger.debug("Statefile loaded with timestamp: %s",
                              datetime.fromtimestamp(self.sort[0] / 1000))
            filehandle.close()
        except (IOError, json.JSONDecodeError):
            self.logger.error("Could not load state", exc_info=False)

    def run(self):
        """Starts the scheduler
        """
        try:
            while self.stopper is False:
                self.logger.debug("Starting another run..")
                self.handler()
        except KeyboardInterrupt:
            self.logger.debug("KeyboardInterrupt detected...")
            self.stopper = True

    def close(self):
        """Stops the socket and the scheduler
        """
        self.logger.debug("Cleaning up socket and scheduler")
        self.stopper = True
        if self.sock is not None:
            self.sock.close()
        self.savestate()
