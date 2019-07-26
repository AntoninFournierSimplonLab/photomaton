#!/usr/bin/env python2.7
# -*- coding: utf-8 -*

#import de pibooth
import RPi.GPIO as GPIO
import time
from datetime import datetime
from PIL import Image
import pygame
from pygame.locals import *
import os


#import de custo-camera
from Adafruit_Thermal import *
from PIL import Image
from picamera import PiCamera
from time import sleep





#pibooth
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
width, height = screen.get_size()

#custom-camera
printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)


#
# Prise de photo : une pour l'affichage ecran et une pour l'impression
#
def takepic(imageName): 
    #command = "sudo raspistill -t 200 -w 512 -h 384 -o "+ imageName
    #raspistill -n -t 200 -w 512 -h 384 -o - | lp
    #camera = PiCamera()
    #camera.start_preview()
    #camera.capture(imageName)
    #camera.stop_preview()
    #camera.close()

    # Prise de vue pour l'affichage ecran
    command = "sudo raspistill -t 1000 -w 512 -h 384 -o "+ imageName +" -rot 180 -q 80" #prend une photo et la tourne de 180°
    os.system(command)

#
# Affichagfe de l'image a l'ecran
#
def loadpic(imageName): # affiche imagename
    print("loading image: " + imageName)
    
    #affiche la photo 
    background = pygame.image.load(imageName);
    background.convert_alpha()
    background = pygame.transform.scale(background,(width,height))
    screen.blit(background,(0,0),(0,0,width,height))
    
    pygame.display.flip()
    
    writemessagetransparent("wait for your pic ;)")
    
    #lance l'impression
    #title = open("/home/pi/texte.txt", "r")
    #printer.println(title.read())
    #title.close()
    #img = Image.open(imageName) #mettre une variable à la place du texte fixe pour récupérer la dernière photo
    #img = img.transpose(Image.ROTATE_90)
    #printer.printImage(img, True)
    
    #printer.println()
    #printer.println()
    #printer.println()

#
# Impression sur imprimante thermique
# 
def printpict(imageName):
    #lance l'impression
    # Nom de l'evenement imprime sur les photos FIXME
    title = open("/home/pi/texte.txt", "r")
    printer.println(title.read())
    title.close()
    img = Image.open(imageName) #mettre une variable à la place du texte fixe pour récupérer la dernière photo
    img = img.transpose(Image.ROTATE_90)
    printer.printImage(img, True)
    
    printer.println()
    printer.println()
    printer.println()
    
    
#
#  Affichage d'un compte a rebours
#
def minuterie():
  writemessage("      3")
  time.sleep(1.5)
  writemessage("      2")
  time.sleep(1.5)
  writemessage("      1")
  time.sleep(1.5)

  
#
# Parametres d'affichage
#
def writemessage(message): # pour pouvoir afficher des messages sur un font noir 
    screen.fill(pygame.Color(0,0,0))
    #textrect =text.get_rect()
    #textrect.centerx = screen.get_rect().centerx
    #textrect.centery = screen.get_rect().centery
    
    font = pygame.font.SysFont("verdana", 250, bold=1)
    textsurface = font.render(message, 1, pygame.Color(255,255,255))
    screen.blit(textsurface, (25,200))
    pygame.display.update()


def writemessagetransparent(message): # pour pouvoir afficher des messages en conservant le font 
    font = pygame.font.SysFont("verdana", 50, bold=1)
    textsurface = font.render(message, 1, pygame.Color(255,255,255))
    screen.blit(textsurface,(35,40))
    pygame.display.update()
    

#def printicket(urlphoto):
#    printer.printImage(urlphoto, True)
#    print "on imprime la photo"


if (os.path.isdir("/home/pi/Desktop/photos") == False): # si le dossier pour stocker les photos n'existe pas       
   os.mkdir("/home/pi/Desktop/photos")                  # alors on crée le dossier (sur le bureau)
   os.chmod("/home/pi/Desktop/photos",0o777)            # et on change les droits pour pouvoir effacer des photos


#
# Main loop
#

while True : #boucle jusqu'a interruption
    try:
        print "\n attente boucle"
        
        #camera = PiCamera()
        #camera.start_preview()
        
        
        
        #on attend que le bouton soit pressé
        GPIO.wait_for_edge(18, GPIO.FALLING)
        
        # on a appuyé sur le bouton...
        
        


        #on lance le decompte
        minuterie()
        
        #camera.stop_preview()
        #camera.close()
        
        #on genere le nom de la photo avec heure_min_sec
        date_today = datetime.now()
        nom_image = date_today.strftime('%d_%m_%H_%M_%S')
        
        

        #on prend la photo
        chemin_photo = '/home/pi/Desktop/photos/'+nom_image+'.jpeg'
        takepic(chemin_photo) #on prend la photo 

        #on affiche la photo
        loadpic(chemin_photo)

	# on lance l'impression
        printpict(chemin_photo)
        
        #on affiche un message
        
        
     

      
        if (GPIO.input(21) == 0): 
               print("bouton  appuye, je dois sortir")
               break # alors on sort du while 
 

    except KeyboardInterrupt:
        print 'sortie du programme!'
        raise

# reinitialisation GPIO lors d'une sortie normale
GPIO.cleanup()
