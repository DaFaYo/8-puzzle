
### 8-puzzle game.

For a refresher visit  http://www.puzzlopia.com/puzzles/puzzle-8/play to play the game.

What this program does is creating an **agent** that solves the 8-puzzle with one of three search algorithms:


[bfs (Breadth-First Search)](https://en.wikipedia.org/wiki/Breadth-first_search)

[dfs (Depth-First Search)](https://en.wikipedia.org/wiki/Depth-first_search)

[ast (A-Star Search)](https://en.wikipedia.org/wiki/A*_search_algorithm)


Its an implementation of the following assignment: [ColumbiaX-AI-project2](https://courses.edx.org/courses/course-v1:ColumbiaX+CSMM.101x+2T2017_2/courseware/)

**Requirements:** Python 2. 

You can use for example the following commands from the **command line**:

  **python driver.py bfs 0,8,7,6,5,4,3,2,1**

  **python driver.py dfs 0,8,7,6,5,4,3,2,1**

  **python driver.py ast 0,8,7,6,5,4,3,2,1**



When executed, the program will create / write to a file called output.txt, containing the following statistics:

**path_to_goal:** the sequence of moves taken to reach the goal
**cost_of_path:** the number of moves taken to reach the goal
**nodes_expanded:** the number of nodes that have been expanded
**search_depth:** the depth within the search tree when the goal node is found
**max_search_depth:**  the maximum depth of the search tree in the lifetime of the algorithm
**running_time:** the total running time of the search instance, reported in seconds
**max_ram_usage:** the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes


U can use the **steps** in **path_to_goal** output to solve the 8-puzzle.

where an arbitrary choice must be made, we always visit child nodes in the "UDLR" order; that is,
 [‘Up’, ‘Down’, ‘Left’, ‘Right’] in that exact order. 
