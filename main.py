import pygame
import math as maths
import time
import random

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Hello World!')



class Node:
  def __init__(self, state, pos, grid, allow_diagonals):
    self.sprite = pygame.image.load("square.png")
    self.sprite = pygame.transform.scale(self.sprite, (50, 50))
    self.colour = (0,0,0)
    self.inPath = False
    self.allow_diagonals = allow_diagonals
    
    self.state = state
    self.pos = pos
    self.screenPos = [50*pos[0], 50*pos[1]]
    self.grid = grid
    
    if self.state == "null":
      self.open = None
    if self.state == "player":
      self.open = True
      self.calculate(None)
    if self.state == "goal":
      self.open = None
    if self.state == "wall":
      self.open = False
      
  def get_h_cost(self):
    #It will move diagonally until its on the same row or column as the end goal and then move orthogonaly to the goal
    delta_x = abs(self.pos[0]-self.grid.goal_pos[0]) # difference in the x values of the node and end node.
    delta_y = abs(self.pos[1]-self.grid.goal_pos[1]) # difference in the x values of the node and end nodes.
    if self.allow_diagonals:
      if delta_x >= delta_y:
        self.h_cost = delta_y*14 + (delta_x-delta_y)*10
      else:
        self.h_cost = delta_x*14 + (delta_y-delta_x)*10
    else:
      self.h_cost = delta_x * 10 + delta_y * 10
      
  def calculate(self, parentNode):
    #self.g_cost = 10 * round(maths.sqrt((self.grid.player_pos[0]-self.pos[0])**2 + (self.grid.player_pos[1]-self.pos[1])**2), 1) #Distance from starting node (player)
    #self.h_cost = 10 * round(maths.sqrt((self.grid.goal_pos[0]-self.pos[0])**2 + (self.grid.goal_pos[1]-self.pos[1])**2), 1) #Distance from end node (goal)
    #self.f_cost = self.g_cost + self.h_cost # The main number
    #print(self.g_cost)

    
    # This method follows the specific path
    #if parentNode != None:
      #print(self.pos, parentNode.pos)
    self.parentNode = parentNode
    if parentNode != None:
      self.g_cost = parentNode.g_cost
      self.g_cost = parentNode.h_cost
      if self.pos[0] == parentNode.pos[0] or self.pos[1] == parentNode.pos[1]: # If it moved orthogonally
        self.g_cost += 10
      elif self.allow_diagonals:
        self.g_cost += 14
    else:
      self.g_cost = 0
      
    self.get_h_cost()
    self.f_cost = self.g_cost + self.h_cost
  def show(self):
    if self.state == "player" or self.state == "goal":
      colour = (150,150,255)
    elif self.inPath == True:
      colour = (255,255,0)
    elif self.state == "wall":
      colour = (0,0,0)
    elif self.open == None:
      colour = (255,255,255)
    elif self.open == True:
      colour = (0,255,0)
    else:
      colour = (255, 0, 0)
    #print(self.inPath)
    #print(colour)
    var = pygame.PixelArray(self.sprite)
    var.replace(self.colour,colour)
    del var

    self.colour = colour

    screen.blit(self.sprite, (self.screenPos[0], self.screenPos[1]))
