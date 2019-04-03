import time
import collections
import logging
from MySimpleLRUCache_KaranMaheshwari.helper import is_signed_32_bit_integer_format

logging.basicConfig(filename='./app.log', filemode='w', level=logging.DEBUG,
					format='%(name)s - %(levelname)s - %(message)s')


class LRUCache:
	"""This is a simple implementation of LRU Cache using OrderedDictionary.

	Attributes:
		__max_capacity: An integer representing the maximum capacity of the cache.
		__cache: An ordered dictionary that holds inserted integers as keys and their last used timestamp as respective values.
	"""

	def __init__(self, max_capacity=5):
		"""
		Constructs a new LRUCache object.

		:param max_capacity: The max capacity of the cache
		"""
		if isinstance(max_capacity, float) or isinstance(max_capacity, str) \
				or max_capacity is None or max_capacity == 0 or max_capacity < 0:
			logging.warning("Wrong value specified for maximum capacity. Setting default value (5).")
			self.__max_capacity = 5
		else:
			self.__max_capacity = max_capacity
		self.__cache = collections.OrderedDict()
		logging.info("Created new LRUCache object.")

	def get(self, key):
		"""This method checks if the given *key* exists in the cache.

		:param key: The element whose existence in the cache needs to be checked.
		:return: True if key exists in the cache else False
		"""
		try:
			self.__cache.pop(key)
			self.__cache[key] = time.time()
			logging.info(str(key) + " exists in cache. Updated last used time.")
			return True
		except KeyError:
			logging.error(str(key) + " does not exist in cache.")
			return False

	def put(self, key):
		"""This method inserts the *key* into the cache.
		If the key already exists, it will update its timestamp.
		If the key does not exist in the cache, it will insert it in
		the cache while fulfilling the maximum capacity constraint.

		:param key: The element that needs to be inserted.
		:return: Nothing.
		"""
		if is_signed_32_bit_integer_format(key):
			try:
				self.__cache.pop(key)
				logging.info(str(key) + " exists in cache. Updated last used time.")
			except KeyError:
				logging.info(str(key) + " does not exist in cache.")
				if len(self.__cache) >= self.__max_capacity:
					element_removed = self.__cache.popitem(last=False)
					logging.warning("Max capacity reached. Removed " + str(element_removed[0]) + ".")
				logging.info("Inserted " + str(key) + ".")
			self.__cache[key] = time.time()
		else:
			logging.error("Cache accepts only signed 32 bit integers.")

	def get_max_capacity(self):
		"""This method can be used to check the maximum capacity of the cache.

		:return: The maximum number of elements the cache can hold.
		"""
		return self.__max_capacity

	def get_current_capacity(self):
		"""This method can be used to check how many elements currently reside in the cache.

		:return: The number of elements currently in the cache.
		"""
		return len(self.__cache)

	def get_elements(self):
		"""Return a list of the elements currently in cache ordered from least recently used to most recently used.

		:return: The elements currently in the cache (ordering: least recently used to most recently used).
		"""
		return list(self.__cache.keys())

	def clear_cache(self):
		"""Used to empty the cache.

		:return: Nothing.
		"""
		self.__cache.clear()
