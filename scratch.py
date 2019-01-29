import random
    
def poker():
    allvalues = list("23456789TJQKA")
    allsuits = list("cdhs")
    allcards = []
    for suit in allsuits:
        for value in allvalues:
            allcards.append(value + suit)
    draw(allcards)

def draw(allcards):
    draw1 = random.randint(0,len(allcards)-1)
    card1 = allcards[draw1]
    #print(card1)
    del allcards[draw1]
    #print(allcards)
    draw2 = random.randint(0,len(allcards)-1)
    card2 = allcards[draw2]
    #print(card2)
    del allcards[draw2]
    #print(allcards)

def community_cards():
    

    
        



            

    