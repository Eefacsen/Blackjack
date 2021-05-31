import random
import os
import time

# CLASSES

class card():
# CARD CLASS
    def __init__ (self,suit,info):
        self.suit = suit
        self.logo = suits[self.suit]
        self.name = info
        self.value = card_info[info]['value']
        self.symbol = card_info[info]['symbol']

    def __str__ (self):
        return f'[{self.symbol:2}{self.logo}]'

class deck():
# DECK CLASS
    def __init__ (self):
        self.cards = []
        for suit in suits:
            for info in card_info:
                new_card = card(suit,info)
                self.cards.append(new_card)

    def shuffle(self):
        random.shuffle(self.cards)

    def remove_one(self):
        card = self.cards.pop(0)
        return card

    def add_cards(self,return_cards):
        if type(return_cards) == type([]):
            self.cards.extend(return_cards)
        else:
            self.cards.append(return_cards)

class person():
# PLAYERS / DEALER CLASS
    def __init__ (self,name):
        self.name = name
        self.hand = []
        self.score = 0
        self.chips = 100
        self.bet = 0

    def __str__ (self):
        return f'{self.name} with {self.chips} chips'

    def add_bet(self,amount):
        self.chips -= amount
        self.bet = amount

    def add_chips(self,amount):
        self.chips += amount

    def hit(self,card):
        self.hand.append(card)

# FUNCTIONS

def clear():
    # clear the terminal display
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def get_name():
    while True:
        try:
            name = input('\nPlease enter your player name : ')
            if len(name) > 2:
                player = person(name)
                return player
            else:
                print('Name must be 3 char or more')
        except Exception as e:
            print(f'Invalid name entry : {e}')

def place_bets(players):
    # EACH PLAYER TO PLACE THEIR BETS
    for player in players:
        if player.name != 'Dealer':
            if player.chips < 2:
                while True:
                    try:
                        print(f'{player.name} does not have enough chips to play\n')
                        op = input('would you like to add more chips? [y] or [n] : ').lower()
                        if op == 'y':
                            player.add_chips(100)
                            print('Chips added')
                            break
                        elif op == 'n':
                            print(f'Thank you for playing {player.name}, Good bye')
                            players.remove(player)
                            break
                        else:
                            Exception = 'Invalid Entry for [y] or [n]'
                    except Exception as e:
                        print(e)
            
            print(f'{player.name} please place your bet 2-100')
            while True:
                try:
                    amount = int(input('--> : '))
                    if amount in range(2,101):
                        if amount <= player.chips:
                            player.add_bet(amount)
                            break
                        else:
                            print('You do not have that many chips to play this hand')
                    else:
                        print('Not a valid bet amount')
                except:
                    print('Invalid bet entry')
    return players

