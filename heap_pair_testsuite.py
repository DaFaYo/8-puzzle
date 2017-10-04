"""
A simple testing suite for Solitaire Mancala
Note that tests are not exhaustive and should be supplemented
http://www.codeskulptor.org/#user34_B88RxBpJcx_0.py
"""

import poc_simpletest

def run_test(heap_class):
    
    suite = poc_simpletest.TestSuite()
    heap = heap_class()
    # Test methods

    # Test isempty
    suite.run_test(heap.isempty(), True, "Test1: isempty")
    heap.insert((9, 4))
    suite.run_test(heap.isempty(), False, "Test2: isempty")
    
    
    # Test insert
    heap.insert((1, 4))
    heap.insert((2, 8))
    heap.insert((3, 9))
    heap.insert((5, 4))
    heap.insert((7, 12))
    heap.insert((4, 9))
    heap.insert((6, 11))
    heap.insert((8, 13))

    suite.run_test(heap.check([(9, 4), (1, 4), (2, 8), (3, 9), (5, 4), (7, 12), (4, 9), (6, 11), (8, 13)]), True, "Test3: insert")

    heap.insert((10, 7))
    heap.insert((11, 10))
    heap.insert((12, 5))

    suite.run_test(heap.check([(9, 4), (1, 4), (12, 5), (3, 9), (5, 4), (2, 8), (4, 9), (6, 11), (8, 13), (10, 7), (11, 10), (7, 12)]), True, "Test4: insert")

    # Test extract_min
    heap = heap_class()
    heap.insert((9, 4))
    heap.insert((1, 4))
    heap.insert((2, 8))
    heap.insert((3, 9))
    heap.insert((5, 4))
    heap.insert((7, 12))
    heap.insert((4, 9))
    heap.insert((6, 11))
    heap.insert((8, 13))

    vertex, minimum = heap.extract_min()
    suite.run_test([vertex, minimum], [9, 4], "Test5: extract_min")
    suite.run_test(heap.check([(1, 4), (5, 4), (2, 8), (3, 9), (8, 13), (7, 12), (4, 9), (6, 11)]), True, "Test6: extract_min")

    # Test delete
    heap = heap_class()
    heap.insert((1, 4))
    heap.insert((2, 7))
    heap.insert((3, 14)) 
    heap.insert((4, 12))
    heap.insert((5, 9))
    heap.insert((6, 17))

    heap.delete(7)
    suite.run_test(heap.check([(1, 4), (2, 7), (3, 14), (4, 12), (5, 9), (6, 17)]), True, "Test7: delete")

    heap.delete(2)
    suite.run_test(heap.check([(1, 4), (5, 9), (3, 14), (4, 12), (6, 17)]), True, "Test8: delete")
    
    suite.report_results()

