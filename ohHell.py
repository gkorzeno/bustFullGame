from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox

root = Tk()
root.title('Teds Game') 
root.geometry("900x500")
root.configure(background="green")

leadSuit = None
numPlayers = 6
firstDealer = "Name"
indexFirstDealer = 0
firstBidder = "Name"
indexFirstBidder = 0
totalHands = 15
numCards = 8
dealingDown = True
currentHand = 8
display_frame = None
startingPosition = 0
play_order = []
turn_index = 0
trick_play_count = 0
numRound = 0
playedCards = []

current_turn_handler = None

player_start_card = None
npc_start_cards = []

playerNames = ["Player", "NPC 1", "NPC 2", "NPC 3", "NPC 4", "NPC 5"]
playerScores = {name: 0 for name in playerNames} 
playerBids = {}
tricksTaken = {}
newPlayerNames = []

def get_bids_for_hand():
    global playerBids, numCards
    playerBids = {}
    
    def collect_bid(index):
        if index >= len(play_order):
            root.after(300, start_turn)
            return
            
        player = play_order[index]
        
        if player == "Player":
            bid_window = Toplevel(root)
            bid_window.title("Enter Your Bid")
            bid_window.geometry("300x150")
            
            Label(bid_window, text=f"Enter your bid (0-{numCards}):").pack(pady=10)
            bid_var = StringVar()
            Entry(bid_window, textvariable=bid_var).pack(pady=5)
            
            def submit_bid():
                try:
                    bid = int(bid_var.get())
                    if 0 <= bid <= numCards:
                        if index == len(play_order) - 1:
                            total = sum(playerBids.values()) + bid
                            if total == numCards:
                                messagebox.showerror("Invalid Bid", "The total bids cannot equal the number of cards")
                                return
                        
                        playerBids[player] = bid
                        chart_cells[numRound][player]['bid'].config(text=str(bid))
                        bid_window.destroy()
                        collect_bid(index + 1)
                    else:
                        messagebox.showerror("Invalid Bid", f"Bid must be between 0 and {numCards}")
                except ValueError:
                    messagebox.showerror("Invalid Bid", "Please enter a number")
            
            Button(bid_window, text="Submit", command=submit_bid).pack(pady=5)
            bid_window.grab_set()
        else:
            npc_index = playerNames.index(player) - 1
            npc_hand = npc_players[npc_index]
            
            if numCards >= 5 and sum(playerBids.values()) < numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit and get_card_value(card) >= 11]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 13]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards >= 5 and sum(playerBids.values()) >= numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit and get_card_value(card) >= 12]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 14]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards == 4 and sum(playerBids.values()) < numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit and get_card_value(card) >= 10]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 12]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards == 4 and sum(playerBids.values()) >= numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit and get_card_value(card) >= 12]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 14]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards == 3 and sum(playerBids.values()) < numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit and get_card_value(card) >= 7]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 11]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards == 3 and sum(playerBids.values()) >= numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit and get_card_value(card) >= 10]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 12]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards == 2 and sum(playerBids.values()) < numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 11]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards == 2 and sum(playerBids.values()) >= numCards:
                trumpBidCount = [card for card in npc_hand if card.split('_')[-1] == trumpSuit and get_card_value(card) >= 7]
                highCardCount = [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 12]
                bid = len(trumpBidCount) + len(highCardCount)
            elif numCards == 1:
                if len(playerBids) == 0 and [card for card in npc_hand if card.split('_')[-1] == trumpSuit]:
                    bid = 1
                elif len(playerBids) == 0 and [card for card in npc_hand if card.split('_')[-1] != trumpSuit and get_card_value(card) >= 11]:
                    bid = 1
                elif [card for card in npc_hand if card.split('_')[-1] == trumpSuit]:
                    bid = 1 
                else:
                    bid = 0
            
            if index == len(play_order) - 1:
                total = sum(playerBids.values()) + bid
                if total == numCards:
                    if bid == 0:
                        bid += 1
                    else:
                        bid -= 1
            
            playerBids[player] = bid
            chart_cells[numRound][player]['bid'].config(text=str(bid))
            root.after(1000, lambda: collect_bid(index + 1))
    
    collect_bid(0)

