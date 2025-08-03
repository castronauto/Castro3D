#  ________  ________  ________  _________  ________  ________                ________  ________     
# |\   ____\|\   __  \|\   ____\|\___   ___\\   __  \|\   __  \              |\_____  \|\   ___ \    
# \ \  \___|\ \  \|\  \ \  \___|\|___ \  \_\ \  \|\  \ \  \|\  \  ___________\|____|\ /\ \  \_|\ \   
#  \ \  \    \ \   __  \ \_____  \   \ \  \ \ \   _  _\ \  \\\  \|\____________\   \|\  \ \  \ \\ \  
#   \ \  \____\ \  \ \  \|____|\  \   \ \  \ \ \  \\  \\ \  \\\  \|____________|  __\_\  \ \  \_\\ \ 
#    \ \_______\ \__\ \__\____\_\  \   \ \__\ \ \__\\ _\\ \_______\              |\_______\ \_______\
#     \|_______|\|__|\|__|\_________\   \|__|  \|__|\|__|\|_______|              \|_______|\|_______|
#                        \|_________|                                                                
#
#---------------------------| Libraries 
import pygame
import math
import os
import json
import socket
import threading
pygame.init()


#---------------------------| CMD customization
os.system('mode con lines=5 cols=34')
print("== Castro3D ======================")
print(" ")
print("> Version 1.14")
print("> Testing")






#---------------------------| Setup & Varibles
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
center_x, center_y = width // 2, height // 2

CAMX, CAMY, CAMZ = 0.0, 0.0, -200.0
CAM_ANGLE = 0.0      
CAM_PITCH = 0.0  
CAM_ROLL = 0.0  
FOV = 250

MOVESPEED = 5
velocity = 0.0
xvelocity = 0.0
acceleration = 0

CAMY = 0 
yvel = 0

text_font = pygame.font.SysFont("Arial", 18) #IBM 3270, Press Start 2P Regular
pygame.mouse.set_visible(False)



#---------------------------| Functions / Define scripts

def apply_rotation(x, z, y, scale=1):

    # For angle ligesom man ryster på hovdet "nej"
    roty_x = x * math.cos(CAM_ANGLE) - z * math.sin(CAM_ANGLE)
    roty_z = x * math.sin(CAM_ANGLE) + z * math.cos(CAM_ANGLE)

    # For pitch ligesom når man nikker "ja"
    rotx_y = y * math.cos(CAM_PITCH) - roty_z * math.sin(CAM_PITCH)
    rotx_z = y * math.sin(CAM_PITCH) + roty_z * math.cos(CAM_PITCH)


    if rotx_z <= 0: return None  

    # Roll for den sidste akse, ligesom man tilter hovdet til skulderen
    rxr = roty_x * math.cos(CAM_ROLL) - rotx_y * math.sin(CAM_ROLL)
    ryr = roty_x * math.sin(CAM_ROLL) + rotx_y * math.cos(CAM_ROLL)
    roty_x, rotx_y = rxr, ryr

    screen_x = roty_x * FOV / rotx_z * scale
    screen_y = rotx_y * FOV / rotx_z * scale
    return screen_x, screen_y, rotx_z

