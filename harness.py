from collections import namedtuple

from snake import move


Point = namedtuple('P', 'x y')
Snake = namedtuple('S', 'head body')

def mksnake(*body):
    return Snake(body[0], body)


print move(mksnake((0, 0)), mksnake((5, 5)), (4, 4), None, 10, 10)