chart_width = 0.49 
chart_height = 0.35 

chart_frame = Frame(root, bg="white", bd=2, relief="groove")
chart_frame.place(relx=(1 - chart_width)/2,  
                 rely=0.65, 
                 relwidth=chart_width, 
                 relheight=chart_height)

headers = ["Hand"] 
for player in playerNames:
    player_header = Frame(chart_frame, bg="lightgray")
    player_header.grid(row=0, column=len(headers), columnspan=3, sticky="nsew")
    
    Label(player_header, text=player, bg="lightgray", font=("Helvetica", 9, "bold"), 
         anchor="center").pack(fill=BOTH, expand=True)
    
    sub_header = Frame(player_header, bg="lightgray")
    sub_header.pack(fill=BOTH, expand=True)
    Label(sub_header, text="Bid", width=5, bg="lightgray", font=("Helvetica", 8), 
         anchor="center").pack(side=LEFT, fill=BOTH, expand=True)
    Label(sub_header, text="Got", width=5, bg="lightgray", font=("Helvetica", 8), 
         anchor="center").pack(side=LEFT, fill=BOTH, expand=True)
    Label(sub_header, text="Pts", width=5, bg="lightgray", font=("Helvetica", 8), 
         anchor="center").pack(side=LEFT, fill=BOTH, expand=True)
    
    headers.extend([f"{player}_bid", f"{player}_got", f"{player}_pts"])

chart_cells = {}
hand_numbers = list(range(8, 0, -1)) + list(range(2, 9)) 

for row in range(1, 16):
    hand_num = hand_numbers[row-1] if (row-1) < len(hand_numbers) else ""
    row_header = Label(chart_frame, text=str(hand_num), bg="lightgray", 
                      font=("Helvetica", 9), anchor="center")
    row_header.grid(row=row, column=0, sticky="nsew")
    
    for col, player in enumerate(playerNames, start=1):
        player_frame = Frame(chart_frame)
        player_frame.grid(row=row, column=1+(col-1)*3, columnspan=3, sticky="nsew")
        
        bid_cell = Label(player_frame, text="", bg="white", font=("Helvetica", 8), 
                        width=5, relief="ridge", anchor="center")
        got_cell = Label(player_frame, text="", bg="white", font=("Helvetica", 8), 
                        width=5, relief="ridge", anchor="center")
        pts_cell = Label(player_frame, text="", bg="white", font=("Helvetica", 8), 
                        width=5, relief="ridge", anchor="center")
        
        bid_cell.pack(side=LEFT, fill=BOTH, expand=True)
        got_cell.pack(side=LEFT, fill=BOTH, expand=True)
        pts_cell.pack(side=LEFT, fill=BOTH, expand=True)
        
        if row not in chart_cells:
            chart_cells[row] = {}
        chart_cells[row][player] = {'bid': bid_cell, 'got': got_cell, 'pts': pts_cell}

for i in range(16):
    chart_frame.rowconfigure(i, weight=1, uniform="chart_rows")
    
for i in range(1 + len(playerNames)*3):
    chart_frame.columnconfigure(i, weight=1, uniform="chart_cols")


def get_card_value(card_name):
    return int(card_name.split('_')[0])

def resizeCards(card):
    cardImage = Image.open(card)
    cardImageResized = cardImage.resize((69, 100))
    return ImageTk.PhotoImage(cardImageResized)

