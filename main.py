
import pygame
import pymunk
import pymunk.pygame_util

# 初始化 Pygame 和 pymunk
pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)  # 設定重力加速度

# 創建邊界
def create_boundaries(space):
    static_lines = [
        pymunk.Segment(space.static_body, (50, 700), (550, 700), 5),
        pymunk.Segment(space.static_body, (50, 100), (50, 700), 5),
        pymunk.Segment(space.static_body, (550, 100), (550, 700), 5)
    ]
    for line in static_lines:
        line.elasticity = 0.95
        space.add(line)

create_boundaries(space)

# 創建球
def create_ball(space, position):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 10))
    body.position = position
    shape = pymunk.Circle(body, 10)
    shape.elasticity = 0.9
    space.add(body, shape)
    return shape

balls = []

# 主循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(create_ball(space, pygame.mouse.get_pos()))

    screen.fill((255, 255, 255))
    space.step(1/50.0)

    # 繪製球
    for ball in balls:
        pygame.draw.circle(screen, (0, 0, 255), (int(ball.body.position.x), int(ball.body.position.y)), 10)

    # 繪製邊界
    for line in space.shapes:
        if isinstance(line, pymunk.Segment):
            pygame.draw.line(screen, (0, 0, 0), line.a, line.b, 5)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