def draw_box(center, length, width, height, color=(0, 0, 0)):
    cx, cy, cz = center
    hl = length / 2
    hw = width / 2
    hh = height / 2

    # Define corners of the box
    corners = [
        (cx - hl, cy - hh, cz - hw),  # 0 Bottom-front-left
        (cx + hl, cy - hh, cz - hw),  # 1 Bottom-front-right
        (cx + hl, cy - hh, cz + hw),  # 2 Bottom-back-right
        (cx - hl, cy - hh, cz + hw),  # 3 Bottom-back-left
        (cx - hl, cy + hh, cz - hw),  # 4 Top-front-left
        (cx + hl, cy + hh, cz - hw),  # 5 Top-front-right
        (cx + hl, cy + hh, cz + hw),  # 6 Top-back-right
        (cx - hl, cy + hh, cz + hw),  # 7 Top-back-left
    ]

    # Project the 3D corners to 2D screen space
    projected = []
    for x, y, z in corners:
        result = apply_rotation(x - CAMX, z - CAMZ, y - CAMY)
        projected.append(result)

    # Define box faces by corner indices
    sides = [
        (4, 5, 6, 7),  # Top
        (0, 1, 5, 4),  # Front
        (1, 2, 6, 5),  # Right
        (2, 3, 7, 6),  # Back
        (3, 0, 4, 7),  # Left
        (0, 1, 2, 3),  # Bottom
    ]
    rect_color = 20
    # Draw each face
    for side in sides:
        polygon = []
        for i in side:
            if projected[i]:
                sx, sy, _ = projected[i]
                polygon.append((int(center_x + sx), int(center_y - sy)))
        if len(polygon) == 4:
            pygame.draw.polygon(screen, color, polygon)

def text(txt, font, color, x, y):
    img = font.render(txt, True, color)
    screen.blit(img, (x, y))





#---------------------------| Run-Time
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((38, 38, 38))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()




    #-----------------------| Rotation
    if keys[pygame.K_LEFT]:
        CAM_ANGLE -= 0.03
    if keys[pygame.K_RIGHT]:
        CAM_ANGLE += 0.03

    if keys[pygame.K_UP]:
        CAM_PITCH += 0.03
    if keys[pygame.K_DOWN]:
        CAM_PITCH -= 0.03

    if keys[pygame.K_x]:
        CAM_ROLL += 0.03
    if keys[pygame.K_z]:
        CAM_ROLL -= 0.03
 




  
    #-----------------------| Movement
    if keys[pygame.K_w]: 
        acceleration += 0.2  
    if keys[pygame.K_s]: 
        acceleration -= 0.2

    CAMX += math.sin(CAM_ANGLE) * velocity
    CAMZ += math.cos(CAM_ANGLE) * velocity

    velocity += acceleration
    velocity *= 0.92
    acceleration = 0



    if keys[pygame.K_a]:  
        acceleration -= 0.2  
    if keys[pygame.K_d]: 
        acceleration += 0.2  
  
    CAMX += math.sin(CAM_ANGLE+1.5) * xvelocity
    CAMZ += math.cos(CAM_ANGLE+1.5) * xvelocity

    xvelocity += acceleration
    xvelocity *= 0.92
    acceleration = 0




 

    if keys[pygame.K_r]: 
        CAMX, CAMY, CAMZ = 0.0, 0.0, -200.0
        CAM_ANGLE = 0.0      
        CAM_PITCH = 0.0  
        CAM_ROLL = 0.0  
        FOV = 250




    #-----------------------| Gravity
    yvel += -0.2  
    CAMY += yvel

    if CAMY < 0:
        CAMY = 0
        yvel = 0
        # Jump!
        if keys[pygame.K_SPACE]:
            yvel = 3  






    #-----------------------| Draw World
    draw_box((0, -50, 0), length=40, width=40, height=20, color=(212, 89, 105))







    #-----------------------| Draw Text
    fps = int(clock.get_fps())

    text(f"{round(CAMX)}, {round(CAMZ)}, {round(CAMY)} | {round(CAM_ANGLE)}", text_font, (255, 255, 255), 15, 15)
    text(f"FPS: {fps}", text_font, (255, 255, 255), 15, 35)
    text("•", text_font, (255, 255, 255), center_x, center_y)







    #-----------------------| Mouse Rotation
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)


    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - center_x
    dy = mouse_y - center_y

    CAM_ANGLE += dx * 0.0012
    CAM_PITCH -= dy * 0.0012

    pygame.mouse.set_pos((center_x, center_y))

    if CAM_PITCH < -1.5:
        CAM_PITCH = -1.5




    #-----------------------| Finish
    pygame.display.flip()
    clock.tick(60)

pygame.quit()