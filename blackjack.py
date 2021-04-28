import tkinter
import random

chip_amount = 500


def load_images(card_images):
    suits = ["heart", "club", "diamond", "spade"]
    face_cards = ["jack", "queen", "king"]

    if tkinter.TkVersion >= 8.5:
        extension = "ppm"


#  for each suit, retrieve the image
    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

        #then the face cards
        for card in face_cards:
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def initial_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()

def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    #  embedded frame to hold card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background="green")
    dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)
    #  embedded frame to hold card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=2)

    result_text.set("")

    #   create list to store dealer and player's hands
    dealer_hand = []
    player_hand = []
    initial_deal()




def _deal_card(frame):
    # pop the next card off the top of the deck
    next_card = deck.pop(0)
    # add it to back of the deck
    deck.append(next_card)
    # add the image to a label and display the label
    tkinter.Label(frame, image=next_card[1], relief="raised").pack(side="left")
    # now return the card's face value
    return next_card

def score_hand(hand):
    # Calculate the total score of all cards in the list
    # Only one ace can have value 11, and this will reduce to 1 if hand would bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we'd bust, check if there's an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append((_deal_card(dealer_card_frame)))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer wins")
    else:
        result_text.set("Draw")


def deal_player():
    player_hand.append(_deal_card(player_card_frame))
    player_score = score_hand(player_hand)

    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer wins")



    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # # if we would bust, then checks if there's an ace and subtract 10
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer Wins.")
    # print(locals())


def shuffle():
    random.shuffle(deck)


def play():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()
    mainWindow.mainloop()


mainWindow = tkinter.Tk()


# set up screen and frames for dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background="green")

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky="ew", columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)
# embedded frame hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)

player_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)
# embedded frame to hold card images
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky="ew", rowspan=3)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky="w")

stay_button = tkinter.Button(button_frame, text="Stay", command=deal_dealer)
stay_button.grid(row=0, column=0)

hit_button = tkinter.Button(button_frame, text="Hit", command=deal_player)
hit_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=3)

#  my personal additions of wager and chips (incomplete)
# chips_frame = tkinter.Frame(mainWindow)
# chips_frame.grid(row=4, column=0, columnspan=4, sticky="w")
#
# tkinter.Label(chips_frame, text="Chips: {}".format(chip_amount), background="green", fg="white").grid(row=0, column=0)
#
# wager_frame = tkinter.Frame(mainWindow)
# wager_frame.grid(row=5, column=0, columnspan=4, sticky="w")
# wager = tkinter.Label(wager_frame, text="Select Wager: ", background="green", fg="white")


#  load cards
cards = []
load_images(cards)
print(cards)

#   create new deck of cards and shuffle
deck = list(cards) + list(cards) + list(cards)
random.shuffle(deck)

#   create list to store dealer and player's hands
dealer_hand = []
player_hand = []

# new_game()

if __name__ == "__main__":
    play()

