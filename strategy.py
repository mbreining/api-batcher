import concurrent.futures as futures
import logging

API_POST = 'post'
API_SYNC = 'sync'


class BaseStrategy(object):
    """ Base parent class for all strategies. """
    valid_actions = [API_POST, API_SYNC]  # also DELETE, UPDATE, PATCH

    def do(self, action, entities):
        """ Take a sequence of entities and apply the API action on them. How the action
        is performed on the sequence of entities is left to the concrete classes.

        :param action: POST or GET
        :param entities: A sequence of entity objects
        """
        if action not in self.valid_actions:
            raise RuntimeError("Invalid action {0}".format(action))
        if not entities:
            raise RuntimeError("No entities to process")


class SequentialStrategy(BaseStrategy):
    """ Basic strategy that loops over each entity one at a time. """
    def do(self, action, entities):
        super(SequentialStrategy, self).do(action, entities)

        for entity in entities:
            getattr(entity, action)()


class ConcurrentStrategy(BaseStrategy):
    """ Concurrently process all entity objects. This class leverages the
    concurrent.futures module to manage concurrent thread workers. A pool of threads
    is used, as opposed to processes, because most of the work done is IO bound
    (network access), i.e. the GIL gets released

    This strategy is expected to yield better performance than the sequential strategy,
    particularly as the size of the data set grows.
    """
    def do(self, action, entities):
        super(ConcurrentStrategy, self).do(action, entities)

        with futures.ThreadPoolExecutor(max_workers=len(entities)) as executor:
            # Spawn one thread per entity and perform the action.
            future_to_entity = dict((executor.submit(getattr(entity, action)), entity)
                                    for entity in entities)

            # Join all threads.
            for future in futures.as_completed(future_to_entity):
                entity = future_to_entity[future]
                if future.exception() is not None:
                    logging.error("Entity {0} failed to {1}: {2}"
                                  .format(entity, action, future.exception()))
                else:
                    logging.info("Entity {0} successfully {1}ed"
                                 .format(future.result(), action))


class BatchStrategy(BaseStrategy):
    """ This strategy is dependent on the API provider. When available it makes use of
    the batch mode exposed by the API, i.e. multiple objects can be pushed remotely with
    one API call.
    Example: https://developers.facebook.com/docs/marketing-api/batch-requests
    """
    def do(self, action, entities):
        raise NotImplementedError("Come back later")
