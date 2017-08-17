import os, sys, pygame, serialcomm
from time import sleep

# Display Initialization
pygame.init()
size = width, height = 1020, 1100
grey = 50, 50, 50
green = 0, 255, 0
screen = pygame.display.set_mode(size)
screen.fill(grey)
pygame.display.set_caption('Testing Interface')


# Car Images
carStraight = pygame.image.load("CarStraight.bmp")
carLeft = pygame.image.load("CarLeft.bmp")
carRight = pygame.image.load("CarRight.bmp")

carSendRect = carStraight.get_rect().move(120,70)
senderLabel = pygame.font.Font(None, 100).render('SENDER', True, green, None)
senderLabelRect = senderLabel.get_rect().move(110,0)

carReceiveRect = carStraight.get_rect().move(600,70)
receiverLabel = pygame.font.Font(None, 100).render('RECEIVER', True, green, None)
receiverLabelRect = receiverLabel.get_rect().move(550,0)

screen.blit(carStraight, carSendRect)
screen.blit(senderLabel, senderLabelRect)

screen.blit(carStraight, carReceiveRect)
screen.blit(receiverLabel, receiverLabelRect)

# Xbox Images
xboxImage = pygame.image.load("xbox.png")
a = pygame.image.load("a.png")
b = pygame.image.load("b.png")
x = pygame.image.load("x.png")
y = pygame.image.load("y.png")
bk = pygame.image.load("bk.png")
gd = pygame.image.load("gd.png")
st = pygame.image.load("st.png")
lb = pygame.image.load("lb.png")
rb = pygame.image.load("rb.png")
lt = pygame.image.load("lt.png")
rt = pygame.image.load("rt.png")
lsu = pygame.image.load("lsu.png")
lsd = pygame.image.load("lsd.png")
lsr = pygame.image.load("lsr.png")
lsl = pygame.image.load("lsl.png")
rsu = pygame.image.load("rsu.png")
rsd = pygame.image.load("rsd.png")
rsl = pygame.image.load("rsl.png")
rsr = pygame.image.load("rsr.png")
du = pygame.image.load("du.png")
dd = pygame.image.load("dd.png")
dl = pygame.image.load("dl.png")
dr = pygame.image.load("dr.png")

xboxImageRect = xboxImage.get_rect().move(20, 600)
screen.blit(xboxImage, xboxImageRect)

# Initial Render

pygame.display.flip()
updateFrame = True #save a little processing power, only update if needed
quitting = False #initiated a window close event
pygame.event.set_allowed(pygame.QUIT) #only listen for a frame close event

#-----------------------------------------------------------------#

#Interpreting input

pygame.joystick.init()

xbox = pygame.joystick.Joystick(0)
xbox.init()

LEFTSTICK_X = 0
LEFTSTICK_Y = 1
RIGHTSTICK_X = 3
RIGHTSTICK_Y = 4
RIGHT_TRIGGER = 5
LEFT_TRIGGER = 2

A_BUTTON = 0
B_BUTTON = 1
X_BUTTON = 2
Y_BUTTON = 3
LBUMPER = 4
RBUMPER = 5
BACK = 6
START = 7
GUIDE = 8

# Current Values
lsx_val = 0
lsy_val = 0
rsx_val = 0
rsy_val = 0
rt_val = -1
lt_val = -1

DEADZONE = 0.2

VALUE_MIDDLE = 50

throttle = VALUE_MIDDLE #1 to 99
steerValue = VALUE_MIDDLE #1 to 99

#-----------------------------------------------------------------#    

#Serial Communication

QUERY = 1000
ACKNOWLEDGE = 1001
SEND_STEERING = 1100 #last 2 digits = value to set steering to
SEND_THROTTLE = 1200 #last 2 digits = value to set throttle to
REQUEST_CONSTANT = 1300 #Constant = max/min range, stored in consants array
REQUEST_VALUE = 1400 #value = active running value

SEND_CONSTANT = 1500
SEND_VALUE = 1600

# Values Read from Arduino

STEER_STRAIGHT = 103

throttleReadValue = 1350
steeringReadValue = 103


#-----------------------------------------------------------------#    

