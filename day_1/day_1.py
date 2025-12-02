
data = []

with open("C:\\Users\\ntexy\\advent_of_code\\day_1\\input.txt") as file:
  data = file.readlines()

def part_1():
  total = 50
  CAP = 99
  count = 0
  for line in data:
    line = line.strip()
    val = 1 if line[0] == "R" else -1
    val *= int(line[1:])
    total = total + val
    total = total % (CAP + 1)

    if total == 0:
      count += 1
  return count

def part_2():
  total = 50
  CAP = 100
  count = 0
  for line in data:
    line = line.strip()
    val = 1 if line[0] == "R" else -1
    val *= int(line[1:])

    count += abs(val) // CAP
    reminder = abs(val)%CAP

    if reminder > 0:
      new_total = total + reminder*(1 if line[0] == "R" else -1)

      if (val > 0 and new_total >= CAP) or (val < 0 and new_total < 1 and total > 0):
        count += 1
    
      total = (new_total + CAP) % CAP 
    
  return count

print(part_2())