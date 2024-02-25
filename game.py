import pygame
import time
import threading
from light_control import *

controller = TrafficIntersectionController()
switch_interval = 3

def updateLights():
    while True:
        current_state = controller.get_current_state()
        new_state = current_state % 4 + 1

        time.sleep(switch_interval)
        controller.switch_state(new_state)


pygame.init()

thread2 = threading.Thread(name="updateLights",target=updateLights, args=())
thread2.daemon = True
thread2.start()

# Set up the drawing window
screen = pygame.display.set_mode([800, 800])

background_image = pygame.image.load('images/intersection.png')

# Resize intersection image
background = pygame.transform.scale(background_image, (800,800))

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background,(0,0))
    screen.blit(pygame.transform.rotate(controller.ts1.image, 180), (335, 50))
    screen.blit(pygame.transform.rotate(controller.ts2.image, 90), (650, 335))
    screen.blit(controller.ts3.image, (410, 650))
    screen.blit(pygame.transform.rotate(controller.ts4.image, 270), (50, 400))    

    pygame.display.update()

# Done! Time to quit.
pygame.quit()

