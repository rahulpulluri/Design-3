# ----------------------------------------------------
# Intuition:
# The problem asks for a data structure that supports O(1) `get` and `put` operations
# while evicting the Least Recently Used (LRU) item once capacity is exceeded.
#
# 1) Brute Force Approach:
#    Use a list to store [key, value] pairs. On each `get`/`put`, scan linearly.
#    Simple but slow: O(n) time for each operation.
#
# 2) Built-in OrderedDict Approach:
#    Leverage Python’s OrderedDict to maintain order of insertion/use.
#    Move keys to the end on access; evict oldest from the front. Clean and fast (avg O(1)).
#
# 3) Optimal Approach (Doubly Linked List + HashMap):
#    - HashMap: key → node reference for O(1) lookup
#    - Doubly Linked List: for O(1) removal and insertion (tracking LRU/MRU order)
#    This gives strict O(1) performance for both operations.
# ----------------------------------------------------

# ----------------------------------------------------
# Time Complexity: O(1) for both get and put
# - Dictionary allows O(1) key access
# - Doubly linked list handles insertion and removal in O(1)
#
# Space Complexity: O(capacity)
# - Stores up to 'capacity' nodes and entries in the hashmap
# ----------------------------------------------------

class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.dict = {}
        self.capacity = capacity
        self.head = ListNode(-1, -1)  # dummy head
        self.tail = ListNode(-1, -1)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.dict:
            return -1
        node = self.dict[key]
        self._remove(node)
        self._add(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.dict:
            self._remove(self.dict[key])
        node = ListNode(key, value)
        self.dict[key] = node
        self._add(node)

        if len(self.dict) > self.capacity:
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.dict[lru_node.key]

    def _add(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev


# ----------------------------------------------------
# Alternative 1: Built-in OrderedDict
#
# Intuition:
# Python’s OrderedDict maintains insertion order.
# We move accessed elements to the end and pop the least recently used from the front.
#
# Time Complexity: O(1) average for get and put
# Space Complexity: O(capacity)
# ----------------------------------------------------

# from collections import OrderedDict
# class LRUCache:
#     def __init__(self, capacity: int):
#         self.cache = OrderedDict()
#         self.capacity = capacity
#
#     def get(self, key: int) -> int:
#         if key not in self.cache:
#             return -1
#         self.cache.move_to_end(key)
#         return self.cache[key]
#
#     def put(self, key: int, value: int) -> None:
#         if key in self.cache:
#             self.cache.move_to_end(key)
#         self.cache[key] = value
#         if len(self.cache) > self.capacity:
#             self.cache.popitem(last=False)


# ----------------------------------------------------
# Alternative 2: Brute Force with List
#
# Intuition:
# Maintain a list of [key, value] pairs. On get/put, linearly scan and update position.
# Remove the least recently used (first) item on capacity overflow.
#
# Time Complexity:
# - get: O(n) for linear scan
# - put: O(n) in worst case for scan and removal
#
# Space Complexity: O(capacity)
# ----------------------------------------------------

# class LRUCache:
#     def __init__(self, capacity: int):
#         self.cache = []
#         self.capacity = capacity
#
#     def get(self, key: int) -> int:
#         for i in range(len(self.cache)):
#             if self.cache[i][0] == key:
#                 tmp = self.cache.pop(i)
#                 self.cache.append(tmp)
#                 return tmp[1]
#         return -1
#
#     def put(self, key: int, value: int) -> None:
#         for i in range(len(self.cache)):
#             if self.cache[i][0] == key:
#                 tmp = self.cache.pop(i)
#                 tmp[1] = value
#                 self.cache.append(tmp)
#                 return
#         if len(self.cache) == self.capacity:
#             self.cache.pop(0)
#         self.cache.append([key, value])



if __name__ == "__main__":
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(lru.get(1))  # Output: 1
    lru.put(3, 3)      # Evicts key 2
    print(lru.get(2))  # Output: -1 (not found)
    lru.put(4, 4)      # Evicts key 1
    print(lru.get(1))  # Output: -1
    print(lru.get(3))  # Output: 3
    print(lru.get(4))  # Output: 4
