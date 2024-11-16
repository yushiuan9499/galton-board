import pygame
import pymunk
import pymunk.pygame_util

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

# 初始化 Pygame 和 pymunk
pygame.init()
WIDTH, HEIGHT = 1400 ,1600 
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)  # 設定重力加速度

LEFT = 50
RIGHT = 1350
TOP = 150
BOTTOM = 1500
CIRCLE_BOTTOM = 1000
CIRCLE_TOP = 250
LINE_WIDTH = 10
BALL_SIZE = 10
CIRCLE_SIZE = 10

# 創建邊界
def create_boundaries(space):
    static_lines = [
        pymunk.Segment(space.static_body, (LEFT, BOTTOM), (RIGHT, BOTTOM), LINE_WIDTH),
        pymunk.Segment(space.static_body, (LEFT, TOP), (LEFT, BOTTOM), LINE_WIDTH),
        pymunk.Segment(space.static_body, (RIGHT, TOP), (RIGHT, BOTTOM), LINE_WIDTH),
    ]
    for line in static_lines:
        line.elasticity = 0.2
        space.add(line)
def create_circles(space,xl,xr,yu,yd,dist):
    mid = (xl + xr) // 2
    k = 0
    while yu+k*dist < yd:
        y = yu + k*dist
        if k&1:
            for x in range(mid,xr,dist):
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (x, y)
                shape = pymunk.Circle(body, CIRCLE_SIZE)
                shape.elasticity = 0.6
                space.add(body, shape)
            for x in range(mid-dist,xl,-dist):
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (x, y)
                shape = pymunk.Circle(body, CIRCLE_SIZE)
                shape.elasticity = 0.6
                space.add(body, shape)
        else:
            for x in range(mid+dist//2,xr,dist):
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (x, y)
                shape = pymunk.Circle(body, CIRCLE_SIZE)
                shape.elasticity = 0.6
                space.add(body, shape)
            for x in range(mid-dist//2,xl,-dist):
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (x, y)
                shape = pymunk.Circle(body, CIRCLE_SIZE)
                shape.elasticity = 0.6
                space.add(body, shape)
        k += 1
def create_funnel(space,yu,yd,input_size):
    mid = (LEFT + RIGHT) // 2
    static_lines = [
        pymunk.Segment(space.static_body, (LEFT, yu), (mid-input_size//2, yd), LINE_WIDTH),
        pymunk.Segment(space.static_body, (RIGHT, yu), (mid+input_size//2, yd), LINE_WIDTH),
    ]
    for line in static_lines:
        line.elasticity = 0.2
        space.add(line)
def create_column(space,yu,num):
    for i in range(num):
        x = (LEFT*(i+1)+RIGHT*(num-i-1))//num
        line = pymunk.Segment(space.static_body, (x, yu), (x, BOTTOM), LINE_WIDTH)
        line.elasticity = 0.2
        space.add(line)

create_boundaries(space)
create_circles(space,LEFT,RIGHT,CIRCLE_TOP,CIRCLE_BOTTOM,50)
create_funnel(space,0,CIRCLE_TOP-30,50)
create_column(space,CIRCLE_BOTTOM+30,20)

# 創建球
def create_ball(space, position):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 10))
    body.position = position
    shape = pymunk.Circle(body, 10)
    shape.elasticity = 0.6
    space.add(body, shape)
    return shape

balls = []

# 主循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        balls.append(create_ball(space, pygame.mouse.get_pos()))

    screen.fill((255, 255, 255))
    space.step(1/50.0)

    # 繪製球
    for ball in balls:
        pygame.draw.circle(screen, (0, 0, 255), (int(ball.body.position.x), int(ball.body.position.y)), BALL_SIZE)

    # 繪製邊界
    for obj in space.shapes:
        if isinstance(obj, pymunk.Segment):
            pygame.draw.line(screen, (0, 0, 0), obj.a, obj.b, LINE_WIDTH)
        if isinstance(obj, pymunk.Circle) and not obj in balls:
            pygame.draw.circle(screen, (255, 0, 0), (int(obj.body.position.x), int(obj.body.position.y)), CIRCLE_SIZE)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
