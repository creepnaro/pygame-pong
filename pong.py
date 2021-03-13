import pygame, sys, random

#General Setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Pong")

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
player = pygame.Rect(screen_width - 20,screen_height/2 - 70,10,140)
opponent = pygame.Rect(10,screen_height/2 - 70,10,140)

backbground_color = (0,0,0)
light_grey = (200,200,200)

ball_speed_x = 13 *random.choice((1,-1))
ball_speed_y = 13 *random.choice((1,-1))
player_speed = 0
opponent_speed = 0
player_points = 0
opponent_points = 0

# Help for fonts: https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
# Points
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
player_point_display = myfont.render(str(player_points), False, light_grey)
opponent_point_display = myfont.render(str(opponent_points), False, light_grey)



# Game variables
def player_animation(player, opponent, player_speed, opponent_speed, screen_height):
	player.y += player_speed
	opponent.y += opponent_speed
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height
	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height
	return player, opponent, player_speed, opponent_speed, screen_height

def ball_animation(ball_speed_y, ball_speed_x):
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1
	if ball.left <= 0 or ball.right > screen_width:
		ball_speed_y, ball_speed_x = ball_restart(ball_speed_y, ball_speed_x)

	if ball.colliderect(player) or ball.colliderect(opponent):
		ball_speed_x *= -1
	return ball_speed_y, ball_speed_x

def ball_restart(ball_speed_y, ball_speed_x):
	ball.center = (screen_width/2, screen_height/2)
	ball_speed_y *= random.choice((1,-1))
	ball_speed_x *= random.choice((1,-1))
	return ball_speed_y, ball_speed_x

def movement(opponent_speed, player_speed):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed +=8.5
			if event.key == pygame.K_UP:
				player_speed -=8.5
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -=8.5
			if event.key == pygame.K_UP:
				player_speed +=8.5
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				opponent_speed +=8.5
			if event.key == pygame.K_w:
				opponent_speed -=8.5
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_s:
				opponent_speed -=8.5
			if event.key == pygame.K_w:
				opponent_speed +=8.5
	return opponent_speed, player_speed

def visuals(screen, screen_width, screen_height, light_grey, player, opponent, ball, player_point_display, opponent_point_display, background_color):
	screen.fill(background_color)
	pygame.draw.rect(screen,light_grey,player)
	pygame.draw.rect(screen,light_grey,opponent)
	pygame.draw.ellipse(screen,light_grey,ball)
	pygame.draw.aaline(screen, light_grey,(screen_width/2,0),(screen_width/2,screen_height))
	screen.blit(opponent_point_display,(350,1280))
	screen.blit(player_point_display,(360,1280))
	return screen, screen_width, screen_height, light_grey, player, opponent, ball, player_point_display, opponent_point_display, background_color

# Point Update
def points(opponent_points, player_points, screen_width, ball):
	if ball.left <= 0:
		player_points +=1
		return player_points
	if ball.right > screen_width:
		opponent_points +=1
		return opponent_points
	return  screen_width, ball, ball_speed_x, ball_speed_y

def update_window():
	pygame.display.flip()
	clock.tick(60)

# Game Loop
while True:
	opponent_speed, player_speed = movement(opponent_speed, player_speed)
	ball_speed_y, ball_speed_x = ball_animation(ball_speed_y, ball_speed_x)
	opponent_points, player_points, screen_width, ball = points(opponent_points, player_points, screen_width, ball)
	player, opponent, player_speed, opponent_speed, screen_height = player_animation(player, opponent, player_speed, opponent_speed, screen_height)
	screen, screen_width, screen_height, light_grey, player, opponent, ball, player_point_display, opponent_point_display, background_color = visuals(screen, screen_width, screen_height, light_grey, player, opponent, ball, player_point_display, opponent_point_display, background_color)
	update_window()
