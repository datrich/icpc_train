# By tuandat
# This python code just show how i handle the problem, not use to engage a competition
# Bc this little shit is time limit exceeded.
n = list(map(int, input().split()))
c = set()
e = set()
f = set()

a = []
for _ in range(n[2]):
    line = input().split()
    dx, dy, count = int(line[0]), int(line[1]), int(line[2])
    positions = [(int(line[i]), int(line[i+1])) for i in range(3, len(line), 2)]
    a.append((dx, dy, count, positions))
    c.update(positions)

def vector(ax, ay, bx, by, dx, dy):
    x_diff, y_diff = bx - ax, by - ay
    if dx == 0 and dy != 0:
        return x_diff == 0 and y_diff % dy == 0 and y_diff // dy > 0
    if dy == 0 and dx != 0:
        return y_diff == 0 and x_diff % dx == 0 and x_diff // dx > 0
    if dx != 0 and dy != 0:
        return x_diff % dx == 0 and x_diff // dx > 0 and x_diff / dx == y_diff / dy
    return False

for dx, dy, count, positions in a:
    for x, y in positions:
        for cx, cy in c:
            if (cx, cy) != (x, y) and vector(x, y, cx, cy, dx, dy):
                if (cx,cy) not in positions:
                    nx, ny = x + dx, y + dy
                    while nx < cx:
                        if (nx, ny) not in c and (nx, ny) not in e:
                            e.add((nx, ny))
                        nx += dx
                        ny += dy

temp = -1
while len(f) > temp:
    temp = len(f)
    for i in range(1, n[0] + 1):  # Iterate over rows (dx)
        for j in range(1, n[1] + 1):  # Iterate over columns (dy)
            valid = True

            for dx, dy, _, _ in a:
                # Calculate surrounding points
                top_left = (i - dx, j - dy)  # Respect (row, column) format
                bottom_right = (i + dx, j + dy)  # Respect (row, column) format
                # Conditions for invalidity
                if (top_left not in c and top_left not in f) or (bottom_right in c):
                    valid = False
                    break

            # If valid, add the point to 'f'
            if valid and (i, j) not in c and (i, j) not in f:
                f.add((i, j))

for j in range(1, n[1] + 1):
    row = ''
    for i in range(1, n[0] + 1):
        if (i, j) in c or (i, j) in e:
            row += '#'
        else:
            row += '.'
    print(row)

print()

for j in range(1, n[1] + 1):
    row = ''
    for i in range(1, n[0] + 1):
        if (i, j) in c or (i, j) in e or (i, j) in f:
            row += '#'
        else:
            row += '.'
    print(row)
