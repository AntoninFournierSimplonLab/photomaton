#!/usr/bin/env python2.7

# coding=utf-8



# on importe les modules necessaires

import time

import os

import RPi.GPIO as GPIO



# on met RPi.GPIO en mode notation BCM (numero des pins)

GPIO.setmode(GPIO.BCM)



# on initialise le GPIO 23 en mode ecoute

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# on definit notre fonction qui sera appelee quand on appuiera sur le bouton

def extinction(channel):

# on affiche un petit message pour confirmer

print("Appui détecté sur le GPIO 21")

# on reinitialise les GPIO

GPIO.cleanup()

# on lance la commande d extinction
os.system('sudo halt')

# on met le bouton en ecoute
GPIO.add_event_detect(21, GPIO.FALLING, callback=extinction)

# on lance une boucle infinie, pour garder le script actif
while 1:

# une petite pause entre chaque boucle, afin de réduire la charge sur le C$
time.sleep(0.02)

# on reinitialise les ports GPIO en sortie de script
GPIO.cleanup()

