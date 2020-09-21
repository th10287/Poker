# This file creates the deck for all game modes

# Imports
import requests
import json

# Calls Deck of Cards API visit their website at https://deckofcardsapi.com/
# This API is viable for use under the MIT license.
response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
# Converts API code from json to python
deck = json.loads(response.text)

# GLOBAL VARIABLES
# Creates a dictionary to give values to every card.
cardvalue = {
    "1": 10,
    "j": 11,
    "q": 12,
    "k": 13,
    "a": 14,
    "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9
}

# This function draws however many cards you input
def draw(draw_count):
    tuple_list = []
    value = ""
    deck_id = deck["deck_id"]
    # Calls the deck that we created globally and draws however many cards are needed.
    json_draw = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=" + str(draw_count))
    # Converts from json to python
    draw_cards = json.loads(json_draw.text)
    # Puts one card into the tuple list
    for num in range(draw_count):
        value = draw_cards["cards"][num]["value"][0].lower()
        value = cardvalue[value]
        tuple_list.append((value, draw_cards["cards"][num]["suit"][0].lower()))
    return tuple_list

# This function takes in the tuple list of cards and the user input 
# for which cards they would like to swap out.
# It then swaps these for cards from the deck.
def swap(tuple_list, int_string):
    index_list = [int(num) for num in int_string]
    # Converts the string user input into a list of ints
    new_tuple = draw(len(index_list))
    count = 0
    # Finds an index for the tuple list
    for num in index_list:
        tuple_list[num - 1] = new_tuple[count]
        count += 1
    return tuple_list
    