def onClick(event):
    global display_frame, turn_index, playedCards, leadSuit, trick_play_count

    if display_frame:
        display_frame.destroy()
        display_frame = None
    
    played_card = event.widget
    card_index = player_cards.index(played_card)
    card_name = player[card_index]
    played_suit = card_name.split('_')[-1]

    if trick_play_count > 0 and leadSuit:
        player_suits = [c.split('_')[-1] for c in player]
        
        if leadSuit in player_suits and played_suit != leadSuit:
            messagebox.showwarning(
                "Invalid Play", 
                f"You must follow {leadSuit} suit! You played {played_suit}."
            )
            return
        
    playedCards.append(("Player", card_name))

    trick_image = resizeCards(f'images/cards/{card_name}.png')
    trick_labels[0].config(image=trick_image)
    trick_labels[0].image = trick_image

    played_card.config(image='')
    played_card.image = None
    player.pop(card_index)
    player_cards.pop(card_index)

    turn_index = (turn_index + 1) % 6
    root.after(3000, play_next_card)

    if trick_play_count == 0:
        leadSuit = card_name.split('_')[-1]

    trick_play_count += 1

    if trick_play_count == 6:
        root.after(1000, clear_trick)

def play_next_card():
    global turn_index, current_turn_handler, trick_play_count
    
    if current_turn_handler:
        root.after_cancel(current_turn_handler)
        current_turn_handler = None
    
    if trick_play_count >= 6:
        clear_trick()
        return
        
    current_player = play_order[turn_index]
    
    if current_player == "Player":
        return
    else:
        idx = playerNames.index(current_player) - 1
        trick_labels[idx+1].config(bg='yellow')
        root.update()
        
        current_turn_handler = root.after(1000, lambda: complete_npc_turn(current_player))

def complete_npc_turn(npc_name):
    global turn_index, current_turn_handler, trick_play_count
    
    play_npc_card(npc_name)
    
    idx = playerNames.index(npc_name) - 1
    trick_labels[idx+1].config(bg='green')
    
    if trick_play_count < 6:
        turn_index = (turn_index + 1) % 6
        current_turn_handler = root.after(1000, play_next_card)
    else:
        current_turn_handler = root.after(1000, clear_trick)

def get_card_value(card):
    rank = card.split('_')[0]
    rank_map = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return int(rank_map.get(rank, rank))

def play_npc_card(npc_name):
    global trick_play_count, leadSuit, playedCards, playerBids, tricksTaken
    index_map = {
        "NPC 1": 0,
        "NPC 2": 1,
        "NPC 3": 2,
        "NPC 4": 3,
        "NPC 5": 4
    }

    if npc_name in index_map:
        idx = index_map[npc_name]
        current_hand = npc_players[idx]
        if not current_hand:
            return

        matching_cards = [c for c in current_hand if c.split('_')[-1] == leadSuit]
        trump_cards = [c for c in current_hand if c.split('_')[-1] == trumpSuit]
        playerNonTrump = [card for card in current_hand if card not in trump_cards]
        played_trumps = [card for (_, card) in playedCards if card.split('_')[-1] == trumpSuit]
        played_lead = [card for (_, card) in playedCards if card.split('_')[-1] == leadSuit]

        npc_bid = playerBids.get(npc_name, 0)
        npc_tricks = tricksTaken.get(npc_name, 0)
        needs_tricks = npc_tricks < npc_bid

        card = None

        if len(playedCards) == 0:
            if sum(playerBids.values()) > numCards and needs_tricks:
                card = max(current_hand, key=get_card_value) if needs_tricks else min(current_hand, key=get_card_value)
            else:
                card = min(current_hand, key=get_card_value)

        elif matching_cards: 
            best_own = max(matching_cards, key=get_card_value)
            best_played = max(played_lead, key=get_card_value)

            if get_card_value(best_own) > get_card_value(best_played) and needs_tricks and not played_trumps:
                card = best_own
            elif needs_tricks:
                card = min(matching_cards, key=get_card_value)
            else:
                card = max(matching_cards, key=get_card_value)

        elif not matching_cards:
            if needs_tricks:
                if trump_cards and not played_trumps:
                    card = min(trump_cards, key=get_card_value)
                elif trump_cards and played_trumps:
                    if get_card_value(max(played_trumps, key=get_card_value)) > get_card_value(max(trump_cards, key=get_card_value)):
                        card = min(playerNonTrump, key=get_card_value)
                    else:
                        card = max(trump_cards, key=get_card_value)
                else:
                    card = min(current_hand, key=get_card_value)
            else:
                card = min(playerNonTrump, key=get_card_value)

        if not card:
            card = random.choice(current_hand)
        
        if trick_play_count == 0:
            leadSuit = card.split('_')[-1]

        npc_players[idx].remove(card)
        playedCards.append((npc_name, card))
        npc_image = resizeCards(f'images/cards/{card}.png')
        trick_labels[idx + 1].config(image=npc_image)
        trick_labels[idx + 1].image = npc_image

        trick_play_count += 1

