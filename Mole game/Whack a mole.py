import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Display
WIDTH = 800
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack a Diglett")
clock = pygame.time.Clock()

# Colours - RGB
BG_COLOUR = (245, 242, 230)
PANEL_COLOUR = (255, 255, 255)
PRIMARY = (60, 120, 200)
PRIMARY_HOVER = (40, 100, 180)
DANGER = (200, 70, 70)
TEXT_COLOUR = (30, 30, 30)

# Images
diglett_img = pygame.transform.scale(pygame.image.load("diglett.png"), (75, 69))
dugtrio_img = pygame.transform.scale(pygame.image.load("dugtrio.png"), (75, 69))
geodude_img = pygame.transform.scale(pygame.image.load("geodude.png"), (187, 72))

# Sounds
hit_sound = pygame.mixer.Sound("hit.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Fonts
def font(size):
    return pygame.font.Font("freesansbold.ttf", size)

############################################
# Button Class
############################################
class Button:
    # Constructor
    def __init__(self, text, x, y, w, h, colour, hover_colour, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.action = action

    # Draw the button
    def draw(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, self.hover_colour, self.rect, border_radius=8)
        else:
            pygame.draw.rect(screen, self.colour, self.rect, border_radius=8)

        text_surface = font(28).render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # This function is responsible for handling button clicks. If the button is clicked, it will execute the assigned action.
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

############################################
# Main Menu
############################################
def main_menu():

    # Create buttons
    btn15 = Button("15 Seconds", 275, 320, 250, 55, PRIMARY, PRIMARY_HOVER, lambda: game_loop(15))
    btn30 = Button("30 Seconds", 275, 390, 250, 55, PRIMARY, PRIMARY_HOVER, lambda: game_loop(30))
    btn60 = Button("60 Seconds", 275, 460, 250, 55, PRIMARY, PRIMARY_HOVER, lambda: game_loop(60))
    btnQuit = Button("Quit", 275, 530, 250, 55, DANGER, (170,50,50), quit_game)

    # While True the main menu will run until the user clicks a button or closes the window
    while True:
        screen.fill(BG_COLOUR)

        # Draw panel
        pygame.draw.rect(screen, PANEL_COLOUR, (150,150,500,500), border_radius=15)

        # Draw title and subtitle
        title = font(50).render("Whack a Diglett", True, TEXT_COLOUR)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 220)))

        subtitle = font(22).render("Choose Game Duration", True, TEXT_COLOUR)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, 270)))

        # Draw buttons
        btn15.draw()
        btn30.draw()
        btn60.draw()
        btnQuit.draw()

        # Handle events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            # Call handle button events functions
            btn15.handle_event(event)
            btn30.handle_event(event)
            btn60.handle_event(event)
            btnQuit.handle_event(event)

        pygame.display.update()
        clock.tick(60)

############################################
# Game Loop
############################################
def game_loop(duration):

    # Initialize variables
    score = 0
    start_time = time.time()

    w, h = 90, 90

    # Randomly generate the initial position of the diglett
    x = random.randint(0, WIDTH - diglett_img.get_width())
    y = random.randint(150, HEIGHT - diglett_img.get_height())

    # Randomly generate the initial position of the dugtrio
    a = random.randint(0, WIDTH - dugtrio_img.get_width())
    b = random.randint(150, HEIGHT - dugtrio_img.get_height())

    # Randomly generate the initial position of the geodude
    g_x = random.randint(0, WIDTH - geodude_img.get_width())
    g_y = random.randint(150, HEIGHT - geodude_img.get_height())

    dugtrio_visible = False
    geodude_visible = False
    dugtrio_timer = 0
    geodude_timer = 0

    running = True

    # The game loop will run until the time runs out or the user closes the window
    while running:
        screen.fill(BG_COLOUR)

        # Calculate seconds left
        seconds_left = duration - int(time.time() - start_time)
        if seconds_left <= 0:
            running = False

        # Get mouse position
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            # Check for mouse clicks and if the click is on the diglett, dugtrio or geodude
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                diglett_rect = diglett_img.get_rect(topleft=(x, y))
                dugtrio_rect = dugtrio_img.get_rect(topleft=(a, b))
                geodude_rect = geodude_img.get_rect(topleft=(g_x, g_y))

                # Diglett
                if diglett_rect.collidepoint(mouse_pos):
                    score += 1
                    hit_sound.play()
                    x = random.randint(0, WIDTH - diglett_img.get_width())
                    y = random.randint(150, HEIGHT - diglett_img.get_height())

                # Dugtrio
                if dugtrio_visible and dugtrio_rect.collidepoint(mouse_pos):
                    score += 3
                    hit_sound.play()
                    dugtrio_visible = False

                # Geodude
                if geodude_visible and geodude_rect.collidepoint(mouse_pos):
                    score -= 5
                    wrong_sound.play()
                    geodude_visible = False

        # Randomly decide when to show the dugtrio and geodude, and for how long they will be visible
        if not dugtrio_visible and random.randint(1, 250) == 1:
            dugtrio_visible = True
            dugtrio_timer = pygame.time.get_ticks()
            a = random.randint(0, WIDTH-w)
            b = random.randint(150, HEIGHT-h)

        if not geodude_visible and random.randint(1, 180) == 1:
            geodude_visible = True
            geodude_timer = pygame.time.get_ticks()
            g_x = random.randint(0, WIDTH-w)
            g_y = random.randint(150, HEIGHT-h)

        # Check if the dugtrio and geodude should still be visible, and if so, draw them on the screen
        if dugtrio_visible:
            if pygame.time.get_ticks() - dugtrio_timer > 1500:
                dugtrio_visible = False
            else:
                screen.blit(dugtrio_img, (a,b))

        if geodude_visible:
            if pygame.time.get_ticks() - geodude_timer > 1500:
                geodude_visible = False
            else:
                screen.blit(geodude_img, (g_x,g_y))

        screen.blit(diglett_img, (x,y))

        # Top Info Bar
        pygame.draw.rect(screen, PANEL_COLOUR, (0,0,WIDTH,100))
        screen.blit(font(30).render(f"Score: {score}", True, TEXT_COLOUR), (40,35))
        screen.blit(font(30).render(f"Time: {seconds_left}", True, TEXT_COLOUR), (650,35))

        pygame.display.update()
        clock.tick(60)

    # After the game loop ends, we call the game_over function and pass the final score as an argument
    game_over(score)

############################################
# Game Over
############################################
def game_over(score):
    # Play game over sound
    game_over_sound.play()

    # Create a button to return to the main menu
    btnMenu = Button("Main Menu", 300, 380, 200, 55, PRIMARY, PRIMARY_HOVER, main_menu)

    while True:
        screen.fill(BG_COLOUR)

        pygame.draw.rect(screen, PANEL_COLOUR, (200,200,400,300), border_radius=15)

        # Display "Game Over" and the final score 
        screen.blit(font(60).render("Game Over", True, TEXT_COLOUR), (260,240))
        screen.blit(font(35).render(f"Final Score: {score}", True, TEXT_COLOUR), (300,320))

        btnMenu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            btnMenu.handle_event(event)

        pygame.display.update()
        clock.tick(60)

############################################
def quit_game():
    pygame.quit()
    quit()

############################################
main_menu()
