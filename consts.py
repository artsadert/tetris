#screen size
from typing import Tuple
from random import randint

X, Y = 600, 900
#size of blocks
size = X // 20
#Colors
BACKGROUND = (20, 20, 20)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
PURPLE = (200, 0, 200)
CYAN = (0, 200, 200)


def get_random_color() -> Tuple[int, int, int]:
    a = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]

    return a[randint(0, len(a) - 1)]
