from re import S
import pygame
pygame.init()


width, height = pygame.display.get_desktop_sizes()[0]
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Pong by Walter AKA a really cool guy")

white = (255, 255, 255)
black = (0, 0, 0)

paddle_width, paddle_height = 40, 200

score_font = pygame.font.SysFont("comicsans", 100)
score_font2 = pygame.font.SysFont("comicsans", 74)
winning_score = 10

class Paddle:
    COLOR = white
    VEL = 6
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up = True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self, x, y):
        self.x += self.original_x
        self.y += self.original_y
        self.y_VEL = 0
        self.x_vel *= -1


class Ball:
    MAX_VEL = 8
    COLOR = white

    

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = 15
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
def draw(window, paddles, ball, left_score, right_score):
    window.fill(black)

    left_score_text = score_font.render(f"{left_score}", 1, white)
    right_score_text = score_font.render(f"{right_score}", 1, white)

    window.blit(left_score_text, (width//4 - left_score_text.get_width()//2, 20))
    window.blit(right_score_text, (3*width//4 - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(window)

    for i in range(10, height, height//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, white, (width//2 - 5, i, 10, height//20))

    ball.draw(window)

    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= height:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                ball.y_vel = (ball.y - (left_paddle.y + left_paddle.height/2)) / (left_paddle.height/2) * ball.MAX_VEL

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                ball.y_vel = (ball.y - (right_paddle.y + right_paddle.height/2)) / (right_paddle.height/2) * ball.MAX_VEL
                
                

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up = True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= height:
        left_paddle.move(up = False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up = True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= height:
        right_paddle.move(up = False)
   

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, height//2 - paddle_height//2, paddle_width, paddle_height)
    right_paddle = Paddle(width - 10 - paddle_width, height//2 - paddle_height//2, paddle_width, paddle_height)

    ball = Ball(width//2, height//2, 7)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(120)
        draw(window, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball = Ball(width//2, height//2, 7)
        elif ball.x > width:
            left_score += 1
            ball = Ball(width//2, height//2, 7)
            ball.x_vel *= -1

        if left_score >= winning_score:
            win_text = score_font2.render(f"Left Player Won! Right Player Sucks!", 1, white)
            window.blit(win_text, (width//2 - win_text.get_width()//2, height//2 - win_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            left_score = 0
            right_score = 0
            ball = Ball(width//2, height//2, 7) 
        elif right_score >= winning_score:
            win_text = score_font2.render(f"Right Player Won! Left Player Sucks!", 1, white)
            window.blit(win_text, (width//2 - win_text.get_width()//2, height//2 - win_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            break


   

    pygame.quit()


if __name__ == "__main__":
    main()