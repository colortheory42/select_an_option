import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Get screen dimensions
screen_width = 4480
screen_height = 2520

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('option selector')

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

# Set up fonts
pygame.font.init()
font = pygame.font.SysFont('Arial', 48)
description_font = pygame.font.SysFont('Arial', 120)

# Define the options
options = ["option 1", "option 2", "option 3"]
selected_option = None
dropdown_open = False

# Calculate centered positions
center_x = screen_width // 2
center_y = screen_height // 2


# Define the dimensions and positions for the text and dropdown menu
question_text = font.render("list of options", True, BLACK)
question_text_rect = question_text.get_rect(center=(center_x, center_y - 100))


dropdown_width = 400
dropdown_height = 60
dropdown_rect = pygame.Rect(center_x - dropdown_width // 2, center_y, dropdown_width, dropdown_height)
option_rects = [
    pygame.Rect(center_x - dropdown_width // 2, center_y + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
    for i in range(len(options))]

# Define the main menu buttons
start_button_rect = pygame.Rect(center_x - dropdown_width // 2, center_y, dropdown_width, dropdown_height)
exit_button_rect = pygame.Rect(center_x - dropdown_width // 2, center_y + 100, dropdown_width, dropdown_height)

# Define the pause menu buttons
resume_button_rect = pygame.Rect(center_x - dropdown_width // 2, center_y, dropdown_width, dropdown_height)
pause_exit_button_rect = pygame.Rect(center_x - dropdown_width // 2, center_y + 100, dropdown_width, dropdown_height)


# Function to display the description text
def display_description(text):
    screen.fill(WHITE)
    description_text = description_font.render(text, True, BLACK)
    description_text_rect = description_text.get_rect(center=(center_x, center_y))
    screen.blit(description_text, description_text_rect)
    pygame.display.flip()
    time.sleep(4)


# Function to display the main menu
def display_main_menu():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, start_button_rect)
    start_text = font.render("start game", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    pygame.draw.rect(screen, GRAY, exit_button_rect)
    exit_text = font.render("exit game", True, BLACK)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()


# Function to display the pause menu
def display_pause_menu():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, resume_button_rect)
    resume_text = font.render("resume", True, BLACK)
    resume_text_rect = resume_text.get_rect(center=resume_button_rect.center)
    screen.blit(resume_text, resume_text_rect)

    pygame.draw.rect(screen, GRAY, pause_exit_button_rect)
    pause_exit_text = font.render("exit game", True, BLACK)
    pause_exit_text_rect = pause_exit_text.get_rect(center=pause_exit_button_rect.center)
    screen.blit(pause_exit_text, pause_exit_text_rect)

    pygame.display.flip()



# Set up the clock for managing the frame rate
clock = pygame.time.Clock()


# Main loop
running = True
in_main_menu = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not in_main_menu:
                    paused = not paused
            if event.key == pygame.K_q:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if in_main_menu:
                if start_button_rect.collidepoint(event.pos):
                    in_main_menu = False
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
            elif paused:
                if resume_button_rect.collidepoint(event.pos):
                    paused = False
                elif pause_exit_button_rect.collidepoint(event.pos):
                    running = False
            else:
                if dropdown_rect.collidepoint(event.pos):
                    dropdown_open = not dropdown_open
                else:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos) and dropdown_open:
                            selected_option = options[i]
                            dropdown_open = False
                            # Display the description text for 4 seconds
                            display_description(f"description for {selected_option}")
                            selected_option = None  # Reset the selected option

    if in_main_menu:
        display_main_menu()
    elif paused:
        display_pause_menu()
    else:
        # Fill the screen with a color (white in this case)
        screen.fill(WHITE)

        # Render the question text
        screen.blit(question_text, question_text_rect)

        # Render the dropdown menu
        pygame.draw.rect(screen, LIGHT_GRAY if dropdown_open else GRAY, dropdown_rect)
        dropdown_text = font.render(selected_option if selected_option else "select an option", True, BLACK)
        dropdown_text_rect = dropdown_text.get_rect(center=dropdown_rect.center)
        screen.blit(dropdown_text, dropdown_text_rect)

        if dropdown_open:
            for i, rect in enumerate(option_rects):
                pygame.draw.rect(screen, LIGHT_GRAY, rect)
                option_text = font.render(options[i], True, BLACK)
                option_text_rect = option_text.get_rect(center=rect.center)
                screen.blit(option_text, option_text_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()