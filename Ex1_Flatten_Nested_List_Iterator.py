# ----------------------------------------------------
# Intuition:
# We need to iterate over a nested list of integers and lists, 
# returning integers in a flattened order.


# Brute Force:
# - Flatten the entire nested list upfront by recursively traversing all elements.
# - Store all integers in a list.
# - Iterate over the flattened list using an index.
# - Simple but uses extra space upfront and does all work before iteration.
#
# Optimal (Lazy Stack-Based):
# - Use a stack initialized with the input list reversed.
# - On hasNext(), flatten only as needed:
#   - If the top is an integer, ready to return it.
#   - If the top is a list, pop it and push its contents reversed onto the stack.
# - This processes elements on demand, saving time and space for partial iteration.
# ----------------------------------------------------

# ----------------------------------------------------
# Time Complexity: Amortized O(1) per next()/hasNext() call
# - Each element is pushed and popped from the stack at most once
# - next() is always O(1) in the worst case
# - hasNext() may do more work in one call, but total work is O(N) → Amortized O(1)

# Space Complexity: O(d)
# - d = maximum depth of the nested list structure
# - Stack only stores necessary nodes during iteration
# ----------------------------------------------------

from typing import List

class NestedInteger:
    def isInteger(self) -> bool: ...
    def getInteger(self) -> int: ...
    def getList(self) -> List['NestedInteger']: ...

class NestedIterator:

    def __init__(self, nestedList: List[NestedInteger]):
        self.stack = nestedList[::-1] # start by reversing the outer list

    def next(self) -> int:
        # Ensure hasNext was called and top is an integer
        return self.stack.pop().getInteger()

    def hasNext(self) -> bool:
        while self.stack:
            top = self.stack[-1]
            if top.isInteger():
                return True
            self.stack.pop()
            self.stack.extend(top.getList()[::-1]) # reverse to preserve order
        return False


'''
# ----------------------------------------------------
# Brute Force Approach (Pre-flatten everything)
#
# Time Complexity: O(n) where n is total number of integers in nestedList
# - Flatten entire structure recursively in constructor.
# - next()/hasNext() are O(1).
#
# Space Complexity: O(n) to store flattened list.
# ----------------------------------------------------

class NestedIterator:

    def __init__(self, nestedList: List[NestedInteger]):
        self.flattened = []
        self._flatten(nestedList)
        self.index = 0

    def _flatten(self, nestedList):
        for ni in nestedList:
            if ni.isInteger():
                self.flattened.append(ni.getInteger())
            else:
                self._flatten(ni.getList())

    def next(self) -> int:
        val = self.flattened[self.index]
        self.index += 1
        return val

    def hasNext(self) -> bool:
        return self.index < len(self.flattened)
'''
