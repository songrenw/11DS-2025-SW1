# random target generation
# getting algarithm
# feedback machannic - number of guesses
# data collection - simulate game
# data analysis - compute average
# data presentation - sort and print the result
import random

def binary_search_guess(target, low=1, high=100):
    # This function implements the binary search algorithm to guess the target number.
    # IT returns the number of guesses taken to find the target number.
    guesses = 0
    while low <= high:
        #make a guess using midpoint
        guess = (low + high) // 2
        #print("Guess is:", guess) # Print the guess for testing purposes
        guesses += 1

        if guess == target:
            return guesses
        elif guess < target:
            low = guess + 1
        else:
            high = guess - 1
    # should never reach here if target is in [low, high]
    return guesses
def simulate_game(num_game):
    """
    Simulate the guessing game of a given number of guess.
    Returns a dictionary with target numbers as key and a tuple of total guesses and count of games as value <- so the average is accurate(reliable) as we need to keep track of how much time a number is guess
    This function simulate the guessing game for a given number of games and keep track of total number of guesses
    and count of games for each target number
    """
    results = {n: (0, 0) for n in range(1, 101)} # Initialise results dectionary with target numbers as keys

    for _ in range(num_game):    # use _ as a throwaway varible since we don't need to loop index
        target = random.randint(1, 100) # generate a random number between 1 and 100
        #print("Target is:", target) # Print the target number for each game for testing purpose
        num_guesses = binary_search_guess(target) #Call the binary_search_guess function to guess the target number
        total, count = results[target] # get the total number of guessess and count of games for the targe number
        results[target] = (total + num_guesses, count + 1) # update the results dictionray with new vales. total store the num_guessess to it
        #print(results) # print the results for testing purpose

    return results # return the results dictionary

def compute_averages(results):
    """
    Compute the average number of guessess for each target number.
    Returns a dictionary with target numbers as keys and the average number of guesses as values.
    This function calculates the average number of guesses for each target number by divingf the total number of guessess by the count of game for that target nuber.
    """
    averages = {} #Initialise an empty dictionary to store the average number of guesses for each target number
    for number, (total_guesses, count) in results.items(): # total guesses(item[0]) and count(item[1]) is in tuple
        if count > 0:
            averages[number] = total_guesses / count
        else:
            averages[number] = None # the the average to NOne if no games were played for that target number (to avoid division by 0)
    return averages # Return the dictionary of average number of guesses for each target number

def main():
    # the main function run the simulation, computes average, sorts them for easier review and prints the result
    num_game = 1000
    results = simulate_game(num_game)
    average = compute_averages(results)

    # Define a function to extract the sorting key based on the average number of guesses
    def sorting_key(item):
        return item[1] if item[1] is not None else float('inf')
    # Soret the averages dictionary by the average number of guesses for presentation
    sorted_averages = dict(sorted(average.items(), key=sorting_key)) # this function checks if the value (item[1]) is None. If it is not None, it returns the value itself, otherwise it returns None

    print("Average number of guesses for each target number (1-100)_ over {} games:".format(num_game))
    for number, avg in sorted_averages.items():
        if avg is not None:
            print("Number {}: {:.2f} guesses on average".format(number, avg))
        else:
            print("Number {}: No games were played with this target.".format(number))

if __name__ == "__main__":
    main()