import random as r
import time as t
from deck_creator_local import dc

# fc = face cards; converts values to names of face cards
fc = {
    11:'Jack',
    12:'Queen',
    13:'King',
    14:'Ace',
    2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10'
}
# dsp = display; converts '14H to AH'
dsp = {
    10:'T',
    11:'J',
    12:'Q',
    13:'K',
    14:'A'
}
symbols = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
handName = {
    9: "royal flush",
    8: "straight flush",
    7: "four of a kind",
    6: "full house",
    5: "flush",
    4: "straight",
    3: "three of a kind",
    2: "two pair",
    1: "pair",
    0: "high card" 
}

# a Table object contains players and 1 set of community cards
# list of players is equivalent to the order of players around a table going CLOCKWISE
class Table:
    def __init__(self, numPlayers=2, ID=1):
        self.name = f'Table {ID}'
        self.community = Community()
        self.ID = ID
        self.players = [Player(1, self, cpu=False)] + [Player(i, self) for i in range(2, numPlayers+1)]
        # 'dealer' position changes after every round, starts at first player; this is used to determine blinds, as well
        self.dealer = self.players[0]
        # pot is the total money to be won. starts at 0
        self.pot = 0
        # currentbet changes each round and is the bet that all players must match to advance to the next round
    # deal goes around the table twice and deals a card each time to the respective player
    def deal(self):
        for player in self.players * 2:
            card = dc.draw(1)
            player.holdCards += card
    @property
    def smlBlind(self):
        # checks position of dealer and gets 1st pos to their left
        pos = self.playersIn.index(self.dealer) + 1
        try:
            return self.playersIn[pos]
        # resets back to 0 if at end of list
        except IndexError:
            return self.playersIn[0]
    @property
    def bigBlind(self):
        # checks the position of the small blind and gets 1st position to their left
        pos = self.playersIn.index(self.smlBlind) + 1
        try:
            return self.playersIn[pos]
        except IndexError:
            return self.playersIn[0]
    @property
    def currentBet(self):
        return max([player.bet for player in self.players])
    # rotate moves the 'dealer' one seat over clockwise; in another sense, the small blind becomes the 'dealer'
    def rotate(self):
        self.dealer = self.smlBlind
    # players that are 'in' havent folded and are still betting
    @property
    def playersIn(self):
        return [player for player in self.players if not player.folded]
    # ranked returns a list of players who havent folded in order by made hand
    @property
    def ranked(self):
        return sorted(self.playersIn, reverse=True)
    # winners returns players with the best hand among all players
    @property
    def winners(self):
        if len(self.playersIn) == 1:
            return self.playersIn[0]
        return [player for player in self.playersIn if player == self.ranked[0]]
    # winDesc returns a sentence describing which player(s) won
    @property
    def winDesc(self):
        winners = self.winners
        desc = f'Player {winners[0].ID}'
        if len(winners) > 2:
            for player in winners[1:-1]:
                desc += f', Player {player.ID}'
            desc += f', and Player {winners[-1].ID}'
        elif len(winners) == 2:
            desc += f' and Player {winners[-1].ID}'
        if len(winners) == len(self.playersIn):
            end = ' tie!'
        else:
            end = ' win!'
        if len(winners) == 1:
            end = ' wins!'
        return desc + end

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

# Community class contains and pulls cards visible to all players
class Community:
    def __init__(self):
        self.cards = []
        self.burnpile = []
    @property
    def displayCards(self):
        displayCards = 'Community Cards:\n'
        for val, suit in self.cards:
            displayCards += f'[{dsp.get(val, val)}{symbols[suit]}] '
        return displayCards
    # Calls deck_creator for flop, turn, and river when they are called
    def flop(self):
        while len(self.cards) < 3:
            burn = dc.draw(1) # Burns a card
            self.burnpile += burn
            self.flopcards = dc.draw(3)
            self.cards += self.flopcards
        return self.flopcards
    def turn(self):
        # loop only runs if community has 3 cards and needs a 4th
        while 3 <= len(self.cards) < 4:
            burn = dc.draw(1) # Burns another card
            self.burnpile += burn
            # turncard will not exist until this loop is completed
            self.turncard = dc.draw(1)
            self.cards += self.turncard
        try:
            return self.turncard
        except AttributeError:
            return 'The flop must be played first!'
    def river(self):
        # loop only runs if community has 4 cards and needs a 5th
        while 4 <= len(self.cards) < 5:
            burn = dc.draw(1) # Burns final card
            self.burnpile += burn
            # rivercard will not exist until this loop is completed
            self.rivercard = dc.draw(1)
            self.cards += self.rivercard
        try:
            return self.rivercard
        except AttributeError:
            return 'The turn must be played first!'
    # showall plays the flop, turn, and river automatically if called
    def playall(self):
        self.flop()
        self.turn()
        self.river()
    def __repr__(self):
        return self.cards

