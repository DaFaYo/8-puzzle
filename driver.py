# -*- coding: utf-8 -*-
import sys
import math
import time
import resource
from collections import deque

##
## Name: Daniël Faruk Younis
## Date: 01/10/2017 
##
##
## This program solves the 8-puzzle using:
##
##  breadth-first search algorithm   (bfs)
##  depth-first search algorithm     (dfs)
##  A* algorithm                     (ast)
##
##  8-puzzles:
##
##     start            goal
##  
##    6  1  8         0  1  2
##    4  0  2         3  4  5
##    7  3  5         6  7  8
##
##
## Use: on the command line call the driver with a method and a board
##
## e.g.       > python2 driver.py ast 6,1,8,4,0,2,7,3,5
##
## This creates an output.txt text file which contains a path from start to goal board.
##
## e.g. [ Down, Right, Up, Up, Left, Down, Right, Down, Left, Up, Left, Up,
##                              Right, Right, Down, Down, Left, Left, Up, Up ]
##
## I made this program to complete project: Week 2 Project: Search Algorithms
## for the course: ColumbiaX: CSMM.101x Artificial Intelligence (AI)  (EDX)
##




###############################################################################
# MANHATTAN DISTANCE FUNCTION
###############################################################################

def manhattan_dist(start, goal, n):
    """
    Computes the manhattan distance between start and goal
    of 8-puzzle boards assumption: start and goal lists are of same length
    """
    dist = 0
    for i in range(len(goal)):
       if start[i] != 0: 
           dist += abs(start[i] % n - goal[i] % n)      
           dist += abs(start[i] /n  - goal[i]/ n) 

    return dist



###############################################################################
# HEAP CLASS
###############################################################################

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
     



###############################################################################
# STACK CLASS
###############################################################################

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)




###############################################################################
# BOARD CLASS
###############################################################################

class Board():
    """
    Board handles the visualisations of the state
    
    """
    def __init__(self, state):

        self._state = state
        self._N = len(self._state._board)
        self._M = int(math.sqrt(self._N))
        
    def show(self):

        myString = []
        for i in xrange(1, self._N + 1):
            myString.append(str(self._state._board[i - 1]))
            if i % self._M != 0:
                myString.append("   ")
            else:
                myString.append("\n")
 
        return ''.join(myString)

    def showMoves(self):
        jump = 2 * '\n'
        moves = []
        n = 0
        while self._state._parent:
 
            if n % 3 == 0 and self._state._parent:
                moves.append(jump)

            moves.append(self.show())
            self._state = self._state._parent
            #moves.append('   –––>   ')
            n += 1

        return ''.join(reversed(moves))



   
###############################################################################
# STATE CLASS
###############################################################################

class State():
    """
    State that stores the board, its parent as a state and the move(direction) it took to get to this state
    """
    def __init__(self, board=None, spaceIndex=None, parent=None, move=None, depth = 0):

        # board is an numpy array
        self._board = board
        self._i = spaceIndex
        self._parent = parent
        self._move = move       
        self._N = len(board)
        self._M = int(math.sqrt(self._N))
        self._depth = depth                  # used to return the maximum depth of the search tree in solver

    def __hash__(self):
        return hash(tuple(self._board))

    def __eq__(self, other):
        return (self._board) == (other._board)

    def __str__(self):
        return ','.join(str(e) for e in self._board)
    

    def neighbors(self):
        """
        (state) -> List(state)
        returns a list of states
        """
        neighbors = []
        for move in [0, 1, 2, 3]:

            if move == 0 and (self._i >= self._M):
                newBoard = self._board[:]
                newBoard[self._i - self._M] = 0
                newBoard[self._i] = self._board[self._i - self._M]
                neighbors.append(State(newBoard, self._i - self._M, self, move, self._depth + 1))
    
            if move == 1 and (self._i < self._N - self._M):
                newBoard = self._board[:]
                newBoard[self._i + self._M] = 0
                newBoard[self._i] = self._board[self._i + self._M]
                neighbors.append(State(newBoard, self._i + self._M, self, move, self._depth +  1))
                
            if move == 2 and (self._i % self._M != 0):                
                newBoard = self._board[:]
                newBoard[self._i - 1] = 0
                newBoard[self._i] = self._board[self._i - 1]
                neighbors.append(State(newBoard, self._i - 1, self, move, self._depth + 1))

            if move == 3 and (self._i % self._M != self._M - 1):
                newBoard = self._board[:]
                newBoard[self._i + 1] = 0
                newBoard[self._i] = self._board[self._i + 1]
                neighbors.append(State(newBoard, self._i + 1, self, move, self._depth + 1))
          
        return neighbors
        
        
 