def takeTricks():
    global playedCards, trumpSuit, leadSuit, tricksTaken
    
    if not playedCards:
        return None
    
    trump_cards = []
    lead_cards = []
    
    for player, card in playedCards:
        suit = card.split('_')[-1]
        value = int(card.split('_')[0])
        
        if suit == trumpSuit:
            trump_cards.append((value, player))
        if suit == leadSuit:
            lead_cards.append((value, player))
    
    if trump_cards:
        winner = max(trump_cards)[1]
    elif lead_cards:
        winner = max(lead_cards)[1]
    else:
        winner = None
    
    if winner:
        tricksTaken[winner] = tricksTaken.get(winner, 0) + 1
        chart_cells[numRound][winner]['got'].config(text=str(tricksTaken[winner]))
    
    return winner
        
def clear_trick():
    global trick_play_count, display_frame, playedCards, tricksTaken, play_order, turn_index
    
    winner = takeTricks()
    
    if winner:
        winner_index = playerNames.index(winner)
        play_order = playerNames[winner_index:] + playerNames[:winner_index]
        turn_index = 0 

    for lbl in trick_labels:
        lbl.config(image='')
        lbl.image = None

    trick_play_count = 0
    playedCards = []

    if display_frame:
        display_frame.destroy()
        display_frame = None
    
    if not player:  
        scoreHand()
        root.after(2000, shuffleCards)
    else:
        root.after(1000, play_next_card)

def scoreHand():
    global playerScores, numCards
    for player in playerNames:
        bid = playerBids.get(player, 0)
        tricks = tricksTaken.get(player, 0)

        if bid == tricks and bid == 0:
            playerScores[player] += 10 + numCards
        elif bid == tricks and bid != 0:
            playerScores[player] += (tricks * tricks) + 10
        else:
            bidTrickDifference = abs(tricks - bid)
            playerScores[player] -= (bidTrickDifference * bidTrickDifference * bidTrickDifference)
        chart_cells[numRound][player]['pts'].config(text=str(playerScores[player]))

def npc1_play_card():
    if npc_players[0]:
        npc_card = random.choice(npc_players[0])
        npc_players[0].remove(npc_card)
        npc_image = resizeCards(f'images/cards/{npc_card}.png')
        trick_labels[1].config(image=npc_image)
        trick_labels[1].image = npc_image

def npc2_play_card():
    if npc_players[1]:
        npc_card = random.choice(npc_players[1])
        npc_players[1].remove(npc_card)
        npc_image = resizeCards(f'images/cards/{npc_card}.png')
        trick_labels[2].config(image=npc_image)
        trick_labels[2].image = npc_image

def npc3_play_card():
    if npc_players[2]:
        npc_card = random.choice(npc_players[2])
        npc_players[2].remove(npc_card)
        npc_image = resizeCards(f'images/cards/{npc_card}.png')
        trick_labels[3].config(image=npc_image)
        trick_labels[3].image = npc_image

def npc4_play_card():
    if npc_players[3]:
        npc_card = random.choice(npc_players[3])
        npc_players[3].remove(npc_card)
        npc_image = resizeCards(f'images/cards/{npc_card}.png')
        trick_labels[4].config(image=npc_image)
        trick_labels[4].image = npc_image

def npc5_play_card():
    if npc_players[4]:
        npc_card = random.choice(npc_players[4])
        npc_players[4].remove(npc_card)
        npc_image = resizeCards(f'images/cards/{npc_card}.png')
        trick_labels[5].config(image=npc_image)
        trick_labels[5].image = npc_image

