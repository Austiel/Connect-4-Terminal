# from os import system

def printBoard(board: list):
    '''Prints the board on the terminal.'''
    # system('cls')
    print(' _______________________________________')
    for y in board[::-1]:
        row = ''
        for x in y:
            if x == 0: row += "|   "
            elif x == 1: row += f"| ○ "
            elif x == 2: row += f"| ● "
        print(row + '|')
    print(' ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n  0   1   2   3   4   5   6   7   8   9\n')

def boardChecker(board: list, player: int, coord: tuple): # Coord is (y, x)   
    '''Checks the board if the player who just made the turn has won'''
    counter_map = {}
    for i in range(1, 4): # Starts from index 1 because we already know that index 0 is the player
        #   bools to check if a cell is not out of range   #
        left = coord[1] - i >= 0
        right = coord[1] + i < len(board[0])
        down = coord[0] - i >= 0
        up = coord[0] + i < len(board)
        
        #   Check horizontally  #
        if right: counter_map['hor'] = counter_map.get('hor','') + str(board[coord[0]][coord[1] + i]) # To the right
        if left: counter_map['hor'] = str(board[coord[0]][coord[1] - i]) + counter_map.get('hor','') # To the left
        
        #   Check Vertically; Checking vertically always goes downwards #
        if down: counter_map['ver'] = counter_map.get('ver','') + str(board[coord[0] - i][coord[1]])

        #   /Check Diagonally/    #
        if up and right: counter_map['/'] = counter_map.get('/','') + str(board[coord[0] + i][coord[1] + i]) # / Upward
        if down and left: counter_map['/'] = str(board[coord[0] - i][coord[1] - i]) + counter_map.get('/','') # / Downward
        #   \Check Diagonally\    #
        if up and left: counter_map['\\'] = str(board[coord[0] + i][coord[1] - i]) + counter_map.get('\\','') # \ Upward
        if down and right: counter_map['\\'] = counter_map.get('\\','') + str(board[coord[0] - i][coord[1] + i]) # \ Downward

    # Checks if any value in counter_map (dict) is the same as str(player) * 3
    # Ex. If player is 1, then the string would be '111'
    if any([str(player) * 3 in x for x in counter_map.values()]):
        return True # Returns True, indicating a player's win
    return False
            

def gameOver(win: bool, player: int, p_wins: dict):
    '''Prints a game over message on the terminal and asks if the player(s) wants to play again.'''
    if win:
        msg = (f"Player {player} won!")
        p_wins[player] = p_wins.get(player, 0) + 1
    else: msg = ("No more slot!")
    print((f'{msg:^41}\n'
    '|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|\n'
    '               Score board\n\n'
    f'{f"player 1   {p_wins.get(1, 0)}":^41}\n'
    f'{f"player 2   {p_wins.get(2, 0)}":^41}\n'
    '|_______________________________________|\n'
    '                Game Over'))

    while True:
        i = input('\nPlay again? Y or N: ')
        if i in 'Yy': return play(p_wins)
        elif i in 'Nn': 
            print("Thanks for playing!")
            break
        else: print('Invalid input')
    

def play(p_wins = {}):
    '''This is the main loop. Takes in a dictionary of player scores/wins.
        Default parameter: p_wins = {} (an empty dictionary)'''

    # Creates a 10x10 board
    board = [[0 for i in range(10)] for i in range(10)]

    player = 1
    win = False
    while not win:
        printBoard(board)

        try:
            x_axis = int(input(f"Player {player}'s Turn: "))
            # Raises ValueError if input (x_axis) is not more than -1 and not less than the length of the board rows
            # or if the top of chosen column is taken.
            if not -1 < x_axis < len(board[0]) or board[len(board) - 1][x_axis] != 0:
                raise ValueError
        except ValueError:
            print("\nINVALID CHOICE!")
            continue

        coord = () # (y, x)
        for y_axis, elem in enumerate(board):
            if elem[x_axis] == 1 or elem[x_axis] == 2: continue
            elem[x_axis] = player
            coord = (y_axis, x_axis)
            break

        win = boardChecker(board, player, coord)
        if win or 0 not in board[-1]: break

        if player == 1: player = 2
        else: player = 1
    printBoard(board)
    gameOver(win, player, p_wins)

if __name__ == "__main__":
    play()