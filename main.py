# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import copy
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = random.randint(5,10)

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word_lower = word.lower();
    result = 0;
    first_component = 0
    second_component = 0
    for i in range(len(word_lower)):
      # compute first half of the formula determine the letter are valid letter and get their value
      if ord(word_lower[i]) > 96 and ord(word_lower[i])<(123):
        first_component += SCRABBLE_LETTER_VALUES.get(word_lower[i])
    # compute second part 
    second_component = 7 * len(word_lower) - 3 * (n - len(word_lower))
    if second_component <= 1:
      second_component = 1;
    result = first_component * second_component
    return result;
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    x = '*'
    hand[x] = hand.get(x,0) + 1
    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    result = dict();
    result = copy.deepcopy(hand)
    
    word_lower = word.lower();

    for i in word_lower:
      # remove the letter from hand
      if i in result.keys():
        result[i] = result.get(i,0) - 1;
        if result[i] < 0:
          result[i] == 0
          
    return result
    


          
        
          

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_lower = word.lower();
    word_lower_unit = list(word_lower)
    # base case of word not contain a star and word is not in word list
    if word_lower not in word_list and '*' not in word_lower_unit:
      return False
    # determine if there is a star
    star_flag = False;
    # there is a star then replace star with every vowel, and check if it is in word list
    if '*' in word_lower_unit:
      star_index = word_lower_unit.index('*')
      for i in VOWELS:
        word_lower_unit[star_index] = i
        word_lower = ''.join(word_lower_unit)
        if word_lower in word_list:
          star_flag = True
      # did not form any word by replacing star with 5 vowels, just exit
      if star_flag == False:
        return False


    temp_dict = dict();
    temp_dict = copy.deepcopy(hand)
    word_lower = word.lower();

    # determine if hand is suffient for the word
    for i in word_lower:
      # letter in hand is not suffient
      if i in temp_dict.keys():
        if temp_dict.get(i,0) <= 0:
          return False
      # letter is not in hand
      elif(i not in temp_dict.keys()):
        return False
      # remove one letter from dictionary
      temp_dict[i] -= 1;
    
    return True


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count = 0;
    for i in hand:
      if hand.get(i,0) != 0:
        count += 1;
    
    return count

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    total_score = 0;
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
    temp_hand = copy.deepcopy(hand)
    while calculate_handlen(temp_hand) > 0:
        # Display the hand
        
        # print("current hand: ",end= '')
        # display_hand(temp_hand)
        # Ask user for input
        current_word = input("please give a combination from your hand or enter '!!' to stop: ")
        # If the input is two exclamation points:
        if current_word == "!!":
          break;
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:
        if is_valid_word(current_word,temp_hand,word_list):
            temp_score = get_word_score(current_word,calculate_handlen(temp_hand))
                # Tell the user how many points the word earned,
            
                # and the updated total score
            total_score += temp_score;
            print("your score of (" + str(current_word) + ") is: " + str(temp_score) + " total score is: " + str(total_score))
            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
        else:
            print("please give a valid word!")
        temp_hand = update_hand(temp_hand,current_word)
        
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print("you total score is: " + str(total_score))
    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    #return right away when user enter a letter not in hand
    if letter not in hand.keys():
      return hand

    temp_hand = copy.deepcopy(hand)

    # get how many piece of letter are in hand
    letters_in_hand = temp_hand.get(letter,0)
    
    #put two lists together and generate a random index
    index = random.randint(0,25)
    temp_hand.pop(letter,None)
    join_alphabets = VOWELS + CONSONANTS
    temp_letter = join_alphabets[index]

    # check if we generate a random letter that is not in hand and not the original letter 
    while temp_letter in temp_hand.keys() or temp_letter == letter:
      index = random.randint(0,25)
      temp_letter = join_alphabets[index]
    temp_hand[temp_letter] = letters_in_hand

    return temp_hand
    
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands
    
    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    #number of Hands
    number_hands = int(input("enter how many total hands do you like to play: "))
    # two flags to determine if player use their chance of substitute or replay
    substitute_flag = False
    replay_flag = False;
    remember_from_replay = False
    total_score = 0
    remember = {}
    # repeat up to player's choice of play
    while number_hands > 0:
      current_score = 0
      # retrieve same hand if user wants to replay previous hand
      current_hand = deal_hand(HAND_SIZE);
      if remember_from_replay == True:
        remember_from_replay = False
        current_hand = remember
      # display every hand for user 
      print("current hand: ",end= '')
      display_hand(current_hand);
      # if false means user can use his chance of substitute
      if substitute_flag == False:
        sub = input("Would you like to substitute a letter? ")
        if sub == "yes":
          substitute_flag = True
          picked_letter = input("please enter the letter that you would like to change: ")
          current_hand = substitute_hand(current_hand,picked_letter)
      # main function for play game
      current_score = play_hand(current_hand,word_list)
      print("----------------------")
      # if false means user can use his chan of replay
      if replay_flag == False:
        rep = input("Would you like to replay this hand? ")
        # remember the current hand and store in remember
        if rep == "yes":
          replay_flag = True
          remember_from_replay = True
          remember = current_hand
          continue;



      total_score += current_score
      number_hands -= 1;
    
    print("Total score of all hands: " + str(total_score)) 
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    # temp_hand = {'a': 1,'j':1,'e':1,'f':1,'*' : 1,'r' : 1,'x' : 1}
    # temp_hand2 = {'a': 1,'c':1,'f':1,'i':1,'*' : 1,'t' : 1,'x' : 1}
    # play_hand(temp_hand,word_list)
    # print(temp_hand)
    # print(substitute_hand(temp_hand,'a'))
    play_game(word_list)