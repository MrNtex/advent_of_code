with open('day_5/input.txt') as f:
  input_data = f.read()

raw_ranges, raw_ids = input_data.strip().split('\n\n')

ranges = raw_ranges.split('\n')
ids = raw_ids.split('\n')

def part_1():
  sorted_ranges = sorted(ranges, key=lambda r: int(r.split('-')[0]))
  merged_ranges = []

  for r in sorted_ranges:
    start, end = map(int, r.split('-'))
    if not merged_ranges or start > merged_ranges[-1][1] + 1:
      merged_ranges.append([start, end])
    else:
      merged_ranges[-1][1] = max(merged_ranges[-1][1], end)

  count = 0

  for id in ids:
    id_num = int(id)
    l,r = 0, len(merged_ranges) - 1
    while l <= r:
      mid = (l + r) // 2
      if merged_ranges[mid][0] <= id_num <= merged_ranges[mid][1]:
        count += 1
        break
      elif id_num < merged_ranges[mid][0]:
        r = mid - 1
      else:
        l = mid + 1

  return count

def part_2():
  sorted_ranges = sorted(ranges, key=lambda r: int(r.split('-')[0]))
  merged_ranges = []

  for r in sorted_ranges:
    start, end = map(int, r.split('-'))
    if not merged_ranges or start > merged_ranges[-1][1] + 1:
      merged_ranges.append([start, end])
    else:
      merged_ranges[-1][1] = max(merged_ranges[-1][1], end)
  total_covered = sum(end - start + 1 for start, end in merged_ranges)
  return total_covered

print(part_2())