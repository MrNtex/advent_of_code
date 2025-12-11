with open("day_11/input.txt") as f:
  data = [line.strip() for line in f]

def part_1():
  mapping = {}
  for line in data:
    parts = line.split(' ')
    key = parts[0][:-1]
    values = parts[1:]
    mapping[key] = values

  visited = {}
  def dfs(node, dac, fft):
    if (node,dac,fft) in visited:
      return visited[(node,dac,fft)]
    if node == 'dac':
      dac = True
    if node == 'fft':
      fft = True
    if node == 'out' and dac and fft:
      return 1
    total = 0
    for neighbor in mapping.get(node, []):
      total += dfs(neighbor, dac, fft)
    visited[(node,dac,fft)] = total
    return total
  return dfs('svr', False, False)

print(part_1())