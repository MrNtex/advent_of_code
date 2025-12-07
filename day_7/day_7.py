import collections

data = []

with open('day_7/input.txt') as f:
  for line in f:
    data.append(line.strip())

def get_splits():
  x_to_splits = {}
  for y, line in enumerate(data):
    for x, c in enumerate(line):
      if c == '^':
        if x not in x_to_splits:
          x_to_splits[x] = []
        x_to_splits[x].append(y)
  
  return x_to_splits

def part_1():
  x_to_splits = get_splits()
  
  start_x = -1
  for idx, x in enumerate(data[0]):
    if x == 'S':
      start_x = idx
      break

  queue = collections.deque([(start_x, 0)])
  hit_splitters = set()

  while queue:
    curr_x, curr_y = queue.popleft()
    found_splitter_y = -1
    
    if curr_x in x_to_splits: # if there is more data can be binary searched
      for sy in x_to_splits[curr_x]:
        if sy > curr_y:
          found_splitter_y = sy
          break

    if found_splitter_y != -1:
      splitter_coord = (curr_x, found_splitter_y)
      if splitter_coord not in hit_splitters:
        hit_splitters.add(splitter_coord)

        left_beam = (curr_x - 1, found_splitter_y)
        right_beam = (curr_x + 1, found_splitter_y)

        queue.append(left_beam)
        queue.append(right_beam)

  return len(hit_splitters)

def part_2():
  x_to_splits = get_splits()
  
  memo = {}

  def dfs(x, y):
    if (x, y) in memo:
      return memo[(x, y)]

    found_splitter_y = -1

    if x in x_to_splits:
      for sy in x_to_splits[x]:
        if sy > y:
          found_splitter_y = sy
          break

    if found_splitter_y == -1:
      return 1
    
    left_count = dfs(x - 1, found_splitter_y)
    right_count = dfs(x + 1, found_splitter_y)
    
    total = left_count + right_count
    
    memo[(x, y)] = total
    return total

  start_x = -1
  for idx, x in enumerate(data[0]):
    if x == 'S':
      start_x = idx
      break
      
  return dfs(start_x, 0)
print(part_2())