# Welcome to the master.py
# The main file of this program
# All other game mode files are run from this one

# Imports
#import video_poker as v
import new_vp as nv
## texas_hold_em is deprecated cuz objects are cooler
#import texas_hold_em as t
import oopTester as test

# Ask user if they want to play video-poker (single player) or Texas Hold-em.
query = input("Would you like to play video poker(v) or Texas Hold-em(t)? ")
while query not in 'vt':
    query = input("I said 'v' or 't'. ")

# Chooses game based on user input
if query == "v":
    # if input is v run video_poker
    nv.game()
elif query == "t":
    # else if input is t run multiplayer/Texas Hold 'em
    #t.game()
    test.play()