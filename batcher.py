"""
API service that efficiently calls an API endpoint recursively on a sequence of entity
objects, e.g. posts, comments or adcampaigns, ads, etc. Typical use case includes
creating a large number of ads on a social API such as the Facebook or Twitter Ads API.

The service supports three strategies to push entities to an API endpoint: sequential,
concurrent and batch. See ApiBatcher class.

For illustration purposes we're using a dummy Post entity. See Post class.
"""
from collections import defaultdict
import os
import random
import time

import requests

from strategy import (API_POST,
                      API_SYNC,
                      SequentialStrategy,
                      BatchStrategy,
                      ConcurrentStrategy)

API_STRATEGY = defaultdict(ConcurrentStrategy, {'sequential': SequentialStrategy,
                                                'concurrent': ConcurrentStrategy,
                                                'batch': BatchStrategy})


class Post(object):
    """ A dummy entity object that represents a Post with one text attribute. It
    exposes two methods, sync and post, respectively to GET and POST the entity to
    an API endpoint. The API itself also has no real-world application.
    """
    root_url = "http://jsonplaceholder.typicode.com/"
    # Or: root_url = "http://graph.facebook.com/"

    def __init__(self, data):
        self.data = data
        self.id = None  # unique id returned by the API

    def sync(self):
        """ GET the entity from the API. """
        requests.get("{root}/posts/{id}".format(root=self.root_url, id=str(self.id)))
        # Set post variables here...

    def post(self):
        """ POST the entity to the API. """
        requests.post("{root}/posts".format(root=self.root_url),
                      data={"title": self.data, "body": self.data})
        # Save post id here...
        self.id = random.randint(0, 100)  # using random int as example

    def save(self):
        """ Persist the entity to a database. Not implemented. """
        pass


class ApiBatcher(object):
    """ API service that allows pushing entities to an API in batches.
    >>> api = ApiBatcher()
    >>> api.enqueue(post1)
    >>> api.enqueue(post2)
    >>> api.push()

    It supports three API strategies that can be defined through dependency injection
    or env var (API_MODE): sequential, concurrent and batch. Dependency injection takes
    precedence over env var. The default strategy is sequential.

    * Sequential (default)
          Basic strategy which processes entities sequentially in a loop.

    * Concurrent
          Multiple API calls are made concurrently for each entity.

    * Batch
          One single API call is made for all enqueued entities. This strategy is not
          always available as some API providers do not provide a batch mode.
          Example: https://developers.facebook.com/docs/marketing-api/batch-requests
    """
    def __init__(self, strategy=None):
        """
        :param strategy: The API strategy to use when interacting with the API.
        :type strategy: SequentialStrategy or BatchStrategy or ConcurrentStrategy
        """
        self.entities = []  # buffer to hold entities that need to be processed
        self.strategy = strategy or API_STRATEGY[os.getenv('API_MODE')]

    def enqueue(self, new_entity):
        """ Queue up an entity for processing.
        :param new_entity: Entity to be added.
        """
        self.entities.append(new_entity)

    def push(self):
        """ Push all queued entities to API, sync them back (and persist to db).  """
        if not self.entities:
            raise RuntimeError("No entity in the queue")

        self.strategy.do(API_POST, self.entities)
        self.strategy.do(API_SYNC, self.entities)
        # Persist to db...


if __name__ == "__main__":
    dataset_size = 10

    print
    print "Starting sequential mode..."
    start = time.time()
    api = ApiBatcher(strategy=SequentialStrategy())
    for i in range(dataset_size):
        api.enqueue(Post("post" + str(i)))
    api.push()
    print "Done - Execution time: {0}".format(str(time.time() - start))

    print
    print "Starting concurrent mode..."
    start = time.time()
    api = ApiBatcher(strategy=ConcurrentStrategy())
    for i in range(dataset_size):
        api.enqueue(Post("post" + str(i)))
    api.push()
    print "Done - Execution time: {0}".format(str(time.time() - start))