def updateGUI():
    if updateFrame:

        # Draw the Sender Car Image
        if(steerValue < VALUE_MIDDLE):
            screen.blit(carRight, carSendRect)
        elif(steerValue > VALUE_MIDDLE):
            screen.blit(carLeft, carSendRect)
        else: screen.blit(carStraight, carSendRect)

        # Draw the Receiver Car Image
        if(steeringReadValue > STEER_STRAIGHT):
            screen.blit(carRight, carReceiveRect)
        elif(steeringReadValue < STEER_STRAIGHT):
            screen.blit(carLeft, carReceiveRect)
        else: screen.blit(carStraight, carReceiveRect)

        # Draw the xbox controller image
        screen.blit(xboxImage, xboxImageRect)
        
        if lsx_val > 0: screen.blit(lsr, xboxImageRect)
        elif lsx_val < 0: screen.blit(lsl, xboxImageRect)
        
        if lsy_val > 0: screen.blit(lsd, xboxImageRect)
        elif lsy_val < 0: screen.blit(lsu, xboxImageRect)

        if rsx_val > 0: screen.blit(rsr, xboxImageRect)
        elif rsx_val < 0: screen.blit(rsl, xboxImageRect)

        if rsy_val > 0: screen.blit(rsd, xboxImageRect)
        elif rsy_val < 0: screen.blit(rsu, xboxImageRect)
        
        if rt_val > 0: screen.blit(rt, xboxImageRect)
        if lt_val > 0: screen.blit(lt, xboxImageRect)

        if xbox.get_button(A_BUTTON): screen.blit(a, xboxImageRect)
        if xbox.get_button(B_BUTTON): screen.blit(b, xboxImageRect)
        if xbox.get_button(X_BUTTON): screen.blit(x, xboxImageRect)
        if xbox.get_button(Y_BUTTON): screen.blit(y, xboxImageRect)

        if xbox.get_button(LBUMPER): screen.blit(lb, xboxImageRect)
        if xbox.get_button(RBUMPER): screen.blit(rb, xboxImageRect)

        if xbox.get_button(BACK): screen.blit(bk, xboxImageRect)
        if xbox.get_button(GUIDE): screen.blit(gd, xboxImageRect)
        if xbox.get_button(START): screen.blit(st, xboxImageRect)
        
        pygame.display.flip() #update the frame   

#-----------------------------------------------------------------#

comms = serialcomm.SerialTalker()
if comms.initialized: print("Established communication with the Arduino.")
else: print("Failed to establish communication with the Arduino.") 

while True: # Grab an event from the queue and process
    
    event = pygame.event.poll()
    #sleep(0.5)
    if event.type == pygame.QUIT:
        quitting = True

    if abs(xbox.get_axis(LEFTSTICK_X)) > DEADZONE:
        lsx_val = xbox.get_axis(LEFTSTICK_X)
    else : lsx_val = 0
    if abs(xbox.get_axis(LEFTSTICK_Y)) > DEADZONE:
        lsy_val = xbox.get_axis(LEFTSTICK_Y)
    else : lsy_val = 0
    
    if abs(xbox.get_axis(RIGHTSTICK_X)) > DEADZONE:
        rsx_val = xbox.get_axis(RIGHTSTICK_X)
    else : rsx_val = 0
    if abs(xbox.get_axis(RIGHTSTICK_Y)) > DEADZONE:
        rsy_val = xbox.get_axis(RIGHTSTICK_Y)
    else : rsy_val = 0
    
    steerValue = VALUE_MIDDLE - int(lsx_val*(VALUE_MIDDLE-1)) #1 to 99, 50 = straight, 1 = right, 99 = left

    rt_val = (xbox.get_axis(RIGHT_TRIGGER) + 1.0)/2 #Read values as 0 to 1 instead of -1 to 1
    lt_val = (xbox.get_axis(LEFT_TRIGGER) + 1.0)/2 
    throttle = int((VALUE_MIDDLE)+(VALUE_MIDDLE-1)*(rt_val-lt_val)) #1 to 99, stop = 50
    
    if xbox.get_button(B_BUTTON): throttle = 0

    if comms.initialized:
        throttleReadValue = comms.send(SEND_THROTTLE + throttle) #Send throttle, arduino sends its throttle value back
        steeringReadValue = comms.send(SEND_STEERING + steeringValue) #Send steering, arduino sends its steering value back

    updateGUI()
    
    if quitting:
        pygame.display.quit()
        break
