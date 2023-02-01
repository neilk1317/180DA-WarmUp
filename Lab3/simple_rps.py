import random

choices = ['rock', 'paper', 'scissors']
print("Welcome to Rock-Paper-Scissors!")
print("When prompted, make you're move by typing 'rock', 'paper', or 'scissors'. \nTo quit the game enter 'q'.")

while True:
    start = input("Proceed to game? (y/n): ")
    if start == 'y':
        break
    elif start == 'n':
        quit()
    else:
        print("Invalid response! Please input 'y' or 'n'")

while True:
    move = input("Enter your move: ")
    cpu_move = random.choice(choices)
    if move in choices:
        print('You: ' + move + '\nCPU: ' + cpu_move)
        if move == cpu_move:
            print('Tie!')
        elif (move == 'rock' and cpu_move == 'paper') or (move == 'paper' and cpu_move == 'scissors') or (move == 'scissors' and cpu_move == 'rock'):
            print('You lost :(')
        else:
            print('You win!!!')
        print('\n')
    elif move == 'q':
        print('Quitting...')
        quit()
    else:
        print("Invalid response! Please input a move in ", choices, " or 'q' to quit.")
        

