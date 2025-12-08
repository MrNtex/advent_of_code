from scipy.spatial import KDTree
import heapq

data = []
with open("day_8/input.txt") as f:
  for line in f:
    data.append(list(map(int, line.strip().split(","))))

class UnionFind:
  def __init__(self, size):
    self.parent = list(range(size))
    self.size = [1] * size
  def find(self, p):
    if self.parent[p] != p:
      self.parent[p] = self.find(self.parent[p])
    return self.parent[p]
  def union(self, p, q):
    root_p = self.find(p)
    root_q = self.find(q)
    if root_p != root_q:
      if self.size[root_p] < self.size[root_q]:
          root_p, root_q = root_q, root_p
      self.parent[root_q] = root_p
      self.size[root_p] += self.size[root_q]
      return root_p


def part_1():
  tree = KDTree(data)
  distances, indices = tree.query(data, k=20)

  edges = []
  for i in range(len(data)):
    for j in range(1, 20):
      if i < indices[i][j]:
        edges.append((distances[i][j], i, indices[i][j]))

  edges.sort(key=lambda x: x[0])
  
  uf = UnionFind(len(data))

  for _, u, v in edges[:1000]:
    uf.union(u, v)

  visited = set()
  sizes = []
  for i in range(len(data)):
    root = uf.find(i)
    if root not in visited:
      visited.add(root)
      sizes.append(uf.size[root])

  top_3 = sorted(sizes, reverse=True)[:3]
  result = 1

  for size in top_3:
    result *= size
  return result

def part_2():
  tree = KDTree(data)
  distances, indices = tree.query(data, k=100)

  edges = []
  for i in range(len(data)):
    for j in range(1, 100):
      if i < indices[i][j]:
        edges.append((distances[i][j], i, indices[i][j]))

  edges.sort(key=lambda x: x[0])
  
  uf = UnionFind(len(data))

  for _, u, v in edges:
    root_u = uf.find(u)
    root_v = uf.find(v)

    if root_u != root_v:
      new_root = uf.union(u, v)
      if uf.size[uf.find(new_root)] == len(data):
        return data[u][0] * data[v][0]
      
  return "Failed to connect all points"

print(part_2())