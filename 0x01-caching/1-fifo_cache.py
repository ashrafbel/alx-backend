#!/usr/bin/env python3
'''FIFO caching'''
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    def __init__(self):
        """Initialize the FIFO cache."""
        super().__init__()

    def put(self, key, item):
        """Assign an item to the cache using the given key."""
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            fistKey = next(iter(self.cache_data))
            print(f"DISCARD: {fistKey}")
            del self.cache_data[fistKey]

    def get(self, key):
        """Retrieve the value associated with the key in the cache."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
