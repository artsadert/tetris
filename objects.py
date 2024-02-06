from pygame import draw
from consts import size, Y, X, get_random_color
from random import randint

class Phigure:
    def __init__(self, surface, coordinate, color):
        self.coordinate = coordinate
        self.direction = 1
        self.color = color
        self.surface = surface
    
    def update_direction(self):
        self.direction += 1
        if self.direction > 4:
            self.direction = 1
        #print(self.direction)
    
    def get_color(self):
        return self.color

    def drop_down(self):
        self.coordinate[1] += size

    
def rand_phigure(surface):
    a = [Line, Cube, TBlock, JBlock, LBlock, ZBlock, SBlock]
    #a = [SBlock]

    return a[randint(0, len(a)-1)](surface, [X//2-size, 0], get_random_color())


class Line(Phigure):
    """Line class"""
    def __init__(self, surface, coordinate, color):
        super().__init__(surface, coordinate, color)
    
    def draw(self):
        l_size = size - 6 #6
        tuple_size = (l_size, l_size)
        cubes = self.get_coordinate()
        for x in cubes:
            draw.rect(self.surface, self.color, (x, tuple_size))
    
    def left(self):
        if self._is_vertical() and self.coordinate[0] - size >= 0:
            self.coordinate[0] -= size 
        elif not self._is_vertical() and self.coordinate[0] - size >= size:
            self.coordinate[0] -= size

    def right(self):
        if self._is_vertical() and self.coordinate[0] + size < X:
            self.coordinate[0] += size 
        elif not self._is_vertical() and self.coordinate[0] + size * 3 < X:
            self.coordinate[0] += size
    
    def _is_vertical(self):
        return self.direction == 2 or self.direction == 4    
    
    def is_dropped(self):
        return (not self._is_vertical() and self.coordinate[1] >= Y - size) or (self._is_vertical() and self.coordinate[1] >= Y - size * 3)

    def get_coordinate(self):
        if not self._is_vertical():
            return [self.coordinate, 
                    [self.coordinate[0] - size, self.coordinate[1]], 
                    [self.coordinate[0] + size, self.coordinate[1]], 
                    [self.coordinate[0] + (size * 2), self.coordinate[1]]]
        else:
            return [self.coordinate, 
                    [self.coordinate[0], self.coordinate[1] + size], 
                    [self.coordinate[0], self.coordinate[1] - size], 
                    [self.coordinate[0], self.coordinate[1] + (size * 2)]]

    def get_coordinate_square(self):
        coord = self.get_coordinate()
        return list(map(lambda x: [x[0] // size, x[1] // size], coord))

    def is_connected(self, item):
        coord = self.get_coordinate()
        for x in coord:
            if x[0] == item[0] and x[1] + size == item[1]:
                return True
        return False 

class Cube(Phigure):
    """Cube class from phigure"""
    def __init__(self, surface, coordinate, color):
        super().__init__(surface, coordinate, color)

    def draw(self):
        l_size = size - 6 #6
        tuple_size = (l_size, l_size)

        cubes = self.get_coordinate()
        for x in cubes:
            draw.rect(self.surface, self.color, (x, tuple_size))

    def left(self):
        if self.coordinate[0] > 0:
            self.coordinate[0] -= size

    def right(self):
        if self.coordinate[0] + size * 2 < X:
            self.coordinate[0] += size

    def is_dropped(self):
        return self.coordinate[1] + size * 3 > Y
    
    def get_coordinate(self):
        return [self.coordinate, 
                [self.coordinate[0] + size, self.coordinate[1]], 
                [self.coordinate[0], self.coordinate[1] + size], 
                [self.coordinate[0] + size, self.coordinate[1] + size]]

    def get_coordinate_square(self):
        coord = self.get_coordinate()
        return list(map(lambda x: [x[0] // size, x[1] // size], coord))

    def is_connected(self, item):
        coord = self.get_coordinate()
        for x in coord:
            if x[0] == item[0] and x[1] + size == item[1]:
                return True
        return False


class TBlock(Phigure):
    """it's like t-cross, but it's phigure"""
    def __init__(self, surface, coordinate, color):
        super().__init__(surface, coordinate, color)
    
    def _is_vertical(self):
        return self.direction == 2 or self.direction == 4

    def get_coordinate(self):
        res = []
        res.append(self.coordinate) 
        if self._is_vertical():
            res.append([self.coordinate[0], self.coordinate[1] + size])   
            res.append([self.coordinate[0], self.coordinate[1] - size])
            if self.direction == 2:
                res.append([self.coordinate[0] + size, self.coordinate[1]])
            else:
                res.append([self.coordinate[0] - size, self.coordinate[1]])
        else:
            res.append([self.coordinate[0] + size, self.coordinate[1]])
            res.append([self.coordinate[0] - size, self.coordinate[1]])

            if self.direction == 3:
                res.append([self.coordinate[0], self.coordinate[1] + size])
            else:
                res.append([self.coordinate[0], self.coordinate[1] - size])

        return res

    def draw(self):
        l_size = size - 6
        tuple_size = (l_size, l_size)

        cubes = self.get_coordinate()
        for x in cubes:
            draw.rect(self.surface, self.color, (x, tuple_size))

    def left(self):
        if (self.direction == 2 and self.coordinate[0] > 0) or self.coordinate[0] - size > 0:
            self.coordinate[0] -= size

    def right(self):
        if (self.direction == 4 and self.coordinate[0] + size < X) or self.coordinate[0] + size * 2 < X:
            self.coordinate[0] += size

    def is_dropped(self):
        return (self.coordinate[1] + size * 2 > Y and self.direction == 1) or (self.coordinate[1] + size * 3 > Y and self.direction != 1)

    def get_coordinate_square(self):
        coord = self.get_coordinate()
        return list(map(lambda x: [x[0] // size, x[1] // size], coord))
    
    def is_connected(self, item):
        coord = self.get_coordinate()

        for x in coord:
            if x[0] == item[0] and x[1] + size == item[1]:
                return True
        return False


class JBlock(Phigure):
    """it's J block, it's like L block, but it's flipped"""
    def __init__(self, surface, coordinate, color):
        super().__init__(surface, coordinate, color)
    
    def _is_vertical(self):
        return self.direction == 2 or self.direction == 4

    def get_coordinate(self):
        res = []
        res.append(self.coordinate) 
        if self._is_vertical():
            res.append([self.coordinate[0], self.coordinate[1] + size])   
            res.append([self.coordinate[0], self.coordinate[1] - size])
            if self.direction == 2:
                res.append([self.coordinate[0] - size, self.coordinate[1] + size])
            else:
                res.append([self.coordinate[0] + size, self.coordinate[1] - size])
        else:
            res.append([self.coordinate[0] + size, self.coordinate[1]])
            res.append([self.coordinate[0] - size, self.coordinate[1]])

            if self.direction == 3:
                res.append([self.coordinate[0] - size, self.coordinate[1] - size])
            else:
                res.append([self.coordinate[0] + size, self.coordinate[1] + size])

        return res

    def draw(self):
        l_size = size - 6
        tuple_size = (l_size, l_size)

        cubes = self.get_coordinate()
        for x in cubes:
            draw.rect(self.surface, self.color, (x, tuple_size))

    def left(self):
        if (self.direction == 4 and self.coordinate[0] > 0) or self.coordinate[0] - size > 0:
            self.coordinate[0] -= size

    def right(self):
        if (self.direction == 2 and self.coordinate[0] + size < X) or self.coordinate[0] + size * 2 < X:
            self.coordinate[0] += size

    def is_dropped(self):
        return (self.coordinate[1] + size * 2 > Y and self.direction == 3) or (self.coordinate[1] + size * 3 > Y and self.direction != 3)

    def get_coordinate_square(self):
        coord = self.get_coordinate()
        return list(map(lambda x: [x[0] // size, x[1] // size], coord))
    
    def is_connected(self, item):
        coord = self.get_coordinate()

        for x in coord:
            if x[0] == item[0] and x[1] + size == item[1]:
                return True
        return False



class LBlock(Phigure):
    """L block"""
    def __init__(self, surface, coordinate, color):
        super().__init__(surface, coordinate, color)
    
    def _is_vertical(self):
        return self.direction == 2 or self.direction == 4

    def get_coordinate(self):
        res = []
        res.append(self.coordinate) 
        if self._is_vertical():
            res.append([self.coordinate[0], self.coordinate[1] + size])   
            res.append([self.coordinate[0], self.coordinate[1] - size])
            if self.direction == 2:
                res.append([self.coordinate[0] + size, self.coordinate[1] + size])
            else:
                res.append([self.coordinate[0] - size, self.coordinate[1] - size])
        else:
            res.append([self.coordinate[0] + size, self.coordinate[1]])
            res.append([self.coordinate[0] - size, self.coordinate[1]])

            if self.direction == 3:
                res.append([self.coordinate[0] - size, self.coordinate[1] + size])
            else:
                res.append([self.coordinate[0] + size, self.coordinate[1] - size])

        return res

    def draw(self):
        l_size = size - 6
        tuple_size = (l_size, l_size)

        cubes = self.get_coordinate()
        for x in cubes:
            draw.rect(self.surface, self.color, (x, tuple_size))

    def left(self):
        if (self.direction == 2 and self.coordinate[0] > 0) or self.coordinate[0] - size > 0:
            self.coordinate[0] -= size

    def right(self):
        if (self.direction == 4 and self.coordinate[0] + size < X) or self.coordinate[0] + size * 2 < X:
            self.coordinate[0] += size

    def is_dropped(self):
        return (self.coordinate[1] + size * 2 > Y and self.direction == 1) or (self.coordinate[1] + size * 3 > Y and self.direction != 1)

    def get_coordinate_square(self):
        coord = self.get_coordinate()
        return list(map(lambda x: [x[0] // size, x[1] // size], coord))
    
    def is_connected(self, item):
        coord = self.get_coordinate()

        for x in coord:
            if x[0] == item[0] and x[1] + size == item[1]:
                return True
        return False

class ZBlock(Phigure):
    """Z block"""
    def __init__(self, surface, coordinate, color):
        super().__init__(surface, coordinate, color)
    
    def _is_vertical(self):
        return self.direction == 2 or self.direction == 4

    def get_coordinate(self):
        res = []
        res.append(self.coordinate) 
        if self._is_vertical():
            res.append([self.coordinate[0], self.coordinate[1] + size])   
            res.append([self.coordinate[0] - size, self.coordinate[1]])
            res.append([self.coordinate[0] + size, self.coordinate[1] + size])
        else:
            res.append([self.coordinate[0] - size, self.coordinate[1]])
            res.append([self.coordinate[0], self.coordinate[1] - size])
            res.append([self.coordinate[0] - size, self.coordinate[1] + size])

        return res

    def draw(self):
        l_size = size - 6
        tuple_size = (l_size, l_size)

        cubes = self.get_coordinate()
        for x in cubes:
            draw.rect(self.surface, self.color, (x, tuple_size))

    def left(self):
        if self.coordinate[0] - size > 0:
            self.coordinate[0] -= size

    def right(self):
        if (self._is_vertical() and self.coordinate[0] + size * 2 < X) or (not self._is_vertical() and self.coordinate[0] + size < X):
            self.coordinate[0] += size

    def is_dropped(self):
        return self.coordinate[1] + size * 3 > Y

    def get_coordinate_square(self):
        coord = self.get_coordinate()
        return list(map(lambda x: [x[0] // size, x[1] // size], coord))
    
    def is_connected(self, item):
        coord = self.get_coordinate()

        for x in coord:
            if x[0] == item[0] and x[1] + size == item[1]:
                return True
        return False

class SBlock(Phigure):
    """Z block"""
    def __init__(self, surface, coordinate, color):
        super().__init__(surface, coordinate, color)
    
    def _is_vertical(self):
        return self.direction == 2 or self.direction == 4

    def get_coordinate(self):
        res = []
        res.append(self.coordinate) 
        if self._is_vertical():
            res.append([self.coordinate[0], self.coordinate[1] + size])   
            res.append([self.coordinate[0] - size, self.coordinate[1]])
            res.append([self.coordinate[0] - size, self.coordinate[1] - size])
        else:
            res.append([self.coordinate[0] - size, self.coordinate[1]])
            res.append([self.coordinate[0], self.coordinate[1] - size])
            res.append([self.coordinate[0] + size, self.coordinate[1] - size])

        return res

    def draw(self):
        l_size = size - 6
        tuple_size = (l_size, l_size)

        cubes = self.get_coordinate()
        for x in cubes:
            draw.rect(self.surface, self.color, (x, tuple_size))

    def left(self):
        if self.coordinate[0] - size > 0:
            self.coordinate[0] -= size

    def right(self):
        if (self._is_vertical() and self.coordinate[0] + size < X) or (not self._is_vertical() and self.coordinate[0] + size * 2 < X):
            self.coordinate[0] += size

    def is_dropped(self):
        return (self.coordinate[1] + size * 2 > Y and self._is_vertical()) or (not self._is_vertical() and self.coordinate[1] + size * 3 > Y)

    def get_coordinate_square(self):
        coord = self.get_coordinate()
        return list(map(lambda x: [x[0] // size, x[1] // size], coord))
    
    def is_connected(self, item):
        coord = self.get_coordinate()

        for x in coord:
            if x[0] == item[0] and x[1] + size == item[1]:
                return True
        return False


