
def move(snake1=None, snake2=None, food=None, data=None, board_width=None, board_height=None):
    from collections import namedtuple
    Point = namedtuple('Point', 'x y')

    if not data:
        data = {}

    def get_mode():
        # TODO:
        # wait when food is too far or in the corner

        if data.get('keep-mode'):
            return mode

        if mode != 'wrap':
            # reset wrap params
            data['wrap-turn'] = 0

        # TODO: killing mode!
        # # TODO: should not check for food distance, but for distance to wrap
        # # approach point
        # if length > 4 and length + food_distance > other_food_distance:
        #     if food_distance == 1:
        #         return 'wrap'
        #     else:
        #         return 'trap'

        if food_distance < other_food_distance:
            return 'feed'

        return 'wait'

    def feed():
        return get_point_direction(snake1.head, food)

    def wait():
        wait_point = get_wait_point()
        return get_point_direction(snake1.head, wait_point)

    def get_wait_point():
        delta = min(length / 2, board_width / 4)

        a = Point(board_width / 2 - delta,
                  board_height / 2 - delta)
        b = Point(board_width / 2 + delta,
                  board_height / 2 + delta)

        current = data.setdefault('waiting-point', a)
        if points_equal(snake1.head, current):
            if current == a:
                data['waiting-point'] = b
            else:
                data['waiting-point'] = a

        return data['waiting-point']

    def points_equal(p1, p2):
        return p1.x == p2.x and p1.y == p2.yy

    # stubs:

    def get_food_distance(snake):
        return get_points_distance(snake.head, food)

    def get_point_direction(point1, point2):
        "return direction letter to get to the point"
        result = astar(point1, point2)
        return result[0]

    def get_points_distance(point1, point2):
        result = astar(point1, point2)
        return result[1]

    def astar(start, goal):
        """Find shortest path from start to goal

        Return: direction to go, length of path
        """
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

        def reconstruct_path(came_from, current_node):
            print 'rec', current_node
            if current_node in came_from:
                p, dist = reconstruct_path(came_from, came_from[current_node])
                return p, dist + 1
            else:
                return current_node, 0

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
                point, length = reconstruct_path(came_from, goal)
                return to_direction(current, point), length
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

    # TODOs: killing mode!
    def wrap():
        other_approach_point = get_food_approach_point(snake2)
        wrap_start_point = get_wrap_start_point()

    def trap():
        data['keep-mode'] = True
        # TODO: go around the food

    length = len(snake1.body)
    food_distance = get_food_distance(snake1)
    other_food_distance = get_food_distance(snake2)
    mode = data.get('mode')

    actions = {
        'feed': feed,
        'wait': wait,
    }

    mode = get_mode()
    direction = actions[mode]()
    data['mode'] = mode
    return direction, data
