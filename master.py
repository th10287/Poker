# Welcome to the master.py
# The main file of this program
# All other game mode files are run from this one

# Imports
import video_poker as vp
import texas_holdem_oop as th

# Ask user if they want to play video-poker (single player) or Texas Hold-em.
query = input("Would you like to play video poker(v) or Texas Hold-em(t)? ")
while query not in 'vt':
    query = input("I said 'v' or 't'. ")

# Chooses game based on user input
if query == "v":
    # if input is v run video_poker
    vp.game()
elif query == "t":
    # else if input is t run multiplayer/Texas Hold 'em
    #t.game()
    th.play()