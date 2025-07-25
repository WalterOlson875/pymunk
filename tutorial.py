from webbrowser import MacOSXOSAScript
import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

width, height = 1600, 900
screen = pygame.display.set_mode((width, height))

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1],p2[0] - p1[0])


pygame.display.set_caption("Pymunk Physics")

def render(space, window, draw_options, line):
    window.fill("aquamarine")
    

    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)

    space.debug_draw(draw_options)
    
    pygame.display.update()

def create_boundaries(space, width, height, elasticity = 0.4, friction = 0.5):
    rects = [
        [(width/2, height - 10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)]
    ]
     

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def create_structure(space, width, height):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(800, height - 120), (40, 200), BROWN, 100],
        [(1100, height - 120), (40, 200), BROWN, 100],
        [(950, height - 240), (340, 40), BROWN, 150]
    ]

    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size ,radius = 2)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)

def create_swinging_ball(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (500, 350)

    body = pymunk.Body()
    body.position = (355, 255)
    line = pymunk.Segment(body, (0, 0), (255, 0), 5)
    circle = pymunk.Circle(body, 40, (255, 0))
    line.friction = 0.4
    circle.friction = 0.4
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.95
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(body, line, circle, rotation_center_joint)
    return body, circle, line

def create_ball(space, radius, mass, pressed_pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pressed_pos
    shape = pymunk.Circle(body, radius = 35)
    shape.mass = mass
    shape.elasticity = 0.95
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 120
    dt = 1 / fps
    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundaries(space, width, height)
    create_structure(space, width, height)
    create_swinging_ball(space)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None

    while run:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None
                    


        render(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    run(screen, width, height)
