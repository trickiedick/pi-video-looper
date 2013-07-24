#!/usr/bin/env python
# -*- coding: utf-8 -*-



# imports
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time
import piface.pfio

# constants & decs

# PLAYER 1
movie_path = '/media/usb0/white_screen_1.mp4'
picture_path = '/media/usb0/*.jpg'
halting=0
stopping=0
goplay=0
led0 = piface.pfio.LED(0)
led1 = piface.pfio.LED(1)
led2 = piface.pfio.LED(2)
led3 = piface.pfio.LED(3)
led4 = piface.pfio.LED(4)
led5 = piface.pfio.LED(5)
led6 = piface.pfio.LED(6)
led7 = piface.pfio.LED(7)

# initialisation
piface.pfio.init()

# sw0 - start playback from pause
sw0 = piface.pfio.digital_read(0)

# sw1 - ?????
sw1 = piface.pfio.digital_read(1)

# sw2 - stop playback and reset
stopping = piface.pfio.digital_read(2)

# sw3 - shut down pi
halting = piface.pfio.digital_read(3)

# sleep for 2 secs to allow break out

print "PLAYER 1 INITIALISING..... Pausing for 2 secs to enable breakout (Control C breaks)"
time.sleep(2)

# show pictures in background (omxplayer will go on top)

fbishell = "fbi -a -noverbose -t 3 " + picture_path
fbi = subprocess.Popen(fbishell, stderr=None, stdout=None, shell=True)

# led0 - set on - ready to play
led0.turn_on()
# play action (0 = play)
goplay=1

# main
while not (halting):
    # relay activated - this player armed for next play
    time.sleep(0.05)
    # wait for input 0 (all players n/o relay contacts in series - start command)
    # all feed one multipole relay, n/o contact pairs to each pi input 0 and common
    # read input 0 which will be 0 for start and 1 for no action
    sw0 = piface.pfio.digital_read(0)
    # latch play signal to 0
    if not (sw0):
        goplay=0
    # check for sw3 - shut down pi
    halting = piface.pfio.digital_read(3)
    if halting:
        print "SHUTTING DOWN NOW................"
        led6.turn_on()
        led0.turn_off()
        subprocess.call(['shutdown -h now "System halted" &'], shell=True)
        time.sleep(15)
        
    # when started continues next while loop
    while (not (goplay)):
        # playback started deactivate relay (delay to allow other players to catch up)
        time.sleep(0.2)
        led0.turn_off()
        # play media
        omxp = subprocess.Popen(['omxplayer',movie_path],stdout=PIPE,stdin=PIPE)
        # while player running flash led7 and poll for stop or shutdown
        stopping = 0
        halting = 0
        goplay = 1
        while (omxp.poll() is None) and (not (halting)) and (not (stopping)):
            led7.turn_on()
            time.sleep(0.2)
            led7.turn_off()
            # sw2 - stop playback and reset
            stopping = piface.pfio.digital_read(2)
            # sw3 - shut down pi
            halting = piface.pfio.digital_read(3)
            time.sleep(0.5)
        # player now at end of track or interrupted by buttons
        if halting:
            led6.turn_on()
            led7.turn_off()
            omxp.stdin.write("q")
            # for omxplayer keys p pauses and q quits
            subprocess.call(['shutdown -h now "System halted" &'], shell=True)
            halting=0
            time.sleep(15)
        # player stopped and re-armed
        if stopping:
            led5.turn_on()
            led7.turn_off()
            # tell media player to quit
            omxp.stdin.write("q")
        # re-armed ready to play
        time.sleep(0.5)
        led5.turn_off()
        led0.turn_on()
        time.sleep(0.1)
        stopping=0
        # player come to end of track
        if ( not stopping ) and (not halting ) :
            # armed ready to play
            led0.turn_on()
            time.sleep(0.1)
    # terminal echo back on as omxp turns off
    stty = subprocess.call(['stty', 'echo'])
