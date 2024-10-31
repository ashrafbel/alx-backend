#!/usr/bin/python3
""" BaseCaching module
"""

class BaseCaching():
    """ BaseCaching defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """
    MAX_ITEMS = 4

    def __init__(self):
        """ Initiliaze
        """
        self.cache_data = {}

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print("{}: {}".format(key, self.cache_data.get(key)))

    def put(self, key, item):
        """ Add an item in the cache
        """
        raise NotImplementedError("put must be implemented in your cache class")

    def get(self, key):
        """ Get an item by key
        """
        raise NotImplementedError("get must be implemented in your cache class")
    
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    "BasicCache class functions as an unlimited cache"

    
    def put(self, key, item):
        "Stores an item in the cache using the provided key."
        if key is not None and item is not None:
            self.cache_data[key] = item
    
    def get(self, key):
        return self.cache_data.get(key, None)
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

        # Check if the number of items exceeds MAX_ITEMS
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Discard the first item (FIFO)
            first_key = next(iter(self.cache_data))  # Get the first key
            print(f"DISCARD: {first_key}")
            del self.cache_data[first_key]  # Remove the first item

    def get(self, key):
        """Retrieve the value associated with the key in the cache."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]

    
my_cache = BasicCache()
my_cache.print_cache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.print_cache()
print(my_cache.get("A"))
print(my_cache.get("B"))
print(my_cache.get("C"))
print(my_cache.get("D"))
my_cache.print_cache()
# my_cache.put("D", "School")
# my_cache.put("E", "Battery")
# my_cache.put("A", "Street")
# my_cache.print_cache()
# print(my_cache.get("A"))
