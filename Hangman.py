import random
import os
import json 

score = 100 # default score

def load_word_list():
    global words, difficulty 
    json_file_path = os.path.join("game_config.json") # variable contains the json file
    with open(json_file_path, "r") as file:
        words_dictionary = json.load(file)
    return words_dictionary # returns the variable value to the function

def set_difficulty_settings(selected_difficulty): 
    global words, difficulty, tries
    words_dictionary = load_word_list() 
    if not words_dictionary: # if the JSON file is invalid
        return False # returns the value of false to the function
    difficulty = selected_difficulty 
    difficulty_settings = words_dictionary['game_settings'][difficulty] # goes through the "game_settings" in the json file and accesses the difficulties
    words = difficulty_settings['words'] # captures the words of the desired difficulty in the JSON file
    tries = difficulty_settings['max_attempts'] # captures the attempts of the desired difficulty in the JSON file
    return True

def check_guess(guess, word, display): 
    found = False
    for position in range(len(word)): # loops the same amount of letters there is in the word
        if word[position] == guess:
            display[position] = guess # the not_guessed_letter position of the guess is replaced with the guessed letter
            found = True # updates the variable that a hidden letter has been found
        if word[position] == " ": # if any position in the hidden word has a space
            display[position] = " " # replaces the not_guessed_letter position with a space if the position of that letter has a space, not a letter
    return found # returns the value that found contains and connects that value to the function 

def hint():
    get_position = [] 
    for position in range(len(hidden_word)): # loops depending on how many letters the hidden word has
        if not_guessed_letter[position] == "_": # if there is still hidden letters
            get_position.append(position) # adds the indexes which are the positions of the hidden letters into get_position
    random_position = random.choice(get_position) # picks out a random position of the get_position
    reveal_letter = hidden_word[random_position] # captures the letter of the chosen position because of random_position 

    print(f"\nHint: {reveal_letter} is in the word") # f string used to add variables into the string.

def play_game(): # main function
    global hidden_word, not_guessed_letter, score, tries # all these variables are outside the function so these variables need to be global
    hidden_word = random.choice(words)
    length_word = len(hidden_word) # captures the amount of indexes of the hidden word
    not_guessed_letter = ["_"] * length_word # "*" is a times symbol and the underscores are duplicated by the number of letters the hidden word has
    guessed_letters = []
    check_guess(" ", hidden_word, not_guessed_letter) # " " is in the guess parameter and the funciton is called so that the user doesn't need to guess space
    print(f"\nThe word has {length_word} letters\nYou have {tries} lives\nYour score is {score}\n")
    while tries > 0: # main game loop

        try: # try makes it so if the user inputs something other then a string, exceptions can be added
            print(" ".join(not_guessed_letter)) # the variable joins this string and the space in this string is to seperate the underscores from each other
            guess = input("Guess the word or buy a hint: ").lower() # variable contains the user input
            if guess == "hint":
                if score >= 50:
                    score -= 50
                    hint() # calls the hint function
                    print(f"\nYour score is now {score}")
                    continue 
                else: # if the user's score isnt enough to buy a hint which is above 50
                    print("You do not have enough points\n")
                    continue
            if len(guess) != 1: # captures the length of the guess and if their guess has more than 1 letter
                print("\nYou can only guess 1 letter at a time\n")
                continue # continue is used to replay the loop
            if guess in guessed_letters:
                print(f"\nYou have already guessed {guess}\n")
                continue

            guessed_letters.append(guess) # gets the user's guess and stores it in another variable
            print(f"\nLetters you have guessed: {guessed_letters}")

            if check_guess(guess, hidden_word, not_guessed_letter): # the variables within the brackets are connected to the check_guess parameters
                if score >= 0: 
                    score += 10
                print(f"Good guess! '{guess}' is in the word, 10 points awarded!.\n\nYou have {tries} lives\nYour score is {score}\n")
            else: # if the check_guess function is false
                tries -= 1 
                if score > 0: 
                    score -= 10
                print(f"Wrong guess! '{guess}' is not in the word, 10 points lost!\n\nYou have {tries} lives\nYour score is {score}\n")

            if "_" not in not_guessed_letter: # if there is no "_" it means that all of the letters of the hidden word has been guessed
                print(f"You win, The word was {hidden_word}")
                while True:
                    replay = input("Would you like to quit or go back to menu (quit/menu): ").lower()
                    if replay == "menu":
                        main_menu() 
                        return # breaks out of the function loop
                    if replay == "quit":
                        return
            if tries == 0:
                print(f"You lose\n\nThe word was {hidden_word}\n")
                while True:
                    replay = input("Would you like to quit or go back to menu (quit/menu): ").lower()
                    if replay == "menu":
                        main_menu()
                        return
                    if replay == "quit":
                        return

        except KeyboardInterrupt:
            break

def main_menu():
    print("\nWELCOME TO THE HANGMAN GAME")
    print("\nRULES AND HOW TO PLAY")
    print("1. Type only one letter when guessing a word")
    print("2. Hints cost 50 points")
    print("3. To buy a hint, type hint when guessing a word")
    while True:
        play = input("\nWould you like to play (Y/N): ").lower() 
        if play == "y":
            while True:
                difficulty_choice = input("What difficulty do you want to play (easy, medium, hard): ").lower()
                if difficulty_choice in ["easy", "medium", "hard"]:
                    if set_difficulty_settings(difficulty_choice): # if what the user's desired difficulty is inside of the json file
                        play_game() 
                        break
                    else: # if what the user's desired difficulty isn't inside the json file
                        print("Failed to set difficulty. Please try again.")
                else:
                    print("Please choose easy, medium, or hard")
                    continue
            break
        if play == "n":
            print("Goodbye!")   
            break
        else:
            print("Input Y or N")
            continue

main_menu()






            