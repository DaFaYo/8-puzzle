class Heap:
    """
    Heap implementation as an array of tuples tuple(v, d)
    where v is the vertex and d is the shortest path value - dist[i]
    """

    def __init__(self):

        # heap is initialized as an empty array
        self._heap = []
        self._vertices = []
        self._lookup_index = {}
        self._num_weights = 0

    def isempty(self):
        """
        returns a boolean True if the heap is empty
        """
        return len(self._heap) == 0
            
    def insert(self, pair):
        """
        insert pair (vertex, weight) into the heap and restores the order
        where vertex is a vertex in the graph and weight is its distance.
        The pair is a tuple.
        """
        
        # insert new vertex and weight
        vertex = pair[0]
        weight = pair[1]

        self._vertices.append(vertex)
        self._heap.append(weight)
        self._num_weights += 1
        # update lookup
        self._lookup_index[vertex] = self._num_weights        
        
        k = self._num_weights
        # bubble-up procedure for the new weight
        # to restore heap
        while k > 1 and self.isgreater(k/2, k):       
            self.exch(k, k/2)
            k = k/2

    def contains(self, vertex):
        """
        checks if vertex is contained in dictionary lookup
        """
        return vertex in self._lookup_index

    def delete(self, vertex):
        """
        deletes an arbitrary vertex from the heap if it is in the heap
        """
        key = 0
        if self.contains(vertex):
            index = self._lookup_index[vertex]

            # exchange the element with the last and remove it
            self.exch(index, self._num_weights)
            key    = self._heap.pop()
            vertex = self._vertices.pop()

            # delete from lookup and update number of weights
            del self._lookup_index[vertex]       
            self._num_weights -= 1

            # bubble-down procedure for the new weight
            # to restore heap
            N = self._num_weights
            k = index
            while k <= N:
                j = 2 * k
                if j < N and self.isgreater(j, j + 1):
                    j += 1
                if j > N or not self.isgreater(k, j):
                    break
                self.exch(k, j)
                k = j

        return key       
        
    def extract_min(self):
        """
        deletes the vertex with the minimum weight in the heap.
        Returns the vertex with its minum weight
        """
        if not self._heap:
            raise Exception("The heap is empty")
        
        self.exch(1, self._num_weights)
        minimum = self._heap.pop()
        vertex = self._vertices.pop()

        # delete from lookup
        del self._lookup_index[vertex]       
        self._num_weights -= 1
        # bubble-down procedure for the new weight
        # to restore heap
        N = self._num_weights
        k = 1
        while k <= N:
            j = 2 * k
            if j < N and self.isgreater(j, j + 1):
                j += 1
            if j > N or not self.isgreater(k, j):
                break
            self.exch(k, j)
            k = j
            
        return vertex, minimum
        
    def exch(self, i, j):
        """
        exchanges two weights in the list by a swap i, j are indices
        """
        assert (i > 0 and i <= self._num_weights)
        assert (j > 0 and j <= self._num_weights)

        # update the lookup
        self._lookup_index[self._vertices[i - 1]] = j
        self._lookup_index[self._vertices[j - 1]] = i
        
        # the heap
        swap = self._heap[i - 1]
        self._heap[i - 1] = self._heap[j - 1]
        self._heap[j - 1] = swap

        # the vertex
        swap = self._vertices[i - 1]
        self._vertices[i - 1] = self._vertices[j - 1]
        self._vertices[j - 1] = swap     
        
    def isgreater(self, i, j):
        """
        checks which weight is greater in the heap
        """
        return (self._heap[i - 1] > self._heap[j - 1])

    def check(self, tuples):
        """
        Check that the heap has the given array structure,
        strictly for debugging purposes
        """
        check = True
        temp = zip(self._vertices, self._heap)
        for indx in range(len(tuples)):
            if tuples[indx][0] != temp[indx][0] or tuples[indx][1] != temp[indx][1]:
                check = False
                break

        return check
          
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(zip(self._vertices, self._heap))

#tests for the heap
#import heap_pair_testsuite
#heap_pair_testsuite.run_test(Heap)



