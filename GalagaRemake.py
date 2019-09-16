# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 12:46:38 2019

@author: evan
"""
from graphics import *
from pygame import *
#import Random_bubbles_Intro as RBI
import pygame as pg
import random as ran
#initialize game functions
pg.init()
#Define some colors
neonRed=[255, 71, 71]
black=[0,0,0]
neonBlue=[0, 195, 255]
white=[255,255,255]
#open your display Window
size=[900,900]
gameDisplay= pg.display.set_mode(size)
#piskel website
#give window a name
pg.display.set_caption('Galaga')
pg.mixer.init()
pg.mixer.music.load('muse.mp3')
#Loop for window till closed create a variable, Loop till true
done=False

#create timer to manage  screen updates
refresher= pg.time.Clock()
star_background=pg.image.load('background.JPG')
# Galaga Ship 
class HeroShip(pg.sprite.Sprite):
    #include where it will start x and y
    image=None
    def __init__(self,location):
       #sprite constructor
       #self allows us to call attributes outside of a class well be able to move the image
        super().__init__()
        if HeroShip.image is None:
           #first time calling class
           HeroShip.image=pg.image.load('falcon2.JPG')
        self.image= HeroShip.image
        self.rect=self.image.get_rect()
        self.rect.topleft=location
        self.shipSpeed=8

#projectiles        
class Missle(pg.sprite.Sprite):
    def __init__(self,location):
        super().__init__()
        self.msound=pg.mixer.Sound('las.wav')
        self.image=pg.Surface((10,30))
        self.image.fill(neonBlue)
        self.rect=self.image.get_rect()
        self.movingSpeed=-14
        self.rect.topleft=location
    
class EnemyMissle(pg.sprite.Sprite):
    def __init__(self,location):
        super().__init__()
        self.msound=pg.mixer.Sound('las.wav')
        self.image=pg.Surface((10,30))
        self.image.fill(neonRed)
        self.rect=self.image.get_rect()
        self.movingSpeed=14
        self.rect.topleft=location    
#------bouncing Enemy--------
class GalagaEnemy(pg.sprite.Sprite):
    #include where it will start x and y
    image=None
    def __init__(self,location):
       #sprite constructor
       #self allows us to call attributes outside of a class well be able to move the image
        super().__init__()
        if GalagaEnemy.image is None:
           #first time calling class
           GalagaEnemy.image=pg.image.load('big-Tie.JPG')
        self.limit=location[0]+150
        self.image= GalagaEnemy.image
        
        self.rect=self.image.get_rect()
        self.rect.topleft=location
        self.movingSpeed=5
        
    def drawImage(self,screen):
        screen.blit(self.image,self.rect)
# initalizing with starting point top left
z=0
#first row
sprite_group=pg.sprite.Group()
for x in range(6):
    enemy=GalagaEnemy((z,0))
    sprite_group.add(enemy)
    z+=150
# second row
d=50
for x in range(6):
    enemy=GalagaEnemy((d,100))
    sprite_group.add(enemy)
    d+=130
Ship=HeroShip((430,610))

#for missle sprite group
missle_group=pg.sprite.Group()
enemy_missle_group=sprite.Group()
#initializing some important values
score=0
shot_counter=0
shot_recharge=0
enemy_shot_recharge=30
pg.mixer.music.play(10,0.50)
#----main game Loop---------
# the not returns true if the expression is false
while done==False:
    for event in pg.event.get(): #check if user did something
        if event.type==pg.QUIT: # if user clicked quit
            done=True
         
 #--------game logic here---------
    #moving in the x direction back and forth switch directions
    enemy_shot_recharge+=1
    enemylist=0
    #bounds checking ships
    for spri in sprite_group:
        if (spri.rect.x+50)>spri.limit:
            spri.movingSpeed*=-1
        if (spri.rect.x)<(spri.limit-150):
            spri.movingSpeed*=-1  
        spri.rect.x+=spri.movingSpeed
        enemylist+=1
     
   # enemy fireback every two seconds or so  and kepping in this loop takes random sprite when time is right
    if enemy_shot_recharge>30:
        spri=ran.choice(sprite_group.sprites())
        enemy_shot_recharge=0
        em=EnemyMissle(((spri.rect.x+45),spri.rect.y))
        enemy_missle_group.add(em)
        missle.msound.play()
       
        
    if pg.key.get_pressed()[pg.K_RIGHT]==True:
        Ship.rect.x+=Ship.shipSpeed
    if pg.key.get_pressed()[pg.K_LEFT]==True:
        Ship.rect.x-=Ship.shipSpeed
    #now were checking for missle launches
    # making this semi-Auto so player cant just hold on space bar
    if pg.key.get_pressed()[pg.K_SPACE]==False:
        shot_recharge+=1
    if pg.key.get_pressed()[pg.K_SPACE]==True:
        shot_counter+=1
        if (shot_counter>2) and (shot_recharge>2) :
            missle=Missle(((Ship.rect.x+127),Ship.rect.y))
            missle_group.add(missle)
            missle.msound.play()
            shot_counter=0
            shot_recharge=0
     # player missle movement
    for shots in missle_group:
        if shots.rect.y<0:
            missle_group.remove(shots)
        shots.rect.y+=shots.movingSpeed
     # enemy missle movement
    for emshot in enemy_missle_group:
         if emshot.rect.y>750:
             enemy_missle_group.remove(emshot)
         emshot.rect.y+=emshot.movingSpeed
  # --- Screen-clearing code goes here
 # can place background image this background is being refreshed 
    gameDisplay.blit(star_background,(0,0))
    #this collision requires a sprite and a group
   
        
    # --- Drawing code should go here
    #loops through my sprite group and draws the ones still alive
    hit_list= pg.sprite.groupcollide(missle_group,sprite_group,True,True)
    
    #loop through group and count number of  which is my score
    
    #checking to see if Game Over
    if pg.sprite.spritecollide(Ship,enemy_missle_group,True):
        print("Game Over")
        done=True
    for hits in hit_list:
        score+=1
        print(score)
    if score==12:
        done=True
        
    missle_group.draw(gameDisplay)
    enemy_missle_group.draw(gameDisplay)
    for spri in sprite_group:
        spri.drawImage(gameDisplay)
    #gameDisplay.blit(enemy.image,enemy.rect)
    gameDisplay.blit(Ship.image,Ship.rect)
    #Ship.Missles.draw(((Ship.rect.x-100),Ship.rect.y))
    # --- Go ahead and update the screen with what we've drawn.
    pg.display.flip()       
               
 
    #fps-usually games are 30fps
    refresher.tick(20)
  
#close window and quit
pg.quit()