data = []

with open("C:\\Users\\ntexy\\advent_of_code\\day_4\\input.txt") as file:
  data = file.readlines()
data = [list(line.strip()) for line in data]
  
def part_1():
  accessible = 0
  vectors = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]

  for y in range(len(data)):
    for x in range(len(data[y])):
      if data[y][x] != "@":
        continue
      paper = 0
      for vec in vectors:
        new_x = x + vec[0]
        new_y = y + vec[1]
        if new_x < 0 or new_x >= len(data[y]) or new_y < 0 or new_y >= len(data):
          continue
        print(f"Checking position x: {new_x}, y: {new_y}")
        if data[new_y][new_x] == "@":
          paper += 1
      if paper < 4:
        accessible += 1

  return accessible

def part_2():
  vectors = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
  possible_changes = set()

  for y in range(len(data)):
    for x in range(len(data[y])):
      if data[y][x] == "@":
        possible_changes.add((x, y))

  while possible_changes:
    change = possible_changes.pop()
    x, y = change
    if data[y][x] != "@":
        continue
    my_possible_changes = []
    paper = 0
    for vec in vectors:
      new_x = x + vec[0]
      new_y = y + vec[1]
      if new_x < 0 or new_x >= len(data[y]) or new_y < 0 or new_y >= len(data):
        continue

      if data[new_y][new_x] == "@":
        my_possible_changes.append((new_x, new_y))
        paper += 1
    if paper < 4:
      for change in my_possible_changes:
        possible_changes.add(change)
      data[y][x] = "x"

  return sum([1 for line in data for c in line if c == "x"])

print(part_2())
      