def start_turn():
    global turn_index
    turn_index = 0  
    play_next_card()
   
my_frame = Frame(root, bg="green")

trick_frame = Frame(root, bg="green")

cards_frame = Frame(root, bg="green")

trump_frame = Frame(root, bg="green")

my_frame.pack_forget()
trick_frame.pack_forget()
cards_frame.pack_forget()
trump_frame.pack_forget()

trump_label = Label(trump_frame, text="Trump:", bg="green", fg="white", font=("Helvetica", 12))
trump_label.pack(side="left")

trump_card_label = Label(trump_frame, bg="green")
trump_card_label.pack(side="left")

trick_labels = []
trick_name_labels = []
player_positions = ["Player", "NPC 1", "NPC 2", "NPC 3", "NPC 4", "NPC 5"]

for i in range(6):
    lbl = Label(trick_frame, bg="green")
    lbl.grid(row=0, column=i, padx=5, pady=5)
    trick_labels.append(lbl)

    name_lbl = Label(trick_frame, text=player_positions[i], bg="green", fg="white", font=("Helvetica", 10))
    name_lbl.grid(row=1, column=i)
    trick_name_labels.append(name_lbl)

positions = [(0, 1), (1, 2), (2, 1), (1, 0), (0, -1), (-1, 0)]

player_label = Label(cards_frame, text="", bg="green")
player_label.grid(row=0, column=0, pady=10)

player_cards = []
for i in range(8):  
    card_label = Label(cards_frame, text='', bg="green")
    card_label.bind("<Button-1>", onClick)  
    card_label.grid(row=0, column=i+1, pady=10)
    player_cards.append(card_label)

npc_players = []
npc_cards = []

for j in range(5):
    cards = []

    for i in range(8):
        card_label = Label(cards_frame, text='', bg="green")
        card_label.grid(row=j+1, column=i+1, pady=10)
        cards.append(card_label)
    npc_cards.append(cards)
    
    npc_players.append([])

def shuffleCards():
    suits = ["spades", "hearts", "diamonds", "clubs"]
    values = range(2, 15)

    global deck, player, npc, numCards, trumpSuit, dealingDown, currentHand, numRound, startingPosition, play_order, turn_index, trick_play_count, playedCards, tricksTaken

    tricksTaken = {name: 0 for name in playerNames}

    numCards = currentHand

    turn_index = 0
    trick_play_count = 0
    playedCards = []

    all_players = ["Player", "NPC 1", "NPC 2", "NPC 3", "NPC 4", "NPC 5"]
    play_order = all_players[startingPosition:] + all_players[:startingPosition]

    while len(player_cards) < numCards:
        card_label = Label(cards_frame, text='', bg="green")
        card_label.bind("<Button-1>", onClick)  
        card_label.grid(row=0, column=len(player_cards)+1, pady=10)
        player_cards.append(card_label)

    for i in range(len(player_cards)):
        player_cards[i].config(image='', text='')
        player_cards[i].image = None
        if i < numCards:
            player_cards[i].grid()
        else:
            player_cards[i].grid_remove()

    deck = [f'{value}_of_{suit}' for suit in suits for value in values]
    random.shuffle(deck)

    trump_card = deck.pop()
    trumpValue = get_card_value(trump_card)
    trump_image = resizeCards(f'images/cards/{trump_card}.png')
    trump_card_label.config(image=trump_image)
    trump_card_label.image = trump_image

    if trumpValue == 14:
        messagebox.showwarning(
            "", 
            f"KINGS GOOD!"
        )

    trumpSuit = trump_card.split('_')[-1]  
 
    all_players = ["Player", "NPC 1", "NPC 2", "NPC 3", "NPC 4", "NPC 5"]
    play_order = all_players[startingPosition:] + all_players[:startingPosition]

    player = []
    for i in range(5):
        npc_players[i] = []

    for i in range(numCards):    
        card = random.choice(deck)
        deck.remove(card)
        player.append(card)
        player_image = resizeCards(f'images/cards/{card}.png')
        player_cards[i].config(image=player_image)
        player_cards[i].image = player_image

    for j in range(5):
        for i in range(numCards): 
            card = random.choice(deck)
            deck.remove(card)
            npc_players[j].append(card)
            npc_image = resizeCards(f'images/cards/{card}.png')
            npc_cards[j][i].config(image='', text='')  
            npc_cards[j][i].image = None

    if dealingDown:
        currentHand -= 1
        if currentHand < 1:
            currentHand = 2
            dealingDown = False
    else:
        currentHand += 1
        if currentHand > 8:
            currentHand = 8  
            dealingDown = True
    
    numRound = numRound + 1
    startingPosition = (startingPosition + 1) % 6

    get_bids_for_hand()

    root.title(f'Teds Game {len(deck)} Cards Left')