###############################################################################
# SOLVER CLASS
###############################################################################


class Solver:
    """
    works with the state datastructure takes a method: bfs, dfs or A* search
    and a board: e.g.: 3,1,2,0,4,5,6,7,8.
    It wants to solve the 8-puzzle so the goalTest should be: 0,1,2,3,4,5,6,7,8
    """
    def __init__(self, method, board):

        self._directions = {0: 'Up', 1: 'Down', 2: 'Left', 3: 'Right'}
        self._board = map(int, board.split(","))
        self._N = len(self._board)
        self._method = method
        self._result = 'FAILURE'
        self._finalState = None
        self._spaceIndex = self.computeSpaceIndex()

        # Output Statistics
        self._path_to_goal = []       # the sequence of moves taken to reach the goal
        self._cost_of_path = 0        # the number of moves taken to reach the goal
        self._nodes_expanded = -1      # the number of nodes that have been expanded
        self._search_depth = 0        # the depth within the search tree when the goal node is found
        self._max_search_depth = 0    # the maximum depth of the search tree in the lifetime of the algorithm
        self._running_time = 0        # the total running time of the search instance, reported in seconds
        self._max_ram_usage = 0       # the maximum RAM usage in the lifetime of the process as measured by the
                                      # ru_maxrss attribute in the resource module, reported in megabytes

 
    def computeSpaceIndex(self):
        for i in xrange(self._N):
            if self._board[i] == 0:
                return i


    def goalTest(self, goal):
        """
        calls one of the three search algorithms and computes some statistics
        """
        goal = map(int, goal.split(","))
        start = time.time() # start clock
        
        if self._method == 'bfs':
            self._result = self.bfs(goal) # breadth-first search
        if self._method == 'dfs':
            self._result = self.dfs(goal) # depth-first search
        if self._method == 'ast':
             self._result = self.ast(goal) # A*-search
            
        end = time.time() # end clock
        self._running_time = end - start
        # compute RAM usage in Megabytes
        self._max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 10e6 
        

    def getFinalState(self):
        return  self._finalState


    def path(self, state):
        while state._parent:
            self._cost_of_path += 1
            self._search_depth += 1
            self._path_to_goal.append(self._directions[state._move])
            state = state._parent

        return reversed(self._path_to_goal)    


    def get_path(self):

        """
        returns the path from start to goal
        """
        if self._result == 'SUCCESS':
            return self.path(self._finalState)


    def get_output(self, path):
        """
        returns the output statistics from __init__.
        """
        if not path:
            path = []

        return 'path_to_goal: {0} \n' \
              'cost_of_path: {1}\n' \
              'nodes_expanded: {2}\n' \
              'search_depth: {3}\n' \
              'max_search_depth: {4}\n' \
              'running_time: {5:.{digits}f}\n'\
              'max_ram_usage: {6:.{digits}f}'.format([str(e) for e in path], self._cost_of_path,
                                            self._nodes_expanded, self._search_depth,
                                            self._max_search_depth, self._running_time, self._max_ram_usage, digits=8)

 
    def dfs(self, goal):
        """
        returns SUCCESS or FAILURE. Uses depth-first-search algorithm to solve goal.
        For example: goal = 0,1,2,3,4,5,6,7,8.
        
        """

        # create the initialState
        initialState = State(list(self._board), self._spaceIndex)           
        frontier = Stack()
        inFront = set()
        explored = set()
        frontier.push(initialState)
        inFront.add(initialState)

        while not frontier.isEmpty():   # while frontier is not empty
            
            state = frontier.pop()   # LIFO           
            inFront.remove(state)
            explored.add(state)
            self._nodes_expanded += 1 
 
            if state._board == goal:
                self._result = 'SUCCESS'
                self._finalState = state
                return self._result

            for neighbor in reversed(state.neighbors()):
                if  neighbor not in inFront and neighbor not in explored:
                    frontier.push(neighbor)
                    inFront.add(neighbor)

                    if neighbor._depth > self._max_search_depth:
                        self._max_search_depth = neighbor._depth
 
        return self._result

    

    def bfs(self, goal):
        """
        returns SUCCESS or FAILURE. Uses breadth-first-search algorithm to solve goal.
        For example: goal = 0,1,2,3,4,5,6,7,8.
        
        """

        # create the initialState
        initialState = State(self._board, self._spaceIndex)           
        frontier = deque()
        inFront = set()
        explored = set()
        frontier.append(initialState)
        inFront.add(initialState)

        while frontier:   # while frontier is not empty
            state = frontier.popleft()   # FIFO                          
            inFront.remove(state)
            explored.add(state)
            self._nodes_expanded += 1

            if state._board == goal:
                self._result = 'SUCCESS'
                self._finalState = state
                return self._result

            for neighbor in state.neighbors():                
                if  neighbor not in inFront and neighbor not in explored:
                     frontier.append(neighbor)
                     inFront.add(neighbor)

                     if neighbor._depth > self._max_search_depth:
                          self._max_search_depth = neighbor._depth

        return self._result



    def ast(self, goal):
        """
        returns SUCCESS or FAILURE. Uses A*-search algorithm to solve goal.
        The only difference with uniform cost search, we use a cost function: f(n) = h(n) + g(n)
        For example: goal = 0,1,2,3,4,5,6,7,8.        
        """

        # create the initialState
        initialState = State(self._board, self._spaceIndex)
        frontier = Heap()
        gn = {}
        gn[initialState] = 0               
        frontier.insert((initialState, 0))       
        explored = set()

        while not frontier.isempty():   # while frontier is not empty

            state, d = frontier.extract_min()   # HEAP Extract state with minimum cost

            if not frontier.isempty():
                nextState, d1 = frontier.extract_min()   # HEAP Extract state with minimum cost
                if d == d1 and state._move > nextState._move:
                    frontier.insert((state, d))
                    state = nextState
                else:
                    frontier.insert((nextState, d1))

            explored.add(state)
            self._nodes_expanded += 1
           
            if state._board == goal:
                self._result = 'SUCCESS'
                self._finalState = state
                return self._result

            for neighbor in reversed(state.neighbors()):                
                if not frontier.contains(neighbor) and neighbor not in explored:
                   
                    gn[neighbor] = gn[state] + 1
                    fn = gn[neighbor] + manhattan_dist(neighbor._board, goal, 3)                                           
                    frontier.insert((neighbor, fn))
                    
                    if neighbor._depth > self._max_search_depth:
                        self._max_search_depth = neighbor._depth

                elif frontier.contains(neighbor):
                    frontier.delete(neighbor)                            

        return self._result
                


def main():



    # read in arguments
    method = sys.argv[1]
    board  = sys.argv[2]
    goal = '0,1,2,3,4,5,6,7,8'
    
    solver = Solver(method, board)    
    solver.goalTest(goal)
    finalState = solver.getFinalState()
    path = solver.get_path()
    output = solver.get_output(path)

    f = open('output.txt', 'w')
    f.write(output)  # python will convert \n to os.linesep
    f.close() 

        
#    import driver_testsuite
#    driver_testsuite.run_test(Solver, manhattan_dist)
 
    

if __name__ == '__main__':
    main()


