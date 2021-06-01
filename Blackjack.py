import random
import os
import time

# CLASSES

class card():
# CARD CLASS
    def __init__ (self,suit,info):
        self.suit = suit
        # to get logo I used a self set variable self.suit
        self.logo = suits[self.suit]
        # info is a second tier dictionary item
        self.name = info
        # refer to dictionary card_info then to key[info] then to tier 2 key[value]
        self.value = card_info[info]['value']
        self.symbol = card_info[info]['symbol']

    def __str__ (self):
        return f'[{self.symbol:2}{self.logo}]'

class deck():
# DECK CLASS
    def __init__ (self):
        # deck class is an empty list we will fill with card class objects
        self.cards = []
        # refer to global variable section for card varibales
        for suit in suits:
            for info in card_info:
                new_card = card(suit,info)
                # after itterating through 4 suit 13 times each we will have appened 52 cards (a full deck)
                self.cards.append(new_card)

    def shuffle(self):
        # imported random library in order to randomize the order of a list (a shuffle)
        random.shuffle(self.cards)

    def remove_one(self):
        # remove last card in the list
        # deal top card of the deck
        card = self.cards.pop(0)
        return card

    def add_cards(self,return_cards):
        # check if varibale is a list type or not
        # if list type then there are more than one returned object and we need to extend our list
        if type(return_cards) == type([]):
            self.cards.extend(return_cards)
        # if only 1 object is returned we need to appened to our list
        else:
            self.cards.append(return_cards)

class person():
# PLAYERS / DEALER CLASS
    def __init__ (self,name):
        # player name
        self.name = name
        # player hand - empty to start
        self.hand = []
        # player score with empty hand is 0
        self.score = 0
        # player start chips, we could add an input on name capture
        # then set the buyin amount through a user entered passed variable
        # self.chips = buyin - remember to add 'buyin' to the __init__ above 
        self.chips = 100
        # before a hand is deal the bet will start at 0
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
            if name == '999':
                print('Returning to menu')
                menu1()
            elif len(name) > 2:
                player = person(name)
                #create and return a player class to add to the players list
                return player
            else:
                print('Name must be 3 charactors or more')
        except Exception as e:
            print(f'Invalid name entry : {e}')

def place_bets(players):
    # EACH PLAYER TO PLACE THEIR BETS
    for player in players:
        if player.name != 'Dealer':
            print(f'Current chip stack - {player.chips}')
            # check if the player has enough chips to bet with
            if player.chips < 2:
                while True:
                    try:
                        print(f'{player.name} does not have enough chips to play\n')
                        # here we force lower case answer so that later checks dont need to check for Y and y
                        op = input('would you like to add more chips? [y] or [n] : ').lower()
                        if op == 'y':
                            # I have forced this rebuy to 100 chips but could easily add an input line for user indicated amount
                            player.add_chips(100)
                            print('Chips added')
                            break
                        elif op == 'n':
                            print(f'Thank you for playing {player.name}, Good bye')
                            # No more buyin so remove the player from the player list and therefor from the game
                            players.remove(player)
                            break
                        else:
                            Exception = 'Invalid Entry for [y] or [n]'
                    except Exception as e:
                        print(f'Error in place_bets - player rebuy : {e}')
            
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
                # by removeing 10 for the last found Ace, we check score is below 21, if so return score
                if score <= 21:
                    return score
        # after checking all cards for Aces if we not below 21 we then return bust
        return 'BUST'
    # CHECK HAND FOR BLACKJACK = 21 in 2 CARDS
    if score == 21 and len(hand) == 2:
        return 'BLACKJACK'          
    else:
        return score  

