import timeit, copy
import numpy as np


### NODE def
class Node:

  # Initialization of Node
  def __init__(self, state, h, parent=None, depth=0, move=""):
    self.state = state
    self.parent = parent
    self.move = move
    
    self.depth = depth
    self.h = h
    self.f = h + depth

### FUNCTIONS
    
# Find the index of target
def find_target(state, target, r, c):
  for i in range(r):
    for j in range(c):
      if state[i][j] == target:
        return i, j

def get_neighbors(node, goal_state):
  
  children=[]
  r, c = len(node.state), len(node.state[0])
  
  # find blank index
  x,y = find_target(node.state, 0, r, c)

  # left
  if y-1>=0:
    new_state = copy.deepcopy(node.state)
    new_state[x][y], new_state[x][y-1] = new_state[x][y-1],new_state[x][y]
    h = manhattan(new_state, goal_state, r, c)
    children.append(Node(new_state, h, node, node.depth + 1, move=f"{new_state[x][y]}R"))
    
  # right
  if y+1<=c-1:
    new_state=copy.deepcopy(node.state)
    new_state[x][y],new_state[x][y+1]=new_state[x][y+1],new_state[x][y]
    h = manhattan(new_state, goal_state, r, c)
    children.append(Node(new_state, h, node, node.depth+1, move=f"{new_state[x][y]}L"))

  # up
  if x-1>=0:
    new_state=copy.deepcopy(node.state)
    new_state[x][y],new_state[x-1][y]=new_state[x-1][y],new_state[x][y]
    h = manhattan(new_state, goal_state, r, c)
    children.append(Node(new_state, h, node, node.depth+1, move=f"{new_state[x][y]}D"))

  # down
  if x+1 <= r-1:
    new_state=copy.deepcopy(node.state)
    new_state[x][y],new_state[x+1][y]=new_state[x+1][y],new_state[x][y]
    h = manhattan(new_state, goal_state, r, c)
    children.append(Node(new_state, h, node, node.depth+1, move=f"{new_state[x][y]}U"))
  
  return children

def get_path(goal_node):
  path=[]
  while goal_node.parent !=None:
    
    # store the step reversely
    path.insert(0,goal_node.move)
    goal_node=goal_node.parent
  return path


def manhattan(state, goal_state, r, c):
  h = 0
  for i in range(1, r*c):
    c_x, c_y = find_target(state, i, r, c)
    g_x, g_y = find_target(goal_state, i, r, c)
    h += abs(c_x-g_x)+abs(c_y-g_y)
  return h

def dfs(node, f_limit):
  
  global goal_state
  #print(node.state, f_limit)
  # next node's f is greater than current f_limit
  if node.f > f_limit:
    return [node.f]

  if np.array_equal(node.state, goal_state):
    return ["Found", node]

  next_f = 2147483647
  for suc_node in get_neighbors(node, goal_state):
    info = dfs(suc_node, f_limit)
    if info[0] == "Found":
      return ["Found", info[1]]
      
    if info[0] < next_f:
      next_f = info[0]

  return [next_f]
  
def idA(start_state):
  start = timeit.default_timer()
  global goal_state
  r, c = len(start_state), len(start_state[0])
  h = manhattan(start_state, goal_state, r, c)
  
  root = Node(start_state, h = h, depth=0, move='Start')
  f_limit = root.f
 
  
  while True:
    info = dfs(root, f_limit)
    
    # Found goal state return sth
    if info[0] == "Found":
      stop = timeit.default_timer()
      node = info[1]
      
      return get_path(node), node.depth, (stop-start)

    # If didn't find goal state, then update f_limit 
    f_limit = info[0]
    
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

  # numbers of inversion, row of blank
  ni, rob= get_ni_rob(start_state, r*c)
  rob = int(rob/r)
  #print(ni, rob)
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
  result = idA(start_state)
  L = [f"Total run time = {result[2]} seconds.\n", f"An optimal solution has {result[1]} moves.\n"]
  #print(f"Total run time = {result[2]} seconds.")
  #print(f"An optimal solution has {result[1]} moves.")
  output_file.writelines(L)
  for m in result[0]:
    #print(m, end=" ")
    output_file.write(f"{m} ")
    

# Closing file
output_file.close()



