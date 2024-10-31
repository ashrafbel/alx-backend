#!/usr/bin/python3
'Module for LIFOCache'

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    "LIFOCache class that inherits from BaseCaching"

    def __init__(self):
        """ Initialize the cache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        "Store an item in the cache using the LIFO strategy"
        if key is None or item is None:
            return
        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):
            last = self.order.pop()
            del self.cache_data[last]
            print(f"DISCARD: {last}")
        self.cache_data[key] = item
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
