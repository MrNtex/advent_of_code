from pyparsing import deque
import numpy as np
from z3 import *


with open("day_10/input.txt") as f:
  data = [line.strip() for line in f]

def part_1():
  total = 0
  for line in data:
    line_split = line.split(' ')
    diagram = line_split[0]
    binary_start = diagram[1:-1].replace('#', '1').replace('.', '0')[::-1]
    start = int(binary_start, 2)

    schemas = line_split[1:-1]
    buttons = []
    for schema in schemas:
      digits = schema[1:-1].split(',')
      mask = 0
      for digit in digits:
        mask |= (1 << int(digit))
      buttons.append(mask)

    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
      current, steps = queue.popleft()
      if current == 0:
        total += steps
        break
      for btn in buttons:
        next_state = current ^ btn
        if next_state not in visited:
          visited.add(next_state)
          queue.append((next_state, steps + 1))
    
  return total

def part_2_optimized():
  total_presses = 0

  for line in data:
    parts = line.split(' ')
    target_str = parts[-1][1:-1]
    targets = list(map(int, target_str.split(',')))
    num_counters = len(targets)
    
    buttons = []
    for schema in parts[1:-1]:
      indices = list(map(int, schema[1:-1].split(',')))
      btn_vector = [0] * num_counters
      for idx in indices:
          btn_vector[idx] = 1
      buttons.append(btn_vector)
        
    optimizer = Optimize()
    presses = [Int(f'b_{i}') for i in range(len(buttons))]

    for p in presses:
      optimizer.add(p >= 0)

    for row_idx in range(num_counters):
      equation = Sum([buttons[btn_idx][row_idx] * presses[btn_idx] 
                      for btn_idx in range(len(buttons))])
      optimizer.add(equation == targets[row_idx])
        
    optimizer.minimize(Sum(presses))

    if optimizer.check() == sat:
      model = optimizer.model()
      local_sum = sum(model[p].as_long() for p in presses)
      total_presses += local_sum
    else:
      print(f"No solution found for: {targets}")

  return total_presses

print(part_2_optimized())