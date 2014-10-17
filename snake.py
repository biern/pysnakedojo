
def move(snake1=None, snake2=None, food=None, data=None, board_width=None, board_height=None):
    info = {'w': board_width, 'h': board_height, '1': snake1.body, '2': snake2.body}

    def estimate(start, goal):
        print start, goal
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def get_neighbors(current):
        for dx, dy in (1, 0), (-1, 0), (0, 1), (0, -1):
            x = current[0] + dx
            y = current[1] + dy
            print info
            if all([0 <= x < info['w'],
                    0 <= y < info['h'],
                    (x, y) not in info['1'],
                    (x, y) not in info['2'],
                  ]):
                yield x, y

    def astar(start, goal):
        closed = set()
        open = {start}
        came_from = {}

        g = {}
        f = {}
        g[start] = 0
        f[start] = g[start] + estimate(start, goal)

        while open:
            current = min(open, key=f.get)
            if current == goal:
                return to_direction(current, reconstruct_path(came_from, goal))
            open.discard(current)
            closed.add(current)
            #print 'o', open
            #print 'c', closed
            for neighbor in get_neighbors(current):
                if neighbor in closed:
                    continue
                tentative_g = g[current] + 1
                if neighbor not in open or tentative_g < g[neighbor]:
                    came_from[neighbor] = current
                    g[neighbor] = tentative_g
                    f[neighbor] = g[neighbor] + estimate(neighbor, goal)
                    if neighbor not in open:
                        open.add(neighbor)

    def reconstruct_path(came_from, current_node):
        print 'rec', current_node
        if current_node in came_from:
            p = reconstruct_path(came_from, came_from[current_node])
            return p
        else:
            return current_node

    def to_direction(a, b):
        print a, b
        if a[0] < b[0]:
            return 'l'
        elif a[0] > b[0]:
            return 'r'
        elif a[1] < b[1]:
            return 'u'
        else:
            return 'd'

    result = astar(snake1.body[0], food), data
    if result:
        return result

    # fallback
    def to_center_key(point):
        return abs(point[0] - board_width / 2) + abs(point[1] - board_height / 2)
    for neighbor in sorted(get_neighbors(current), key=to_center_key):
        return to_direction(current, neighbor), data

    # No free way. Lose :(
    return 'u', data
