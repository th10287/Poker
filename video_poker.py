# This file is for the single player video poker version of the game.

# Imports
from random import randint
from deck_creator_local import dc


# dsp = display; converts '14H to AH'
dsp = {
    10:'T',
    11:'J',
    12:'Q',
    13:'K',
    14:'A'
}

# Hand class contains all the cards the user will see and determine multipliers
class Hand:
    def __init__(self):
        self.cards = dc.draw(5)
    @property
    def display(self):
        displayCards = ''
        for val, suit in self.cards:
            displayCards += f'[{dsp.get(val, val)}{suit}] '
        return displayCards
    @property
    def rank(self):
        # determines which hand the player has, from a royal flush \
        # to a high card using return statements
        self.vals = sorted([val for val,suit in self.cards], reverse=True)
        self.suits = [suit for val,suit in self.cards]

        # royal flush
        fVals = [val for val,suit in self.cards if self.suits.count(suit) >= 5]
        if {2,3,4,5}.issubset(fVals) and 14 in fVals and 6 not in fVals:
            return 'Straight Flush', 50
        for v in sorted(fVals, reverse=True):
            if {v-4, v-3, v-2, v-1, v}.issubset(fVals):
                if v == 14:
                    return 'Royal Flush', 250
                return 'Straight Flush', 50 

        # four of a kind
        for v in self.vals:
            if self.vals.count(v) == 4:
                return 'Four of a Kind', 25

        # full house
        # 'triples' and 'doubles' will create lists of values which 2 or 3 cards possess in a players hand, respectively
        # if a player does not have a double or triple, the corresponding list will be empty
        triples = sorted(list({val for val in self.vals if self.vals.count(val) == 3}), reverse=True)
        doubles = sorted(list({val for val in self.vals if self.vals.count(val) == 2}), reverse=True)
        if bool(triples) and bool(doubles):
            return 'Full House', randint(6, 10)

        # flush, fVals variable in 'royal flush' checker
        if bool(fVals):
            return 'Flush', randint(5, 7)

        # straight
        # first check is for A2345 straight
        if {2,3,4,5}.issubset(self.vals) and 14 in self.vals and 6 not in self.vals:
            return 'Straight', 4
        for v in self.vals:
            if {v-4, v-3, v-2, v-1, v}.issubset(self.vals):
                return 'Straight', 4

        # three of a kind, triples variable in 'full house' checker
        if bool(triples):
            return 'Three of a Kind', 3
        
        # two pair, doubles variable in 'full house' checker
        if len(doubles) >= 2:
            return 'Two Pair', 2

        # pair, doubles variable in 'full house' checker
        if bool(doubles):
            return 'Pair', 1

        # high card
        return 'High Card', 0
    @property
    def multiplier(self):
        return self.rank[1]
    @property
    def name(self):
        return self.rank[0]
    # swap takes in a string of numbers (ex: '12345') and swaps cards out based on these values
    # '1' swaps the first card, '2' swaps the second, etc.
    def swap(self, numstr):
        self.cards = [dc.draw(1)[0] if str(i+1) in numstr else self.cards[i] for i in range(len(self.cards))]
        
# Main function for this file. It has three parameters that are changed throughout, 
# but default to None, -100.00, and 0.
def game(tuple_list = None, initial_bet = -100.00, count = 0): 
    # Count for number of times the function has been called
    count += 1
    while initial_bet <= 0:
        try:
            initial_bet = float(input("How much would you like to bet?\n$"))
        except ValueError:
            continue
    hand = Hand()
    print(f'{hand.display}\n{hand.name}\nThis hand would win you ${initial_bet*hand.multiplier:.2f}')
    hand.swap(input('What cards would you like to swap? ("12345" trades all)\n'))
    print(f'{hand.display}\n{hand.name}\nYou won ${initial_bet*hand.multiplier:.2f}!')

