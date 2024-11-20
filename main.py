import pygame
import pymunk
import pymunk.pygame_util

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

# 初始化 Pygame 和 pymunk
pygame.init()
WIDTH, HEIGHT = 1400 ,1800
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)  # 設定重力加速度

LEFT = 50
RIGHT = 1350
TOP = 150
BOTTOM = HEIGHT-50
CIRCLE_BOTTOM = 1100
CIRCLE_TOP = 300
LINE_WIDTH = 10
BALL_SIZE = 20
CIRCLE_SIZE = 10
PLAYER_SIZE = 200
PROFESSOR1_IMAGE_PATH = "image/professor1.png"
PROFESSOR2_IMAGE_PATH = "image/professor2.png"
PROFESSOR1_IMAGE = pygame.image.load(PROFESSOR1_IMAGE_PATH)
PROFESSOR1_IMAGE = pygame.transform.scale(PROFESSOR1_IMAGE, (PLAYER_SIZE, PLAYER_SIZE))
PROFESSOR2_IMAGE = pygame.image.load(PROFESSOR2_IMAGE_PATH)
PROFESSOR2_IMAGE = pygame.transform.scale(PROFESSOR2_IMAGE, (PLAYER_SIZE*1.079, PLAYER_SIZE))
APPLE_IMAGE_PATH = "image/apple.png"
APPLE_IMAGE = pygame.image.load(APPLE_IMAGE_PATH)
APPLE_IMAGE = pygame.transform.scale(APPLE_IMAGE, (BALL_SIZE*2, BALL_SIZE*2*1.246))
VOICE_PATH = "voice/throw_apple.wav"
pygame.mixer.init()
THROW_BALL = pygame.mixer.Sound(VOICE_PATH)

class Player:
    def __init__(self,):
        self.throw = False
        self.x = WIDTH//2
        self.y = 10
    def update(self):
        if self.throw:
            balls.append(create_ball(space, (self.x+20, self.y+180)))
            screen.blit(PROFESSOR2_IMAGE, (self.x, self.y))
            self.throw = False
        else:
            screen.blit(PROFESSOR1_IMAGE, (self.x+PLAYER_SIZE*0.079, self.y))
    def move_right(self):
        self.x = min(self.x+10,WIDTH-PLAYER_SIZE-200)
    def move_left(self):
        self.x = max(self.x-10,330)
    def throw_ball(self):
        self.throw = True
        if not pygame.mixer.get_busy():
            THROW_BALL.play()


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
create_circles(space,LEFT,RIGHT,CIRCLE_TOP,CIRCLE_BOTTOM,65)
create_funnel(space,150,CIRCLE_TOP-30,70)
create_column(space,CIRCLE_BOTTOM+BALL_SIZE*1.8,20)

# 創建球
def create_ball(space, position):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BALL_SIZE))
    body.position = position
    shape = pymunk.Circle(body, BALL_SIZE)
    shape.elasticity = 0.6
    space.add(body, shape)
    return shape

balls = []
player = Player()

# 主循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_SPACE]:
        player.throw_ball()
    screen.fill((255, 255, 255))
    space.step(1/50.0)
    player.update()
    # 繪製球
    for ball in balls:
        screen.blit(APPLE_IMAGE, (int(ball.body.position.x-BALL_SIZE), int(ball.body.position.y-BALL_SIZE-3)))

    # 繪製邊界
    for obj in space.shapes:
        if isinstance(obj, pymunk.Segment):
            pygame.draw.line(screen, (0, 0, 0), obj.a, obj.b, LINE_WIDTH)
        if isinstance(obj, pymunk.Circle) and not obj in balls:
            pygame.draw.circle(screen, (0, 0, 255), (int(obj.body.position.x), int(obj.body.position.y)), CIRCLE_SIZE)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
