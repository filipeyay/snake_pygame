# import libs
import pygame
import time
import random

snake_speed = 15

# window size
height = 720
lenght = 480

# colors
black = pygame.Color(0, 0, 0)  # background
white = pygame.Color(255, 255, 255)  # font
red = pygame.Color(255, 0, 0)  # fruit
green = pygame.Color(0, 255, 0)  # snake

# start pygame
pygame.init()

# start window
pygame.display.set_caption("Snake Game")  # window name
window_game = pygame.display.set_mode((height, lenght))

# FPS (frames per second) control
fps = pygame.time.Clock()

# set snake initial position
snake_position = [100, 50]

# set snake body first 4 blocks
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# fruit position
fruit_position = [
    random.randrange(1, (height // 10)) * 10,
    random.randrange(1, (lenght // 10)) * 10,
]

spawn_fruit = True

# set snake start direction
direction = "RIGHT"

change_to = direction

# start score value
score = 0


# score function
def show_score(choice, color, font, size):
    # score font text
    score_font = pygame.font.SysFont(font, size)
    # show score text during gameplay
    score_render = score_font.render("Score: " + str(score), True, color)
    # draw text
    score_rec = score_render.get_rect()
    window_game.blit(score_render, score_rec)


# end game function
def endgame():
    # end game font text
    myfont = pygame.font.SysFont("times new roman", 50)

    endgame_render = myfont.render("Your score is: " + str(score), True, white)

    endgame_rec = endgame_render.get_rect()

    # text position
    endgame_rec.midtop = (height / 2, lenght / 4)

    window_game.blit(endgame_render, endgame_rec)
    pygame.display.flip()

    # after 2 seconds game window closes
    time.sleep(2)

    # exit pygame
    pygame.quit()

    # exit program
    quit()


# main function
while True:
    # game controls
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = "UP"
            if event.key == pygame.K_DOWN:
                change_to = "DOWN"
            if event.key == pygame.K_LEFT:
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                change_to = "RIGHT"

    # if two keys are pressed at the same time
    # this should prevent the snake from walking in two directions
    # at the same time
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # move snake
    if direction == "UP":
        snake_position[1] -= 10
    if direction == "DOWN":
        snake_position[1] += 10
    if direction == "LEFT":
        snake_position[0] -= 10
    if direction == "RIGHT":
        snake_position[0] += 10

    # snake growth mechanism if the fruit and the snake collide
    # the score increases by 10 points
    snake_body.insert(0, list(snake_position))
    if (
        snake_position[0] == fruit_position[0]
        and snake_position[1] == fruit_position[1]
    ):
        score += 10
        spawn_fruit = False
    else:
        snake_body.pop()

    if not spawn_fruit:
        fruit_position = [
            random.randrange(1, (height // 10)) * 10,
            random.randrange(1, (lenght // 10)) * 10,
        ]

    spawn_fruit = True
    window_game.fill(black)

    for pos in snake_body:
        pygame.draw.rect(window_game, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(
        window_game, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10)
    )

    # end game conditions
    if snake_position[0] < 0 or snake_position[0] > height - 10:
        endgame()
    if snake_position[1] < 0 or snake_position[1] > lenght - 10:
        endgame()

    # if collide with snake
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            endgame()

    # score always visible on screen
    show_score(1, white, "times new roman", 20)

    # update game screen
    pygame.display.update()

    # fps & frame rate
    fps.tick(snake_speed)
