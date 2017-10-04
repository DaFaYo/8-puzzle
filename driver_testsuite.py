"""
A simple testing suite for 8-puzzle, 15-puzzle, 24-puzzle, etc.
"""

import poc_simpletest
import time

total_time = 0.0


def timeTest(testName, timeElapsed):
    global total_time

    total_time += timeElapsed        
    return "%s. Time elapsed: %.3f s." % (testName, timeElapsed)


def run_test(solver_class, manhattan_func):


    # -----------------------------------------------------------
    # test manhattan distance function with 8-puzzle 
    # -----------------------------------------------------------


    suite = poc_simpletest.TestSuite()
    
    function = 'manhattan distance'
    start = '7,2,4,5,0,6,8,3,1'
    goal = '0,1,2,3,4,5,6,7,8'
    print 'Goal:', goal
    testName = "Test #1: function: %s, start: %s" % (function, start)
    start = map(int, start.split(","))
    goal = map(int, goal.split(","))
    dist = manhattan_func(start, goal, 3)
    suite.run_test(dist, 18, testName)
    print testName
 
    start = '1,2,5,3,4,0,6,7,8'
    testName = "Test #2: function: %s, start: %s" % (function, start)
    start = map(int, start.split(","))
    dist = manhattan_func(start, goal, 3)
    suite.run_test(dist, 3, testName)
    print testName

    start = '3,1,2,0,4,5,6,7,8'
    testName = "Test #3: function: %s, start: %s" % (function, start)
    start = map(int, start.split(","))
    dist = manhattan_func(start, goal, 3)
    suite.run_test(dist, 1, testName)
    print testName

    start = '8,6,4,2,1,3,5,7,0'
    testName = "Test #4: function: %s, start: %s" % (function, start)
    start = map(int, start.split(","))
    dist = manhattan_func(start, goal, 3)
    suite.run_test(dist, 18, testName)
    print testName


    start = '8,4,0,3,7,1,6,2,5'
    testName = "Test #5: function: %s, start: %s" % (function, start)
    start = map(int, start.split(","))
    dist = manhattan_func(start, goal, 3)
    suite.run_test(dist, 12, testName)
    print testName

    ##############
    # TEST SOLVER
    ##############

    #solve the 8-puzzle
    goal = '0,1,2,3,4,5,6,7,8'

    # -------------------------------------------------------------
    # test solver with 8-puzzle with breadth-first-search algorithm
    # -------------------------------------------------------------

    board = '3,1,2,0,4,5,6,7,8'
    testName = "Test #6 t/m #8: sanity checks, board: %s" % (board)
    print testName

    solver = solver_class('bfs', board)
    solver.goalTest(goal)
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Up }', testName)
    solver = solver_class('dfs', board)
    solver.goalTest(goal)
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Up }', testName)
    solver = solver_class('ast', board)
    solver.goalTest(goal)
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Up }', testName)


    method = 'bfs'
    board = '1,2,5,3,4,0,6,7,8'
    testName = "Test #9: method: %s, board: %s" % (method, board)

    # time the solver
    start = time.time()
    solver = solver_class(method, board)
    solver.goalTest(goal)
    end = time.time()
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Up, Left, Left }', testName)
    print timeTest(testName, (end - start))
    

    method = 'ast'
    board = '1,2,5,3,4,0,6,7,8'
    testName = "Test #10: method: %s, board: %s" % (method, board)

    # time the solver
    start = time.time()
    solver = solver_class(method, board)
    solver.goalTest(goal)
    end = time.time()
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Up, Left, Left }', testName)
    print timeTest(testName, (end - start))
    
     
    board = '6,3,4,7,1,8,2,0,5'
    testName = "Test #11: method: %s, board: %s" % (method, board)

    start = time.time()
    solver = solver_class(method, board)
    solver.goalTest(goal)
    end = time.time()
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Left, Up, Up, Right, Down, Down, Right, Up, ' \
                    'Left, Down, Left, Up, Up, Right, Right, Down, Left, Up, Left }', testName)
    print timeTest(testName, (end - start))

 
    board = '4,5,6,1,2,0,8,7,3'
    testName = "Test #12: method: %s, board: %s" % (method, board)
    
    start = time.time()
    solver = solver_class(method, board)
    solver.goalTest(goal)
    end = time.time()
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Up, Left, Down, Down, Left, Up, Right, Right, ' \
                   'Down, Left, Up, Left, Down, Right, Up, Right, Up, Left, Left, Down, Right, Up, Left }', testName)
    print timeTest(testName, (end - start))


    # -----------------------------------------------------------
    # test solver with 8-puzzle with depth-first-search algorithm
    # -----------------------------------------------------------
    
    method = 'dfs'
    board = '1,2,5,3,4,0,6,7,8'
    testName = "Test #13: method: %s, board: %s" % (method, board)

    # time the solver
    start = time.time()
    solver = solver_class(method, board)
    solver.goalTest(goal)
    end = time.time()
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Up, Left, Left }', testName)
    print timeTest(testName, (end - start))


    
    # -----------------------------------------------------------
    # test solver with 8-puzzle with A* algorithm
    # -----------------------------------------------------------
    
    method = 'ast'
    board = '6,1,8,4,0,2,7,3,5'
    testName = "Test #14: method: %s, board: %s" % (method, board)

    # time the solver
    start = time.time()
    solver = solver_class(method, board)
    solver.goalTest(goal)
    end = time.time()
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Down, Right, Up, Up, Left, Down, Right, Down, ' \
                    'Left, Up, Left, Up, Right, Right, Down, Down, Left, Left, Up, Up }', testName)
    print timeTest(testName, (end - start))


    
    # -----------------------------------------------------------
    # test solver with 8-puzzle with A* algorithm
    # -----------------------------------------------------------
    
    method = 'ast'
    board = '6,3,4,7,1,8,2,0,5'
    testName = "Test #15: method: %s, board: %s" % (method, board)

    # time the solver
    start = time.time()
    solver = solver_class(method, board)
    solver.goalTest(goal)
    end = time.time()
    path = solver.get_path()
    suite.run_test('{ %s }' % (', '.join(str(e) for e in path)), '{ Left, Up, Up, Right, Down, Down, Right, Up, ' \
                    'Left, Down, Left, Up, Up, Right, Right, Down, Left, Up, Left }', testName)
    
    print timeTest(testName, (end - start))

    print
    print "Total time: %.3f seconds." % (total_time)    
    
    suite.report_results()

