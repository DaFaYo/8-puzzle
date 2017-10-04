class Heap:
    """
    Heap implementation as an array of tuples tuple(v, d)
    where v is the vertex and d is the shortest path value - dist[i]
    """

    def __init__(self):

        # heap is initialized as an empty array
        self._heap = []
        self._num_items = 0

    def isempty(self):
        """
        returns a boolean True if the heap is empty
        """
        return len(self._heap) == 0
            
    def insert(self, item):
        """
        insert integer into the heap and restores order
        """

        # insert new item and update the number of items
        self._heap.append(item)
        self._num_items += 1    
        k = self._num_items
        # bubble-up procedure for the new item
        # to restore heap
        while k > 1 and self.isgreater(k/2, k):       
            self.exch(k, k/2)
            k = k/2


    def extract_min(self):
        if not self._heap:
            raise Exception("The heap is empty")
        self.exch(1, self._num_items)
        minimum = self._heap.pop()
        self._num_items -= 1
        
        # bubble-down procedure for the new item
        # to restore heap
        N = self._num_items
        k = 1
        while k <= N:
            j = 2 * k
            if j < N and self.isgreater(j, j + 1):
                j += 1
            if j > N or not self.isgreater(k, j):
                break
            self.exch(k, j)
            k = j
            
        return minimum
        
    def exch(self, i, j):
        """
        exchanges two items in the list by a swap
        """
        assert (i > 0 and i <= self._num_items)
        assert (j > 0 and j <= self._num_items)

        swap = self._heap[i - 1]
        self._heap[i - 1] = self._heap[j - 1]
        self._heap[j - 1] = swap       

    def isgreater(self, i, j):
        """
        checks which item is greater in the heap
        """
        return (self._heap[i - 1] > self._heap[j - 1])

    def check(self, array):
        """
        Check that the heap has the given array structure,
        strictly for debugging purposes
        """

        return self._heap == array
          
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return str(self._heap)

# tests for the heap
import heap_testsuite
heap_testsuite.run_test(Heap)




