import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anatha Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEOLOCITY = 5
BULLET_VEOLOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space.png")), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
	WIN.blit(BACKGROUND, (0, 0))
	pygame.draw.rect(WIN, BLACK, BORDER)

	red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
	yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
	WIN.blit(yellow_health_text, (10, 10))

	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
	WIN.blit(RED_SPACESHIP, (red.x, red.y))

	for bullet in red_bullets:
		pygame.draw.rect(WIN, RED, bullet)

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, YELLOW, bullet)

	pygame.display.update()

def yellow_spaceship_movement(keys_pressed, yellow):
	if keys_pressed[pygame.K_a] and yellow.x - VEOLOCITY > 0: # left
			yellow.x -= VEOLOCITY
	if keys_pressed[pygame.K_d] and yellow.x + VEOLOCITY + yellow.width < BORDER.x + 10: # right
			yellow.x += VEOLOCITY
	if keys_pressed[pygame.K_w] and yellow.y - VEOLOCITY > 0: # up
			yellow.y -= VEOLOCITY
	if keys_pressed[pygame.K_s] and yellow.y + VEOLOCITY + yellow.height < HEIGHT - 10: # down
			yellow.y += VEOLOCITY

def red_spaceship_movement(keys_pressed, red):
	if keys_pressed[pygame.K_LEFT] and red.x - VEOLOCITY > BORDER.x + BORDER.width: # left
			red.x -= VEOLOCITY
	if keys_pressed[pygame.K_RIGHT] and red.x + VEOLOCITY + red.width < WIDTH + 15: # right
			red.x += VEOLOCITY
	if keys_pressed[pygame.K_UP] and red.y - VEOLOCITY > 0: # up
			red.y -= VEOLOCITY
	if keys_pressed[pygame.K_DOWN] and red.y + VEOLOCITY + red.height < HEIGHT - 10: # down
			red.y += VEOLOCITY

def bullet_movement(yellow_bullets, red_bullets, yellow, red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEOLOCITY
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEOLOCITY
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)

def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
	pygame.display.update()
	pygame.time.delay(5000)

def main():
	red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
	yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

	yellow_bullets = []
	red_bullets = []

	red_health = 100
	yellow_health = 100

	winner_text = ""

	clock = pygame.time.Clock()
	run = True
	while run:

		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
					yellow_bullets.append(pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5))

				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
					red_bullets.append(pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5))

			if event.type ==RED_HIT:
				red_health -= 5

			if event.type == YELLOW_HIT:
				yellow_health -= 5

		if red_health == 0:
			winner_text = "Yellow won!"

		if yellow_health == 0:
			winner_text = "Red won!"

		if winner_text != "":
			draw_winner(winner_text)
			break

		keys_pressed = pygame.key.get_pressed()
		yellow_spaceship_movement(keys_pressed, yellow)
		red_spaceship_movement(keys_pressed, red)

		bullet_movement(yellow_bullets, red_bullets, yellow, red)

		draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

	main()

if __name__ == '__main__':
	main()