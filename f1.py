
import pygame
import os
import random
import time

pygame.init()

# Static variables
SIZE = (WIDTH, HEIGHT) = (1200, 800)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Formula 1")
FPS = 60
BORDERWIDTH = 20
BORDER = pygame.Rect(0, HEIGHT/2 - BORDERWIDTH/2, WIDTH, BORDERWIDTH)
UPPERMIDDLE = BORDER.y/2
LOWERMIDDLE = BORDER.y*3/2
START = 20
Y_SPEED = 5

# Colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Fonts
SCORE_FONT = pygame.font.SysFont('arial', 20)
GAME_OVER_FONT = pygame.font.SysFont('arial', 150)

# Images 
F1_RED = pygame.image.load(os.path.join('Assets', 'f1_red.png'))
F1_BLUE = pygame.image.load(os.path.join('Assets', 'f1_blue.png'))
OBSTACLE = pygame.image.load(os.path.join('Assets', 'obstacle_1.png'))

def draw_obstacles(obstacles):
    for o in obstacles:
        SCREEN.blit(OBSTACLE, (o.x, o.y))

# This is where all the visual updates are performed
def draw_screen(red, blue, red_obstacles, blue_obstacles, score):

    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, BLACK, BORDER)

    draw_obstacles(red_obstacles)
    draw_obstacles(blue_obstacles)

    SCREEN.blit(F1_RED, (red.x, red.y))
    SCREEN.blit(F1_BLUE, (blue.x, blue.y))

    text = SCORE_FONT.render(f"SCORE: {score}", 1, BLACK)
    SCREEN.blit(text, (WIDTH - text.get_width() - 5, 5))

    pygame.display.update()

def red_movement(keys_pressed, red):
        if keys_pressed[pygame.K_w] and red.y - Y_SPEED >=0:
                red.y -= Y_SPEED
        if keys_pressed[pygame.K_s] and red.y + Y_SPEED + red.height <= BORDER.y:
                red.y += Y_SPEED

def blue_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_UP] and blue.y - Y_SPEED >= BORDER.y + BORDERWIDTH:
                blue.y -= Y_SPEED
    if keys_pressed[pygame.K_DOWN] and blue.y + Y_SPEED + blue.height <= HEIGHT:
            blue.y += Y_SPEED

def obstacle_movement(red, blue, speed):
    for o in red:
        o.x -= speed
        if o.x < 0:
            o.x = WIDTH
            o.y = getRandomRedY()
    for o in blue:
        o.x -= speed
        if o.x < 0:
            o.x = WIDTH
            o.y = getRandomBlueY()

def checkCollision(red, blue, red_obstacles, blue_obstacles):
    for o in red_obstacles:
        if red.colliderect(o):
            return True

    for o in blue_obstacles:
        if blue.colliderect(o):
            return True

def getRandomBlueY():
    i = random.randint(1,3)
    return HEIGHT - 115*i

def getRandomRedY():
    i = random.randint(1,3)
    return BORDER.y - BORDERWIDTH/2 - 115*i

# main loop which runs the program
def main():

    # creates an ingame clock to set FPS in loop
    clock = pygame.time.Clock()
    score = 0
    obstacle_speed = 3

    # car hitboxes and position 
    red = pygame.Rect(START, UPPERMIDDLE, F1_RED.get_width(), F1_RED.get_height())
    blue = pygame.Rect(START, LOWERMIDDLE, F1_BLUE.get_width(), F1_BLUE.get_height())

    # Create the three red obstacles
    red_obstacles = []
    for i in range(1,4):
        x = WIDTH*2 - WIDTH/3*i
        y = getRandomRedY()  
        red_obstacles.append(pygame.Rect(x, y, OBSTACLE.get_width(), OBSTACLE.get_height()))

    # Create the three blue obstacles
    blue_obstacles = []
    for i in range(1,4):
        x = WIDTH*2 - WIDTH/3*i
        y = getRandomBlueY()        
        blue_obstacles.append(pygame.Rect(x, y, OBSTACLE.get_height(), OBSTACLE.get_height()))

    running = True
    
    while running:
        clock.tick(FPS)
        score += 1
        if score % 100 == 0:
            obstacle_speed += 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()

        if not checkCollision(red, blue, red_obstacles, blue_obstacles):
            red_movement(keys_pressed, red)
            blue_movement(keys_pressed, blue)
            obstacle_movement(red_obstacles, blue_obstacles, obstacle_speed)
            
            draw_screen(red, blue, red_obstacles, blue_obstacles, score)
        else:
            # delay 2 seconds before restarting
            text = GAME_OVER_FONT.render("GAME OVER", 1, YELLOW)
            SCREEN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()

            time.sleep(2)
            running = False
            
    main()
    
if __name__ == "__main__":
    main()