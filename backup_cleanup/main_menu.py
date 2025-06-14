import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Title")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define fonts
FONT_NAME = pygame.font.match_font('arial')
FONT_SIZE = 36
font = pygame.font.Font(FONT_NAME, FONT_SIZE)

# Define menu options
menu_options = ["Start Game", "Settings", "Update", "Quit"]
selected_option = 0

def draw_menu():
    screen.fill(WHITE)
    for i, option in enumerate(menu_options):
        if i == selected_option:
            label = font.render(option, True, GREEN)
        else:
            label = font.render(option, True, BLACK)
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2 + i * 40))

def main_menu_loop():
    global selected_option
    show_updates = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if show_updates and event.key == pygame.K_ESCAPE:
                    show_updates = False
                elif not show_updates:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if menu_options[selected_option] == "Update":
                            show_updates = True
                        # Add handling for other options like "Start Game", "Settings", and "Quit" here

        if show_updates:
            from updates_screen import draw_updates_screen
            draw_updates_screen(screen)
        else:
            draw_menu()
        pygame.display.flip()

# Start the main menu loop
main_menu_loop()