#!/usr/bin/python3
"""LRU Module"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class that inherits from BaseCaching and implements
    a Least Recently Used caching system
    """
    def __init__(self):
        """Initialize the cache instance"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        'Store an item in the cache using the LRU strategy'
        if key is None or item is None:
            return
        if (len(self.cache_data) >= self.MAX_ITEMS and
                key not in self.cache_data):
            lru_key = self.order.pop(0)
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")
        self.cache_data[key] = item
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

    def get(self, key):
        'Retrieve an item from the cache by its key'
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
