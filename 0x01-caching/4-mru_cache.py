#!/usr/bin/python3
"""MRU Module"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class that inherits from BaseCaching and implements
    a Most Recently Used caching system
    """

    def __init__(self):
        """Initialize the cache instance"""
        super().__init__()
        self.order = []  # Keep track of access order

    def put(self, key, item):
        "Store an item in the cache using the MRU strategy"
        if key is None or item is None:
            return
        if (len(self.cache_data) >= self.MAX_ITEMS and
                key not in self.cache_data):
            mru_key = self.order.pop()
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")
        self.cache_data[key] = item
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

    def get(self, key):
        "Retrieve an item from the cache by its key"
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
