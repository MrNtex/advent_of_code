with open("day_2/input.txt") as file:
    data = file.read()

ids = data.replace("\n", "").split(",")

ids = [id.strip() for id in ids]

def part_1():
  total = 0
  for id in ids:
    left, right = id.split("-")[0], id.split("-")[1]

    for x in range(int(left), int(right)+1):
      n = len(str(x))
      if n % 2 == 0:
        mid = n // 2
        if str(x)[mid:] == str(x)[:mid]:
          total += x
  return total

def part_2():
  total = 0
  for id in ids:
    left, right = id.split("-")[0], id.split("-")[1]

    for x in range(int(left), int(right)+1):
      n = len(str(x))
      for div in range(1, int(n**0.5)+1):
        if n % div == 0:
          #print(f"x: {x}, div: {div}, n//div: {n//div}, slice: {str(x)[:div]}, part: {(str(x)[:div])*(n//div)}")
          if str(x)[:div]*(n//div) == str(x) and n//div > 1:
            #print(f"Found repeating number: {x}")
            total += x
            break
          divided = n // div
          if divided != div and divided < n and n//divided > 1:
            if str(x)[:divided]*(n//divided) == str(x):
              #print(f"Found repeating number: {x}")
              total += x
              break

  return total

print(part_2())
      