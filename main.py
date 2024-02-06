#!/usr/local/bin/python
import pygame

from consts import BACKGROUND, X, Y, get_random_color, size
from objects import rand_phigure


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((X, Y))
        self.working = True
        self.hard_mode = 200
        self.temp_object = rand_phigure(self.screen)
        self.scope = 0
        
        self.map = [[[[0, 0], 0] for i in range(X // size)] for j in range(Y // size)]

    def new_object(self):
        self.temp_object = rand_phigure(self.screen)

    def objects_fall(self):
        dropped = self.temp_object.is_dropped()
        square = self.temp_object.get_coordinate_square()
        coord = self.temp_object.get_coordinate()

        if dropped:
            for i, (x, y) in enumerate(square):
                self.map[y][x][1] = self.temp_object.get_color() 
                self.map[y][x][0] = coord[i].copy()           

            self.new_object()
    def one_bottom(self, cube):
        cube[0] = [cube[0][0], cube[0][1] + size]
        return cube

    def roll(self):
        for i, line in enumerate(self.map):
            works = True
            for item in line:
                if item[1] == 0:
                    works = False
                else:
                    if self.temp_object.is_connected(item[0]):
                        square = self.temp_object.get_coordinate_square()
                        coord = self.temp_object.get_coordinate()
                        for i, (x, y) in enumerate(square):
                            self.map[y][x] = [coord[i].copy(), self.temp_object.get_color()]
                        self.new_object()
            if works:
                #print("rock and roll!!")
                self.scope += 1
                self.hard_mode -= 2
            
                for j in range(len(line)):
                    self.map[i][j] = [[0, 0], 0]
                print(i)
                for stack_line in range(i - 1, 0, -1):
                    for cube in range(X // size):
                        if self.map[stack_line][cube][1] != 0:

                            #print(self.map[stack_line + 1][cube], self.map[stack_line][cube], "b")

                            self.map[stack_line + 1][cube] = self.one_bottom(self.map[stack_line][cube].copy())
                            self.map[stack_line][cube] = [[0, 0], 0]
                
                            #print(self.map[stack_line + 1][cube], self.map[stack_line][cube], "a")

                
    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.temp_object.drop_down()
                if event.key == pygame.K_s:
                    self.temp_object.update_direction()
                if event.key == pygame.K_a:
                    self.temp_object.left()
                if event.key == pygame.K_d:
                    self.temp_object.right()

    def run(self):
        while self.working:
            self._events()
            self.screen.fill(BACKGROUND)
            self.temp_object.draw()
            self.objects_fall()
             
            self.roll()
                        
            # print(self.temp_object.direction)
            for line in self.map:
                for item in line:
                    if item[1] != 0:
                        pygame.draw.rect(self.screen, item[1], (item[0], [size-6, size - 6]))

            pygame.display.update()
            self.temp_object.drop_down()
            pygame.time.delay(self.hard_mode)
        print(self.scope)
        pygame.quit()


#pygame.draw.line(screen, RED, coordinate, end_pos, width = 3)
if __name__ == '__main__':
    game = Game()
    game.run()

