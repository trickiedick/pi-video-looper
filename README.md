pi-video-looper
===============

Simple script to automate playing of videos on Rasperry Pi - with multi-client sync

The Raspberry Pis I'm using are fitted with the PiFace interface boards in order to 
simplify the hardware.  

I'm using the relay0 output to indicate that each pi is finished playing video and ready 
to re-start.  When all players are ready then a master relay is deactivated - letting
input 0 go high on all of the raspberry pis.  All of the pi's then start their vido 
in synchronism.

In operation with 3 units the videos are close enough to give what looks like reasonable
(but not perfect) lip synchronisation between the 3 players. (I'm playing 3 different
videos to the same soundtrack and only using audio on one.)

(working from memory as units are in use right now)


