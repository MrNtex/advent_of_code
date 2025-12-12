with open("day_12/input.txt") as f:
	lines = [line.strip() for line in f]

def parse_input():
	raw_shapes = []
	regions = []
	i = 0
	while i < len(lines):
		if not lines[i]:
			i += 1
			continue
		if "x" in lines[i]:
			break
		if lines[i].endswith(":"):
			i += 1
			shape_coords = []
			y = 0
			while i < len(lines) and lines[i] != "":
				for x, char in enumerate(lines[i]):
					if char == '#':
						shape_coords.append((y, x))
				y += 1
				i += 1
			raw_shapes.append(shape_coords)
		else:
			i += 1
	while i < len(lines):
		line = lines[i]
		if 'x' in line:
			parts = line.split(':')
			dims = parts[0].strip()
			counts = list(map(int, parts[1].strip().split()))
			w, h = map(int, dims.split('x'))
			regions.append({'width': w, 'height': h, 'counts': counts})
		i += 1
	return raw_shapes, regions
def part_1():
  def normalize(shape):
    if not shape: return frozenset()
    min_y = min(y for y, x in shape)
    min_x = min(x for y, x in shape)
    return frozenset((y - min_y, x - min_x) for y, x in shape)

  def get_transformations(shape):
    variations = set()
    current = shape
    for _ in range(4):
      current = [(x, -y) for y, x in current]
      variations.add(normalize(current))
      flipped = [(y, -x) for y, x in current]
      variations.add(normalize(flipped))
    return list(variations)

  def can_place(grid, shape, offset_y, offset_x, H, W):
    for y, x in shape:
      ny, nx = y + offset_y, x + offset_x
      if not (0 <= ny < H and 0 <= nx < W):
        return False
      if grid[ny][nx]:
        return False
    return True

  def toggle_grid(grid, shape, offset_y, offset_x, value):
    for y, x in shape:
      grid[y + offset_y][x + offset_x] = value

  def check_next_fits(grid, next_idx, all_variants, H, W):
    for variant in all_variants[next_idx]:
      shape_h = max(y for y, x in variant) + 1
      shape_w = max(x for y, x in variant) + 1
      for y in range(H - shape_h + 1):
        for x in range(W - shape_w + 1):
          if can_place(grid, variant, y, x, H, W):
            return True
    return False

  def solve_recursive(grid, presents_queue, all_variants, H, W, last_shape_idx=-1, last_pos_idx=-1):
    if not presents_queue:
      return True

    present_idx = presents_queue[0]
    remaining_presents = presents_queue[1:]
    
    start_pos = 0
    if present_idx == last_shape_idx:
      start_pos = last_pos_idx

    for variant in all_variants[present_idx]:
      shape_h = max(y for y, x in variant) + 1
      shape_w = max(x for y, x in variant) + 1
      
      for pos in range(start_pos, H * W):
        y, x = divmod(pos, W)
        if y + shape_h > H or x + shape_w > W:
          continue
        if can_place(grid, variant, y, x, H, W):
          toggle_grid(grid, variant, y, x, True)
          if not remaining_presents or check_next_fits(grid, remaining_presents[0], all_variants, H, W):
            if solve_recursive(grid, remaining_presents, all_variants, H, W, present_idx, pos):
              return True
          
          toggle_grid(grid, variant, y, x, False)
    return False

  raw_shapes, regions = parse_input()
  all_variants = [get_transformations(s) for s in raw_shapes]
  shape_areas = [len(s) for s in raw_shapes]
  success_count = 0

  for i, region in enumerate(regions):
    W, H = region['width'], region['height']
    counts = region['counts']
    presents_to_fit = []
    total_present_area = 0
    
    for shape_idx, count in enumerate(counts):
      for _ in range(count):
        presents_to_fit.append(shape_idx)
        total_present_area += shape_areas[shape_idx]
    
    if total_present_area > (W * H):
      print(f"Region {i}: Impossible (Area too large)")
      continue

    presents_to_fit.sort(key=lambda idx: shape_areas[idx], reverse=True)	
    grid = [[False for _ in range(W)] for _ in range(H)]
    
    if solve_recursive(grid, presents_to_fit, all_variants, H, W):
      print(f"Region {i} ({W}x{H}): Fits!")
      success_count += 1
    else:
      print(f"Region {i} ({W}x{H}): Does not fit.")

  return success_count
print(part_1())