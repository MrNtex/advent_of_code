from collections import deque
from scipy.spatial import ConvexHull
from scipy.ndimage import binary_fill_holes
import numpy as np
import matplotlib.pyplot as plt

data = []
with open("day_9/input.txt") as f:
  for line in f:
    data.append(list(map(int, line.strip().split(","))))

data = np.array(data)

def part_1():
  hull = ConvexHull(data)
  hull_points = data[hull.vertices]
  
  best_area = -1
  for i in range(len(hull_points)):
    for j in range(i + 1, len(hull_points)):
      w = abs(hull_points[i][0] - hull_points[j][0]) + 1
      h = abs(hull_points[i][1] - hull_points[j][1]) + 1
      area = w * h
      best_area = max(best_area, area)

  return best_area

# ------ Unoptimized version ------
# Memory is cheap :DDD
def fill_polygon():
  max_x = np.max(data[:, 0])
  max_y = np.max(data[:, 1])

  grid = np.zeros((max_x + 2, max_y + 2), dtype=bool)

  for k in range(len(data)):
    x, y = data[k]
    x2, y2 = data[(k + 1) % len(data)]

    x += 1
    y += 1
    x2 += 1
    y2 += 1

    if x == x2:
      if y > y2:
        y, y2 = y2, y
      grid[x, y:y2 + 1] = True
    elif y == y2:
      if x > x2:
        x, x2 = x2, x
      grid[x:x2 + 1, y] = True

  # dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  # queue = deque([(0, 0)])
  # outside = np.zeros((max_x + 2, max_y + 2), dtype=bool)
  # outside[0, 0] = True

  # while queue:
  #   x, y = queue.popleft()
  #   for dx, dy in dirs:
  #     nx, ny = x + dx, y + dy
  #     if 0 <= nx < max_x + 2 and 0 <= ny < max_y + 2:
  #       if not grid[nx, ny] and not outside[nx, ny]:
  #         outside[nx, ny] = True
  #         queue.append((nx, ny))

  filled_area = binary_fill_holes(grid)
  return filled_area

def part_2():
  filled_area = fill_polygon()

  sat = np.zeros((filled_area.shape[0] + 1, filled_area.shape[1] + 1), dtype=int)
  sat[1:, 1:] = filled_area.cumsum(axis=0).cumsum(axis=1)

  best_area = -1

  for i in range(len(data)):
    for j in range(i + 1, len(data)):
      x, y = data[i]
      x2, y2 = data[j]
      w = abs(x - x2) + 1
      h = abs(y - y2) + 1
      area = w * h
      if area <= best_area:
        continue

      x1, x2 = sorted([x, x2])
      y1, y2 = sorted([y, y2])

      actual_sum = (sat[x2, y2] 
                  - sat[x1, y2] 
                  - sat[x2, y1] 
                  + sat[x1, y1])
      
      if actual_sum == area:
        best_area = area
  return best_area
# ------ Optimized version ------

def part_2_compressed():
  unique_x = np.unique(data[:, 0])
  unique_y = np.unique(data[:, 1])
  
  x_map = {val: i * 2 for i, val in enumerate(unique_x)}
  y_map = {val: i * 2 for i, val in enumerate(unique_y)}
  grid_w = len(unique_x) * 2 + 2
  grid_h = len(unique_y) * 2 + 2
  
  grid = np.zeros((grid_h, grid_w), dtype=bool)

  n_points = len(data)
  for k in range(n_points):
    p1 = data[k]
    p2 = data[(k + 1) % n_points]

    c1_x, c1_y = x_map[p1[0]] + 1, y_map[p1[1]] + 1
    c2_x, c2_y = x_map[p2[0]] + 1, y_map[p2[1]] + 1

    if c1_x == c2_x:
      start, end = sorted([c1_y, c2_y])
      grid[start:end+1, c1_x] = True
    else:
      start, end = sorted([c1_x, c2_x])
      grid[c1_y, start:end+1] = True
        
  filled_grid = binary_fill_holes(grid)

  sat = np.zeros((grid_h + 1, grid_w + 1), dtype=int)
  sat[1:, 1:] = filled_grid.cumsum(axis=0).cumsum(axis=1)

  best_area = 0
  
  for i in range(n_points):
    for j in range(i + 1, n_points):
      p1 = data[i]
      p2 = data[j]
      real_w = abs(p1[0] - p2[0]) + 1
      real_h = abs(p1[1] - p2[1]) + 1
      real_area = real_w * real_h
      
      if real_area <= best_area:
          continue
      
      x1_idx = x_map[p1[0]] + 1
      y1_idx = y_map[p1[1]] + 1
      x2_idx = x_map[p2[0]] + 1
      y2_idx = y_map[p2[1]] + 1

      c_x1, c_x2 = sorted([x1_idx, x2_idx])
      c_y1, c_y2 = sorted([y1_idx, y2_idx])
      
      r1, r2 = c_y1, c_y2 + 1
      c1, c2 = c_x1, c_x2 + 1
      
      expected_area = (r2 - r1) * (c2 - c1)
      
      actual_sum = (sat[r2, c2] 
                  - sat[r1, c2] 
                  - sat[r2, c1] 
                  + sat[r1, c1])
      
      if actual_sum == expected_area:
          best_area = real_area
              
  return best_area

print(part_2_compressed())