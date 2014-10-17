# -*- coding: utf-8 -*-


def move(snake1=None, snake2=None, food=None, data=None, board_width=None, board_height=None):
    from collections import namedtuple
    Point = namedtuple('Point', 'x y')

    length = len(snake1.body)
    food_distance = get_food_distance(snake1)
    other_food_distance = get_food_distance(snake2)
    mode = data.get('mode')

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
        return get_point_direction(food)

    def wait():
        wait_point = get_wait_point()
        return get_point_direction(wait_point)

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

    def get_point_direction(point):
        "return direction letter to get to the point"
        pass

    def get_points_distance(point1, point2):
        pass

    # TODOs: killing mode!
    def wrap():
        other_approach_point = get_food_approach_point(snake2)
        wrap_start_point = get_wrap_start_point()

    def trap():
        data['keep-mode'] = True
        # TODO: go around the food

    actions = {
        'feed': feed,
        'wait': wait,
    }

    mode = get_mode()
    direction = actions[mode]()
    data['mode'] = mode
    return direction, data