def new_game():
    clear()
    # SET UP THE GAME WITH PLAYERS, DEALER AND A DECK OF CARDS
    print('New game setup')
    # set the dealer as a person class
    Dealer = person('Dealer')
    # add dealer to players list that are at the table
    players = [Dealer]
    # Using a bolean and not a variable in my while statment
    while True:
        try:
            op = int(input('How many players : '))
            if op == 0:
                print('You need more players')
                continue
            elif op == 999:
                print('returning to menu')
                menu1()
            x = 0
            while x < op:
                players.append(get_name())
                x += 1
            # with no variable set as bolean we need to break out of the while loop when ready
            break
        except Exception as e:
            print('Invalid player count {}'.format(e))
    # create the class object game_deck to track the movments of cards
    # I have used only 1 deck for my game that will get shuffled after every hand
    # Normal 21 rules use 3 decks and only get shuffled once
    game_deck = deck()
    for each in players:
        print(f'\nWelcome {each.name}')

    # I reverse the list of players to place the dealer as the last player
    players = players[::-1]

    # rounds is a counter set only for interest perposes
    rounds = 0
    play = True
    while play:
        rounds += 1
        clear()
        print('Shuffling Deck')
        game_deck.shuffle()
        # dramatic pause
        time.sleep(1)

        # once returned the new player list with contain the bets for each player this round
        players = place_bets(players)

        # DEAL 2 CARDS TO EACH PLAYER WITH 1 DEALER CARD HIDDEN
        for player in players:
            x = 0 
            while x < 2:
                # remove 1 card from game_deck and hit(add) to that players hand 
                player.hit(game_deck.remove_one())
                if x == 1:
                    # if x = 1 then both cards have been delt
                    # I use end="" so that the next print is not on a new line 
                    # now we can see name and cards on 1 line
                    print(f'\n{player.name:8} : ',end="")
                    time.sleep(0.5)
                    if player.name == 'Dealer':
                        # if dealer shop us the first card but keep the second card hidden
                        print(f'{player.hand[0]} [%%%]')
                        time.sleep(0.5)
                    else:
                        for card in player.hand:
                            #print each card in the players hand seperated by a space
                            print(card, end=" ")
                            time.sleep(0.5)
                # after each player is delt pause for drama
                # removed pause for better flow
                # time.sleep(1)
                
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
                        time.sleep(0.5)
                    time.sleep(1)
                    
                    # if player has blackjack - end this turn
                    if player.score == 'BLACKJACK':
                        print('\nBLACKJACK YOU WIN')
                        myTurn = False
                        time.sleep(1)
                    # if player is bust - end this turn
                    elif player.score == 'BUST':
                        print('\nBUST YOU LOOSE')
                        myTurn = False
                        time.sleep(1)
                    # else we will need input from the player to continue
                    else:
                        print('\n\n\nWould you like another card? [y] or [n]')
                        while True:
                            try:
                                op = input('--> : ').lower()
                                if op == 'y':
                                    player.hit(game_deck.remove_one())
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
            # player is now = dealer
            else:    
                # dealer turn - work out a target score to reach to safely beat as many players as possible
                p_scored = []
                for p in players:
                    # here we check if the player.score is an integer and add this to the list of scores to beat
                    # if score is a string then player does not need to be beaten
                    if type(p.score) == type(1):
                        p_scored.append(p.score)
                # pop with remove the last score added as this is the dealers score
                p_scored.pop()
                no_p = len(p_scored)
                if no_p > 0:
                    target = round(sum(p_scored)/no_p,0)
                    if target < 17:
                        # dealer must play every hand to at least a soft stop of 17
                        target = 17
                # if no players are left to beat then there is no point in playing the hand
                else:
                    target = 0

                if player.name == 'Dealer':
                    dealer_turn = True
                    while dealer_turn:
                        clear()
                        for player in players:
                            # show all hands around the table so each player can track their progress
                            if player.name != 'Dealer':
                                # I use a player.score padding of 9 for the word BLACKJACK
                                print(f'\n{player.name:10} : {player.score:9} : ',end="")
                                for card in player.hand:
                                    print(f'{card}',end=" ")
                            else:
                                player.score = get_score(player.hand)
                                print(f'\n{player.name:10} : {player.score:9} : ',end="")
                                for card in player.hand:
                                    print(f'{card}',end=" ")
                                # dealer second card has been revealed pause for drama
                                time.sleep(1)
                                if player.score == 'BUST':
                                    print('\nDealer is BUST')
                                    time.sleep(2)
                                    dealer_score = player.score
                                    dealer_turn = False
                                elif player.score != 'BLACKJACK' and player.score < target:
                                    # KEEP DRAWING CARDS UNTIL WE MAKE TARGET OR BUST
                                    player.hit(game_deck.remove_one())
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
                    # With a push chips should remain on the table for next hand but I just return them to the player in this case
                    player.add_chips(amount)
                    
                elif player.score > dealer_score:
                    status = 'Win'
                    amount *= 2
                    player.add_chips(amount)
                
                else:
                    status = 'Lose'        

                # return the player cards to the game_deck
                game_deck.add_cards(player.hand)
                # remove the cards from the players hand
                player.hand.clear()
                print(f'{player} : {status:4} : {amount:3}\n')
                # i use an empty input so user can control the time delay on the game results screen
                input('Enter to continue')

            elif player.name == 'Dealer':
                game_deck.add_cards(player.hand)
                player.hand.clear()
            
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
    # Using tuple unpacking with enumerate to index menu faster
    for index,item in enumerate(menu_items):
            print(f'[{index}] - {item}')
    print('[999] - to exit at any time')
    while using_menu1:
        try:
            op = int(input('--> : '))
                
            if op == 0:
                new_game()
            elif op == 1 or op == 999:
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