#!/usr/bin/python3
""" FIFOCache module """

from base_caching import BaseCaching

class FIFOCache(BaseCaching):
    """ FIFO cache system """
    def __init__(self):
        """ Initialize the cache """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache using FIFO """
        if key is not None and item is not None:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:

                fistKey = next(iter(self.cache_data))
                delItem = self.cache_data.pop(fistKey)
                print("DISCARD: {}".format(fistKey))

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
