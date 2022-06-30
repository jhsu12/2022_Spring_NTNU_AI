from queue import LifoQueue
import timeit, copy
import numpy as np


### NODE def

class Node:
  # Initialization of Node
  def __init__(self, state, parent=None, depth=0, move=""):
    self.state = state
    self.parent = parent
    self.move = move
    self.depth = depth
# Find the index of space

### FUNCTIONS
    
def find_blank(node):
  for i in range(len(node.state)):
    for j in range(len(node.state[0])):
      if node.state[i][j] == 0:
        return i, j

def get_neighbors(node):
  children=[]
  r, c = len(node.state), len(node.state[0])
  
  # find blank index
  x,y= find_blank(node)

  # left
  if y-1 >= 0:
    new_state = copy.deepcopy(node.state)
    new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
    children.append(Node(new_state, node, node.depth+1, move=f"{new_state[x][y]}R"))
    
  # right
  if y+1 <= c-1:
    new_state = copy.deepcopy(node.state)
    new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
    children.append(Node(new_state, node, node.depth+1, move=f"{new_state[x][y]}L"))

  # up
  if x-1 >= 0:
    new_state = copy.deepcopy(node.state)
    new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
    children.append(Node(new_state, node, node.depth+1, move=f"{new_state[x][y]}D"))

  # down
  if x+1 <= r-1:
    new_state = copy.deepcopy(node.state)
    new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
    children.append(Node(new_state, node, node.depth+1, move=f"{new_state[x][y]}U"))
  
  return children

def get_path(goal_node):
  path=[]
  while goal_node.parent !=None:
  
    # store the step reversely
    path.insert(0,goal_node.move)
    goal_node=goal_node.parent
  return path

# Deep limited search
def dls(start_state,goal_state, d):
  start = timeit.default_timer()
  root = Node(start_state,depth=0,move='Start')
  frontier = LifoQueue()
  frontier.put(root)
  frontier_set =set()
  frontier_set.add(root)
  visited = set()
  
  while not frontier.empty():
    node = frontier.get()
    frontier_set.remove(node)
    
    visited.add(node)
    
    # find goal
    if np.array_equal(node.state,goal_state):
      stop = timeit.default_timer()
      return get_path(node),node.depth,(stop-start)
      
    # if current node's depth is not equal to d, then expand it
    if node.depth != d:
      # expand node
      for n in get_neighbors(node):
       
        if n not in visited and n not in frontier_set:
          frontier.put(n,n.depth)
          frontier_set.add(n)
    
  return False
  




# Get numbers of inversion and row index of blank
def get_ni_rob(start_state, size):
  ni = 0
  rob = 0
  for i in range(0, size):
    if start_state[i] == 0:
      rob = i
      continue;
    for j in range(i + 1, size):
      if start_state[j] == 0:
        continue;
      if start_state[i] > start_state[j]:
          ni += 1
  return ni, rob
def issolvable(start_state, r, c):

  # numbers of inversion, row index of blank
  ni, rob= get_ni_rob(start_state, r*c)
  rob = int(rob/r)
  
  if(c%2 != 0 and ni%2==0):
    return True
  elif(r%2 == 0 and c%2 == 0 and (ni+rob)%2 == 0):
    return True
  elif(r%2 != 0 and c%2 == 0 and (ni+rob)%2 != 0):
    return True

  return False 



### MAIN
  
f = open("input1.txt", "r")
# Read row, column
r, c = f.readline().split()
r = int(r)
c = int(c)

# Read puzzle
start_state = []
goal_state = []

f = f.read().splitlines()
check = []
for d in f:
  row = []
  # append data to row
  for j in d.split():
    row.append(int(j))
    check.append(int(j))
  # append row to state
  start_state.append(row)

# Generate goal state
init = 1
for i in range(r):
  row = []
  for j in range(c):
    row.append(init)
    init+=1
  goal_state.append(row)
goal_state[r-1][c-1] = 0

# Opening a file
output_file = open('output.txt', 'w')

# Check whether the puzzle is solvable
if(not issolvable(check, r, c)):
  #print("no solution")
  output_file.write("no solution")
else:
  # iterative deepening search, maximum 50 steps
  for i in range(50):
    
    result = dls(start_state, goal_state, i)
    if not result:
      continue
    L = [f"Total run time = {result[2]} seconds.\n", f"An optimal solution has {result[1]} moves.\n"]
  
    output_file.writelines(L)

    #print(f"Total run time = {result[2]} seconds.")
    #print(f"An optimal solution has {result[1]} moves.")
    for m in result[0]:
      #print(m, end=" ")
      output_file.write(f"{m} ")
    break
    
# Closing file
output_file.close()