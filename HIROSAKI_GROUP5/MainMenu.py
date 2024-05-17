import pygame
import onlyButton
import subprocess
import sys
from pygame import mixer


pygame.init()
#------game window------

screen= pygame.display.set_mode((800,500))
#--------------------------------------------TITLE------------------------------------
pygame.display.set_caption("HIROSAKI")
icon = pygame.image.load("Hirosaki files/HIROSAKI_2.jpg")
pygame.display.set_icon(icon)

#-------------------------BACKGROUND----------------------------------------
background=pygame.image.load("Hirosaki files/ILOVEYOU.jpg")
background = pygame.transform.scale(background, (800, 500))

mixer.music.load('Hirosaki files/MAINMENUSOUND.mp3')
mixer.music.play(-1)

#----------------------button image----------------------------------------
start_img=pygame.image.load('Hirosaki files/START1.png').convert_alpha()
exit_img=pygame.image.load("Hirosaki files/EXIT1.png").convert_alpha()


#create the button              x & y location
start_button=onlyButton.Button(230,320,start_img,.9)
exit_button=onlyButton.Button(480,320,exit_img,.9)

def open_main_file():
    subprocess.Popen([sys.executable, "HIROSAKI_GROUP5/game.py"])
    pygame.quit()
    sys.exit()


#GAME LOOP
run = True
while run:
    
    screen.blit(background, (0,0))

    if start_button.draw(screen):
        open_main_file()  
    if exit_button.draw(screen):
        run=False


    #--------------------------------EVENT HANDLER---------------------------------
    for event in pygame.event.get():
        if event.type ==pygame. QUIT:
            run= False


    pygame.display.update()

pygame.quit()