class Player:
    def __init__(self, ID, table, cpu=True, chips=0):
        self.ID = ID
        self.chips = chips
        self.table = table
        # non-controlled players will have isCPU as True
        self.isCPU = cpu
        self.bet = 0
        self.folded = False
        # players begin with no hold cards, they are recieved when the table deals them
        self.holdCards = []
    # hand returns all (up to 7) cards in a players hand
    # only 5 of these cards can make a hand, however
    @property
    def hand(self):
        communityCards = self.table.community.cards
        return communityCards + self.holdCards
    # displyHold shows hold cards but makes them easier to read; the tuple (14, 'h') converts to [Ah]
    @property
    def displayHold(self):
        displayHold = f'{self}: '
        for val, suit in self.holdCards:
            displayHold += f'[{dsp.get(val, val)}{symbols[suit]}] '
        return displayHold
    def call(self):
        # call matches the current bet at the table, NOT IMPLEMENTED
        currentBet = self.table.currentBet
        if currentBet > self.currentChips:
            self.bet = self.currentChips
        else:
            self.bet = currentBet
    def raiseMethod(self, bet=0):
        currentBet = self.table.currentBet
        newBet = bet
        while newBet <= 0:
            try:
                newBet = int(input('How much would you like to raise?'))
            except ValueError:
                continue
        self.bet = currentBet + newBet
    # fold will be called if a player decides to forfeit that round
    def fold(self):
        self.folded = True
    def decision(self):
        # current bet is taken from table properties
        currentBet = self.table.currentBet
        print(f'{self.table.community.displayCards}\nYour Cards: {self.displayHold}')
        choice = ''
        # if current bet is 0, options are check, raise, fold
        if currentBet == 0:
            while choice.lower() not in ['check', 'raise', 'fold']:
                choice = input(f'Current bet is {currentBet}.\n Would you like to check, raise, or fold?')
        # if current bet is above 0, options are call, raise, fold
        else:
            while choice.lower not in ['call', 'raise', 'fold']:
                choice = input(f'Current bet is {currentBet}.\n Would you like to call(${currentBet - self.bet}), raise, or fold?')
        if choice == 'check':
            self.check()
        elif choice == 'call':
            self.call()
        elif choice == 'raise':
            self.raiseMethod()
        elif choice == 'fold':
            self.fold()
    def decisionCPU(self):
        pass
    # if I began a round with 1000 chips and bet 200 on the flop, i will have 800 chips left to bet with on the turn
    @property
    def currentChips(self):
        return self.chips - self.bet
    @property
    def allIn(self):
        return self.currentChips == 0
    @property
    def rank(self):
        # rank determines which hand the player has, from a royal flush \
        # to a high card using return statements
        self.vals = sorted([val for val,suit in self.hand], reverse=True)
        self.suits = [suit for val,suit in self.hand]

        # royal flush
        fVals = [val for val,suit in self.hand if self.suits.count(suit) >= 5]
        if {2,3,4,5}.issubset(fVals) and 14 in fVals and 6 not in fVals:
            return 8, 5
        for v in sorted(fVals, reverse=True):
            if {v-4, v-3, v-2, v-1, v}.issubset(fVals):
                if v == 14:
                    return (9,)
                return 8, v 

        # four of a kind
        for v in self.vals:
            if self.vals.count(v) == 4:
                quad = v
                kicker = max([val for val in self.vals if val is not quad])
                return 7, quad, kicker

        # full house
        # 'triples' and 'doubles' will create lists of values which 2 or 3 cards possess in a players hand, respectively
        # if a player does not have a double or triple, the corresponding list will be empty
        triples = sorted(list({val for val in self.vals if self.vals.count(val) == 3}), reverse=True)
        doubles = sorted(list({val for val in self.vals if self.vals.count(val) == 2}), reverse=True)
        if bool(triples) and bool(doubles):
            return 6, max(triples), max(doubles)

        # flush, fVals variable in 'royal flush' checker
        if bool(fVals):
            return (5,) + tuple(sorted(fVals, reverse=True)[:5])

        # straight
        if {2,3,4,5}.issubset(self.vals) and 14 in self.vals and 6 not in self.vals:
            return 4, 5
        for v in self.vals:
            if {v-4, v-3, v-2, v-1, v}.issubset(self.vals):
                return 4, v

        # three of a kind, triples variable in 'full house' checker
        if bool(triples):
            topTriple = max(triples)
            kickers = sorted([val for val in self.vals if val is not topTriple], reverse=True)
            return (3, topTriple) + tuple(kickers[:2])
        
        # two pair, doubles variable in 'full house' checker
        if len(doubles) >= 2:
            topTwoPair = doubles[:2]
            kickers = sorted([val for val in self.vals if val not in topTwoPair], reverse=True)
            return (2,) + tuple(topTwoPair) + tuple(kickers[:1])

        # pair, doubles variable in 'full house' checker
        if bool(doubles):
            topPair = doubles[0]
            kickers = sorted([val for val in self.vals if val is not topPair], reverse=True)
            return (1, topPair) + tuple(kickers[:3])

        # high card
        return (0,) + tuple(self.vals[:5])
    @property
    def description(self):
        sent = f'Player {self.ID} has'
        verbosity = self.verbosity
        info = self.rank
        rank = info[0]
        try:
            val = fc[info[1]]
        except IndexError:
            val = None
        try:
            kicker = info[2:]
        except IndexError:
            kicker = None
        if rank == 9:
            return f"{sent} a royal flush!"
        elif rank in [8,5,4]:
            sent += f" a {handName[rank]}, {val} high"
            if rank == 5:
                if verbosity >= 2: sent = sent + f", second card{fc[kicker[0]]}"
                if verbosity >= 3: sent = sent + f", third card {fc[kicker[1]]}"
                if verbosity >= 4: sent = sent + f", fourth card {fc[kicker[2]]}"
                if verbosity == 5: sent = sent + f", fifth card {fc[kicker[3]]}"
            return f'{sent}.'
        elif rank == 7:
            sent += f" four of a kind, {val}s"
            if verbosity >= 2: sent = sent + f", fifth card {fc[kicker[0]]}"
            return f'{sent}.'
        elif rank == 6:
            return f"{sent} a full house, {val}s full of {fc[kicker[0]]}s."
        elif rank == 3:
            sent += f" three of a kind, {val}s"
            if verbosity >= 2: sent = sent + f', fourth card {fc[kicker[0]]}'
            if verbosity >= 3: sent = sent + f', fifth card {fc[kicker[1]]}'
            return f'{sent}.'
        elif rank == 2:
            sent += f" two pair, {val}s and {fc[kicker[0]]}s"
            if verbosity >= 3: sent = sent + f', fifth card {fc[kicker[1]]}'
            return f'{sent}.'
        elif rank == 1:
            sent += f" a pair of {val}s"
            if verbosity >= 2: sent = sent + f", third card {fc[kicker[0]]}"
            if verbosity >= 3: sent = sent + f', fourth card {fc[kicker[1]]}'
            if verbosity >= 4: sent = sent + f', fifth card {fc[kicker[2]]}'
            return f'{sent}.'
        elif rank == 0:
            sent += f" a high card, {val}"
            if verbosity >= 2: sent = sent + f", second card {fc[kicker[0]]}"
            if verbosity >= 3: sent = sent + f", third card {fc[kicker[1]]}"
            if verbosity >= 4: sent = sent + f", fourth card {fc[kicker[2]]}"
            if verbosity == 5: sent = sent + f", fifth card {fc[kicker[3]]}"
            return f'{sent}.'
    def compare(self, other):
        me = list(self.rank)
        them = list(other.rank)
        if len(me) != len(them):
            return 0
        i = 0
        while i < len(me) and me[i] == them[i]:
            i += 1
        return i
    @property
    def verbosity(self):
        others = [other for other in self.table.players if other is not self]
        comparisons = [self.compare(other) for other in others]
        return max(comparisons)
    
    def __lt__(self, other):
        return self.rank < other.rank
    def __eq__(self, other):
        return self.rank == other.rank
    def __gt__(self, other):
        return self.rank > other.rank
    def __repr__(self):
        return f'P{self.ID}'

 # function begins here

def play(printOut=True):
    numPlayers = -1
    while not 2 <= numPlayers <= 22:
        try:
            numPlayers = int(input('How many players are at the table? (2-22) '))
        except ValueError:
            continue
    
    # create new table and set of community cards
    table = Table(numPlayers)
    comm = table.community
    # deal all cards and plays hand of poker
    table.deal()
    comm.playall()
    if printOut:
        print(comm.displayCards, end='\n\n')
        for player in table.playersIn:
            print(player.displayHold)
            print(player.description)
        print(f'\n{table.winDesc}')

        


    