import heapq


data = []

with open("C:\\Users\\ntexy\\advent_of_code\\day_3\\input.txt") as file:
  data = file.readlines()

def part_1():
  total = 0

  for line in data:
    line = line.strip()
    
    best_most_significant = (-1, -1)

    for idx, x in enumerate(line[:-1]):
      if int(x) > best_most_significant[0]:
        best_most_significant = (int(x), idx)
    
    best_lest_significant = -1
    for idx, x in enumerate(line[best_most_significant[1]+1:]):
      if int(x) > best_lest_significant:
        best_lest_significant = int(x)

    total += best_most_significant[0] * 10 + best_lest_significant
  return total

def part_2():
  total = 0

  for line in data:
    line = line.strip()
    stack = []
    
    to_drop = len(line) - 12
    
    for x in line:
      val = int(x)
      while to_drop > 0 and stack and stack[-1] < val:
        stack.pop()
        to_drop -= 1
      
      stack.append(val)
    
    final_digits = stack[:12]
    
    result_string = "".join(map(str, final_digits))
    total += int(result_string)

  return total

print(part_2())