def new_game():
    clear()
    # SET UP THE GAME WITH PLAYERS, DEALER AND A DECK OF CARDS
    print('New game setup')
    Dealer = person('Dealer')
    players = [Dealer]
    while True:
        try:
            op = int(input('How many players : '))
            x=0
            while x < op:
                players.append(get_name())
                x += 1
            break
        except Exception as e:
            print('Invalid player count {}'.format(e))
    game_deck = deck()
    for each in players:
        print(f'\nWelcome {each.name}')

    players = players[::-1]

    rounds = 0
    play = True
    while play:
        rounds += 1
        clear()
        print('Shuffling Deck')
        game_deck.shuffle()
        time.sleep(2)

        players = place_bets(players)

        # DEAL 2 CARDS TO EACH PLAYER WITH 1 DEALER CARD HIDDEN
        for player in players:
            x = 0 
            while x < 2:
                player.hit(game_deck.remove_one())
                if x == 1:
                    print(f'\n{player.name:8} : ',end="")
                    if player.name == 'Dealer':
                        print(f'{player.hand[0]} [%%%]')
                    else:
                        for card in player.hand:
                            print(card, end=" ")
                time.sleep(1)
                
                x += 1
        time.sleep(1)

        # PLAYERS TURN TO PLAY - HIT OR STAY
        for player in players:
            if player.name != 'Dealer':
                myTurn = True

                while myTurn:        
                    clear()
                    print(f"{player.name}'s turn\n")
                    print(f'Your bet     : {player.bet}')
                    player.score = get_score(player.hand)
                    print(f'Your score   : {player.score}\n\n')
                    print(f'Dealers hand : {(players[-1].hand[0])} [%%%]')
                    print(f'Your hand    : ',end="")
                    for card in player.hand:
                        print(f'{card}',end=" ")
                    time.sleep(1)
                    
                    if player.score == 'BLACKJACK':
                        print('\nBLACKJACK YOU WIN')
                        myTurn = False
                        time.sleep(1)
                    elif player.score == 'BUST':
                        print('\nBUST YOU LOOSE')
                        myTurn = False
                        time.sleep(1)
                    else:
                        print('\n\n\nWould you like another card? [y] or [n]')
                        while True:
                            try:
                                op = input('--> : ').lower()
                                if op == 'y':
                                    card = game_deck.remove_one()
                                    player.hit(card)
                                    break
                                elif op == 'n':
                                    print('WAIT FOR DEALERS TURNS')
                                    myTurn = False
                                    time.sleep(1)
                                    break
                                else:
                                    print('Invalid entry for [y] or [n]')
                            except:
                                print('Invalid entry for [y] or [n]')

            else:    
                # dealer turn - work out a target score to reach to safely beat as many players as possible
                p_scored = []
                for p in players:
                    if type(p.score) == type(1):
                        p_scored.append(p.score)
                p_scored.pop()
                no_p = len(p_scored)
                if no_p > 0:
                    target = round(sum(p_scored)/no_p,0)
                    if target < 17:
                        target = 17
                else:
                    target = 0

                if player.name == 'Dealer':
                    dealer_turn = True
                    while dealer_turn:
                        clear()
                        for player in players:
                            if player.name != 'Dealer':
                                print(f'\n{player.name:10} : {player.score:9} : ',end="")
                                for card in player.hand:
                                    print(f'{card}',end=" ")
                            else:
                                player.score = get_score(player.hand)
                                print(f'\n{player.name:10} : {player.score:9} : ',end="")
                                for card in player.hand:
                                    print(f'{card}',end=" ")
                                time.sleep(2)
                                if player.score == 'BUST':
                                    print('\nDealer is BUST')
                                    time.sleep(2)
                                    dealer_score = player.score
                                    dealer_turn = False
                                elif player.score != 'BLACKJACK' and player.score < target:
                                    # KEEP DRAWING CARDS UNTIL WE MAKE TARGET OR BUST
                                    card = game_deck.remove_one()
                                    player.hit(card)
                                else:
                                    dealer_score = player.score
                                    dealer_turn = False
                                    print('Dealer stays')
                                    time.sleep(2)
        
        # WORK OUT WINNINGS AND RETURN CARDS TO THE DECK
        clear()
        print(f'Dealer score : {dealer_score}\n')
        print('')
        for player in players:
            if player.name != 'Dealer':
                amount = player.bet
                # CHECK FOR BLACKJACKS                            
                if dealer_score == 'BLACKJACK' and player.score != 'BLACKJACK':
                    status = 'Lose'
                elif player.score == 'BLACKJACK' and dealer_score != 'BLACKJACK':
                    status = 'Win'
                    amount *= 3
                    player.add_chips(amount)    
                
                # CHECK FOR BUSTS
                elif player.score == 'BUST':
                    status = 'Lose'
                elif dealer_score == 'BUST':
                    status = 'Win'
                    amount *= 2
                    player.add_chips(amount)

                # CHECK FOR PUSH
                elif player.score == dealer_score:
                    status = 'Push'
                    player.add_chips(amount)

                elif player.score > dealer_score:
                    status = 'Win'
                    amount *= 2
                    player.add_chips(amount)
                
                else:
                    status = 'Lose'        

                game_deck.add_cards(player.hand)
                player.hand.clear()
                print(f'{status:4} : {amount:3} : {player}\n')
                input('Enter to continue')

            elif player.name == 'Dealer':
                player.hand.clear()
            



def get_score(hand):
    # CHECK SCORE IS NOT ABOVE 21
    score = 0
    for card in hand:
        score += card.value
    if score > 21:
        for card in hand:
            # IF ABOVE 21 CHECK HAND FOR ACEs AND START CHANGING 11 -> 1 per ACE
            if card.name == 'Ace':
                score -= 10
                if score <= 21:
                    return score
        return 'BUST'
    # CHECK HAND FOR BLACKJACK = 21 in 2 CARDS
    if score == 21 and len(hand) == 2:
        return 'BLACKJACK'          
    else:
        return score  
                
    


    



# VARIABLES

suits = {'Hearts':'\U00002665','Spades':'\U00002660','Diamonds':'\U00002666','Clubs':'\U00002663'}
card_info = {'Ace' : {'value':11, 'symbol':'A'},
            'Two' : {'value':2, 'symbol':'2'},
            'Three' : {'value':3, 'symbol':'3'},
            'Four' : {'value':4, 'symbol':'4'},
            'Five' : {'value':5, 'symbol':'5'},
            'Six' : {'value':6, 'symbol':'6'},
            'Seven' : {'value':7, 'symbol':'7'},
            'Eight' : {'value':8, 'symbol':'8'},
            'Nine' : {'value':9, 'symbol':'9'},
            'Ten' : {'value':10, 'symbol':'10'},
            'Jack' : {'value':10, 'symbol':'J'},
            'Queen' : {'value':10, 'symbol':'Q'},
            'King' : {'value':10, 'symbol':'K'}}

# MAIN LOOP
def menu1():
    clear()
    print('\n**** BLACK-21-JACK ****\n')
    using_menu1 = True
    menu_items = ['New Game','Exit']
    # Using tuple unpacking with enumerate to index my menu faster
    for index,item in enumerate(menu_items):
            print(f'[{index}] - {item}')
    while using_menu1:
        try:
            op = int(input('--> : '))
                
            if op == 0:
                new_game()
            elif op == 1:
                using_menu1 = False
                print('Good Bye')
            else:
                print('Invalid entry')
                time.sleep(1)
                continue
        except:
            print('Invalid entry')
            time.sleep(1)
            continue

if __name__ == '__main__':
    menu1()