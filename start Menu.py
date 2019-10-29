import pygame
from button import Button

# Game Initialization
pygame.init()

# Game Resolution


def main_menu():
    menu = True
    screen_width = 800
    screen_height = 600
    background = pygame.image.load('backround.png')
    banner = pygame.image.load('banner.png')
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.blit(background, (0, 0))
    screen.blit(banner, (100, 100))

    def draw_screen():
        screen.blit(background, (0, 0))
        screen.blit(banner, (100, 100))

    def redrawWindow():
        play_button.draw(screen, (0, 0, 0))
        levelEditor.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))

    # Text Renderer
    # def text_format(message, textFont, textSize, textColor):
    #     newFont = pygame.font.Font(textFont, textSize)
    #     newText = newFont.render(message, 0, textColor)
    #
    #     return newText

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (50, 50, 50)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    # Make the buttons.
    play_button = Button(black, 200, 300, 300, 50, "1 Player Game")
    levelEditor = Button(black, 200, 360, 300, 50, "Level Editor")
    quit_button = Button(black, 200, 420, 300, 50, "Exit Game")

    selection = 0

    while menu:
        redrawWindow()
        pygame.display.update()
        #pygame.time.delay(2)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            #click button with mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.isOver(pos):
                    #start_game = True
                    print('Clicked start Button')
                elif levelEditor.isOver(pos):
                    print('Clicked level editor button')
                elif quit_button.isOver(pos):
                    pygame.quit()
                    quit()

            #select buttons with enter
            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN]:
                if selection == 2:
                    print(selection)
                else:
                    selection = selection + 1
            if keys[pygame.K_UP]:
                if selection == 0 or selection < 0:
                    print(selection)
                else:
                    selection = selection - 1
            if keys[pygame.K_RETURN]:
                if selection == 0:
                    print('selected Start Button')
                elif selection == 1:
                    print('selected level editor')
                elif selection == 2:
                    pygame.quit()
                    quit()
                    print("selected exit game")


            #draw mushroom over hovered button
            if event.type == pygame.MOUSEMOTION:
                if play_button.isOver(pos):
                    mushroom = pygame.image.load('mushroom.png')
                    screen.blit(mushroom, (145, 300))
                elif levelEditor.isOver(pos):
                    mushroom = pygame.image.load('mushroom.png')
                    screen.blit(mushroom, (145, 360))
                elif quit_button.isOver(pos):
                    mushroom = pygame.image.load('mushroom.png')
                    screen.blit(mushroom, (145, 420))
                else:
                    redrawWindow()
                    draw_screen()


            #select buttons with arrow keys
            if selection == 0:
                mushroom = pygame.image.load('mushroom.png')
                screen.blit(mushroom, (145, 300))
            if selection == 1:
                redrawWindow()
                draw_screen()
                mushroom = pygame.image.load('mushroom.png')
                screen.blit(mushroom, (145, 360))
            if selection == 2:
                redrawWindow()
                draw_screen()
                mushroom = pygame.image.load('mushroom.png')
                screen.blit(mushroom, (145, 420))




running = True
while running:
    main_menu()





