import pygame
import random
import copy


BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

blocksize=30
dimension=[20,10]
size = [blocksize*(dimension[1]+7), blocksize*(dimension[0]+1)]

list_of_tetris=[
    [[-2,-1],[-1,-1],[0,-1],[0,0]],
    [[1,-1],[0,-1],[-1,-1],[-1,0]],
    [[0,0],[0,-1],[-1,-1],[-1,0]],
    [[0,0],[0,-1],[1,-1],[-1,0]],
    [[0, 0], [-2, -1], [-1, -1], [-1, 0]],
    [[-2, -1], [-1, -1], [0, -1],[1,-1] ],
    [[1,0], [0,0], [-1, 0], [0, -1]]
]

different_shapes=len(list_of_tetris)

def set_to_the_beginning():
    return  int(dimension[1]//2),  0, 0

def check_and_delete_bottom_blocks_and_increase_count_and_y_speed(bottom_blocks, count, y_speed):
    for i in range(dimension[0]):
        index = 0
        for j in range(dimension[1]):
            if bottom_blocks.blocks[j][i] == 0:
                index = 1
        if index == 0:
            bottom_blocks.kill(i)
            count += 1
            if count % 3 == 0:
                y_speed += 0.1
    return bottom_blocks, count, y_speed

def print_initial_message(screen):
    font = pygame.font.SysFont('TimesNewRoman', blocksize * 3, True, False)
    text5 = font.render("Press Enter", True, BLUE)
    text6 = font.render("to continue", True, BLUE)
    screen.blit(text5, [int(50 * (blocksize / 25)), int(150 * (blocksize / 25))])
    screen.blit(text6, [int(50 * (blocksize / 25)), int(250 * (blocksize / 25))])

def print_scoreboard(screen, count):
    font = pygame.font.SysFont('TimesNewRoman', blocksize, True, False)
    text1 = font.render("SCORE", True, BLACK)
    text2 = font.render(str(count), True, BLACK)
    text3 = font.render("LEVEL", True, BLACK)
    text4 = font.render(str(count // 2), True, BLACK)
    screen.blit(text1, [blocksize * (dimension[1] + 1), blocksize * 1])
    screen.blit(text2, [blocksize * (dimension[1] + 1), blocksize * 4])
    screen.blit(text3, [blocksize * (dimension[1] + 1), blocksize * 7])
    screen.blit(text4, [blocksize * (dimension[1] + 1), blocksize * 10])

def draw_background(screen):
    screen.fill(WHITE)
    pygame.draw.rect(screen, WHITE, [0,0, blocksize*dimension[1],blocksize*dimension[0]])
    for i in range(dimension[0]+1):
        pygame.draw.line(screen, BLACK, [0, i*blocksize], [dimension[1]*blocksize, i*blocksize], 1)
    for i in range(dimension[1]+1):
        pygame.draw.line(screen, BLACK, [i*blocksize, 0], [i*blocksize, dimension[0]*blocksize], 1)


def setup_drops(tetris_lookahead):
    tetris_lookahead.append(random.randrange(0, different_shapes))
    tetris_piece = tetris(list_of_tetris[tetris_lookahead[0]])
    tetris_lookahead.pop(0)
    tetris_future = tetris(list_of_tetris[tetris_lookahead[0]])
    return tetris_lookahead, tetris_piece, tetris_future

class bottom:

    def __init__(self):
        self.blocks=[]
        for i in range(dimension[1]):
            self.blocks.append([])
            for j in range(dimension[0]):
                self.blocks[i].append(0)
            self.blocks[i].append(1)

    def draw(self, screen, color):
        for i in range(dimension[1]):
            for j in range(dimension[0]):
                if self.blocks[i][j] != 0:
                    temp=[i,j,1,1]
                    temp=[x * blocksize for x in temp]
                    pygame.draw.rect(screen, color, temp)

    def insert(self,tet):
        for i in range(4):
            if tet.shape_position[i][0]>=0 and tet.shape_position[i][1]>=0:
                self.blocks[tet.shape_position[i][0]][tet.shape_position[i][1]] =1

    def kill(self,i):
        for j in range(dimension[1]):
            for k in range(0,i):
                self.blocks[j][i-k]=self.blocks[j][i-1-k]
            self.blocks[j][0] = 0