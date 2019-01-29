import random
def poker():
    hand = ""
    allvalues = "23456789TJQKA"
    allsuits = "cdhs"
    for x in range(10):
        hand = ""
        for y in range(2):
            value1 = random.randint(0,12)
            suit1 = random.randint(0,3)    
            for i in range(len(allvalues)):
                if i == value1:
                    hand += allvalues[i]
            for j in range(len(allsuits)):
                if j == suit1:
                    hand += allsuits[j]
                    if len(hand) == 2:
                        hand += " "
        return hand
      
            
                   
    
    
    
       
            
    
                
            
        
