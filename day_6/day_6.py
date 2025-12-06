data = []

with open('day_6/input.txt') as f:
  for line in f:
    data.append(line.strip().split())

def part_1():
  total = 0
  for col in range(len(data[0])):
    operation = data[-1][col]
    result = 0
    if operation == '*':
      result = 1
      for row in range(len(data)-1):
        result *= int(data[row][col])
    elif operation == '+':
      result = 0
      for row in range(len(data)-1):
        result += int(data[row][col])
    total += result
  return total

def part_2():
  data = []

  with open('day_6/input.txt') as f:
    for line in f:
      data.append(line)
  total = 0
  prev_operation = None
  nums = []
  for col in range(len(data[0])-1):
    operation = data[-1][col]
    if operation in ['*', '+']:
      #print(nums, prev_operation)
      if prev_operation == '+':
        result = 0
        for n in nums:
          if n != '':
            result += int(n)
        total += result
      elif prev_operation == '*':
        result = 1
        for n in nums:
          if n != '':
            result *= int(n)
        total += result
      nums = []
      prev_operation = operation
    
    nums.append('')

    for row in range(len(data)-1):
      if not data[row][col].isdigit():
        continue
      nums[-1] += data[row][col]

  if prev_operation == '+':
    result = 0
    for n in nums:
      if n != '':
        result += int(n)
    total += result
  elif prev_operation == '*':
    result = 1
    for n in nums:
      if n != '':
        result *= int(n)
    total += result

  return total

print(part_2())