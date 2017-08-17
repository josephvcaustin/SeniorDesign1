import sys, pygame
from time import sleep

pygame.init()
size = width, height = 1100, 510
grey = 50, 50, 50
green = 0, 255, 0
screen = pygame.display.set_mode(size)
screen.fill(grey)
pygame.display.set_caption('Testing Interface')

pygame.display.flip()

pygame.joystick.init()
#joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

xbox = pygame.joystick.Joystick(0)
xbox.init()

LEFTSTICK_X = 0
RIGHT_TRIGGER = 5
LEFT_TRIGGER = 2
B = 1

quitting = False

DEADZONE = 0.3

while True: # Grab an event from the queue and process

    sleep(1)
    event = pygame.event.poll()  
    if event.type == pygame.QUIT:
        quitting = True

    lsx_val = xbox.get_axis(LEFTSTICK_X)
    rt_val = xbox.get_axis(RIGHT_TRIGGER)
    lt_val = xbox.get_axis(LEFT_TRIGGER)

    b_pressed = xbox.get_button(B)

    print(lsx_val)
    print(rt_val)
    print(lt_val)
    print(b_pressed)

    if quitting:
        pygame.display.quit()
        break