shuffle_button = Button(root, text="Shuffle", font=("Helvetica", 14), command=shuffleCards)
shuffle_button.pack_forget()

selection_frame = Frame(root, bg="green", width=900, height=500)
selection_frame.place(x=0, y=0)

card_back_images = []
card_back_labels = []

full_deck = [f'{value}_of_{suit}' for suit in ["spades", "hearts", "diamonds", "clubs"] for value in range(2, 15)]
random.shuffle(full_deck)

def display_start_cards(player_card, npc_cards):
    global display_frame
    display_frame = Frame(root, bg="green")
    display_frame.pack(pady=20)

    all_cards = [player_card] + npc_cards
    for i, card in enumerate(all_cards):
        image = resizeCards(f'images/cards/{card}.png')
        label = Label(display_frame, image=image, bg="green")
        label.image = image
        label.grid(row=0, column=i, padx=10)
    
    name_labels = ["You", "NPC 1", "NPC 2", "NPC 3", "NPC 4", "NPC 5"]
    for i, name in enumerate(name_labels):
        Label(display_frame, text=name, bg="green", fg="white", font=("Helvetica", 10)).grid(row=1, column=i)

    if display_frame:
        root.after(5000, lambda: display_frame.destroy())

def select_start_card(event, selected_card):
    global player_start_card, npc_start_cards, startingPosition, count_min
    selection_frame.place_forget()

    player_start_card = selected_card

    npc_start_cards = random.sample([card for card in full_deck if card != player_start_card], 5)

    display_start_cards(player_start_card, npc_start_cards)

    my_frame.pack(pady=0)
    trick_frame.pack(pady=(0, 0))
    cards_frame.pack(pady=0)
    trump_frame.pack(side="left", anchor="sw", padx=10, pady=10)

    startCards = [player_start_card] + npc_start_cards
    startCardsValues = [get_card_value(card) for card in startCards]
    min_val = min(startCardsValues)
    count_min = startCardsValues.count(min_val)

    if count_min > 1:
        messagebox.showwarning(
            "", 
            f"There was a tie you must redraw"
        )
        remaining_cards = [c for c in full_deck if c not in npc_start_cards]
        if not remaining_cards:  
            remaining_cards = full_deck.copy()
        selected_card = random.choice(remaining_cards)

    else:
        min_index = startCardsValues.index(min_val)
        startingPosition = (min_index + 1) % 6 
        print(f"Starting position is player {startingPosition}")
        
    global play_order
    all_players = ["Player", "NPC 1", "NPC 2", "NPC 3", "NPC 4", "NPC 5"]
    play_order = all_players[startingPosition:] + all_players[:startingPosition]

    shuffleCards()

overlap_offset = 15 
card_width = 69 
num_cards = 52

total_width = overlap_offset * (num_cards - 1) + card_width
start_x = (900 - total_width) // 2  

for i, card in enumerate(full_deck[:52]):
    image = resizeCards('images/cards/back_of_card.png')
    label = Label(selection_frame, image=image, bg="green")
    label.image = image
    label.place(x=start_x + overlap_offset * i, y=200)
    label.bind("<Button-1>", lambda e, c=card: select_start_card(e, c))
    card_back_labels.append(label)
    card_back_images.append(image)

root.mainloop()
