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
    heap.insert(4)
    suite.run_test(heap.isempty(), False, "Test2: isempty")
    
    
    # Test insert
    heap.insert(4)
    heap.insert(8) 
    heap.insert(9)
    heap.insert(4)
    heap.insert(12)
    heap.insert(9)
    heap.insert(11)
    heap.insert(13)

    suite.run_test(heap.check([4, 4, 8, 9, 4, 12, 9, 11, 13]), True, "Test3: insert")

    heap.insert(7)
    heap.insert(10)
    heap.insert(5)

    suite.run_test(heap.check([4, 4, 5, 9, 4, 8, 9, 11, 13, 7, 10, 12]), True, "Test4: insert")

    # Test extract_min
    heap = heap_class()
    heap.insert(4)
    heap.insert(4)
    heap.insert(8) 
    heap.insert(9)
    heap.insert(4)
    heap.insert(12)
    heap.insert(9)
    heap.insert(11)
    heap.insert(13)

    minimum = heap.extract_min()
    suite.run_test(minimum, 4, "Test5: extract_min")
    suite.run_test(heap.check([4, 4, 8, 9, 13, 12, 9, 11]), True, "Test6: extract_min")
    
    suite.report_results()