class Grid:
  def __init__(self, size, walls, player, goal, allow_diagonals):
    self.grid = []
    self.player_pos = player
    self.goal_pos = goal
    self.allow_diagonals = allow_diagonals
    for i in range(size[1]):
      self.grid.append([])
      for j in range(size[0]):
        if [j, i] in walls:
          self.grid[i].append(Node("wall", [j,i], self, allow_diagonals))
        elif [j, i] == player:
          self.grid[i].append(Node("player", [j,i], self, allow_diagonals))
        elif [j, i] == goal:
          self.grid[i].append(Node("goal", [j,i], self, allow_diagonals))
        else:
          self.grid[i].append(Node("null", [j,i], self, allow_diagonals))
          
  def show(self):
    for i in self.grid:
      for j in i:
        j.show()
    pygame.display.update()
  def getNeighbours(self,node):
    neighbours = []

    if self.allow_diagonals:
      if 0 <= (node[1]-1):
        if 0 <= (node[0]-1):
          neighbours.append(self.grid[node[1]-1][node[0]-1])
        neighbours.append(self.grid[node[1]-1][node[0]])
        if (node[0]+1) < len(self.grid):
          neighbours.append(self.grid[node[1]-1][node[0]+1])
  
      if 0 <= (node[0]-1):
        neighbours.append(self.grid[node[1]][node[0]-1])
      #neighbours.append(self.grid[node[1]][node[0]])
      if (node[0]+1) < len(self.grid):
        neighbours.append(self.grid[node[1]][node[0]+1])
  
      if (node[1]+1) < len(self.grid):
        if 0 <= (node[0]-1):
          neighbours.append(self.grid[node[1]+1][node[0]-1])
        neighbours.append(self.grid[node[1]+1][node[0]])
        if (node[0]+1) < len(self.grid):
          neighbours.append(self.grid[node[1]+1][node[0]+1])
    else:
      if 0 <= node[0]-1:
        neighbours.append(self.grid[node[1]][node[0]-1])

      if 0 <= node[1]-1:
        neighbours.append(self.grid[node[1]-1][node[0]])

      if node[0]+1 < len(self.grid):
        neighbours.append(self.grid[node[1]][node[0]+1])

      if node[1]+1 < len(self.grid):
        neighbours.append(self.grid[node[1]+1][node[0]])

    return neighbours
  def run(self):
    #candidates = self.getNeighbours(player) #List of searchable nodes
    openNodes = []
    for i in self.grid:
      for j in i:
        if j.open == True:
          openNodes.append(j)
    if len(openNodes) != 0:      
      lowestCost = openNodes[0].f_cost
      lowestNode = openNodes[0]
      for i in openNodes:
        #print(i)
        if i.f_cost < lowestCost:
          lowestNode = i
          lowestCost = i.f_cost
        elif i.f_cost == lowestCost:
          if i.h_cost < lowestCost:
            lowestNode = i
            lowestCost = i.f_cost
  
      self.selectedNode = lowestNode
  
      #print(selectedNode)
      neighbours = self.getNeighbours(self.selectedNode.pos)
  
      for i in neighbours:
        if i.open != False:
          i.open = True
          i.calculate(self.selectedNode)
  
      self.selectedNode.open = False
  
      #print()
      return True
    else:
      return False

def random_walls(number, player, goal):
  walls = []
  for i in range(number):
    wall = [random.randint(0,9),random.randint(0,9)]
    while wall == player or wall == goal or wall in walls:
      wall = [random.randint(0,9),random.randint(0,9)]
    walls.append(wall)
  return walls

#walls = [[7,0],[7,1],[7,2],[7,3],[7,4],[7,5], [7,6], [7,7], [7,8], [3,1], [3,2], [3,3], [3,4], [3,5], [3,6], [3,7], [3,8], [3,9], [1,0], [1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7], [1,8]]

def get_path(size, walls, player, goal, allow_diagonals):
  test = Grid(size,walls,player,goal, allow_diagonals)
  while test.grid[test.goal_pos[1]][test.goal_pos[0]].open == None: 
    if test.run():
      test.show()
      pass
    else:
      break
    
  if test.run(): # So that the goal becomes the selected node
  
    #print(test.grid)
    
    
    node = test.selectedNode
    #print(node.parentNode.pos)
    
    #quit()
    path = []
    #i = 0
    while node != test.grid[test.player_pos[1]][test.player_pos[0]]:
      path.append(node)
      node.inPath = True
      #print(node.pos, test.player_pos)
      #print(node.inPath)
      #print("")
      node.show()
      #print(node.pos)
      node = node.parentNode ### This is not working how I expected it to
      #print("p", node.pos)
      #print(path)
    pygame.display.update()
      #if i == 1:
      #quit()
      #i += 1
    return path
  else:
    return False
  '''
  while True:
    screen.fill((90,90,90))
    pygame.display.update()
  '''

#print(get_path())






def get_valid_level():
  path = False
  while not path:
    path = True
    walls = random_walls(25,[9,9],[0,0])
    if not get_path([10,10], walls, [9,9],[0,0], False):
      path = False
    elif not get_path([10,10], walls, [0,5],[9,9], False):
      path = False
    else:
      return get_path([10,10], walls, [0,5],[9,9], False)

path = get_valid_level()
for i in path:
  print(i.pos)

  #[7,0],[7,1],[7,2],[7,3],[7,4],[7,5], [7,6], [7,7], [7,8], [3,1], [3,2], [3,3], [3,4], [3,5], [3,6], [3,7], [3,8], [3,9], [1,0], [1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7], [1,8]
