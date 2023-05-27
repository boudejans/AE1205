import random

board = [["." for i in range(6)] for j in range(7)]


# Print the board in a nice format
def ShowBoard(board):
    row = ""
    for i in range(6):
        for j in range(7):
            row += board[j][i] + "\t"
        print(row)
        row = ""
    bottom = ""
    for k in range(1, 8):
        bottom += str(k) + "\t"
    print(bottom)


# Drop a disc in the given column
def DropDisc(board, col, disc):
    # Check if the column number is between 1 and 7, else the input is invalid
    if col < 1 or col > 7:
        return "Invalid"
    # Go through each of the 6 positions in a column
    for i in range(6):
        if board[col - 1][i] != ".":
            # If the first position of a column is full, then the column is full
            if i == 0:
                # If the first position of each of the 6 columns is full, then the board is full
                for j in range(0, 6):
                    if board[j][0] == ".":
                        return "Col Full"
                return "Full"
            board[col - 1][i - 1] = disc
            return "Success"
        if i == 5:
            board[col - 1][i] = disc
            return "Success"


# Check for 4 in a row
def CheckForWin(board):
    col_index = 0
    # Go through each column on the board
    for col in board:
        vert_player = ""
        horz_player = ""
        diag_down_player = ""
        diag_up_player = ""
        vert_count = 0
        horz_count = 0
        diag_down_count = 0
        diag_up_count = 0
        row_index = 0
        # Go through each row on the board
        for row in col:
            # If the space is not empty
            if row != ".":
                # Check for 4 row entries in a column
                if row_index <= 2:
                    for j in range(4):
                        if col[row_index + j] == vert_player:
                            vert_count += 1
                        else:
                            vert_player = col[row_index + j]
                            vert_count = 0
                    if vert_count == 3:
                        return vert_player
                # Check for 4 column entries in a row
                if col_index <= 3:
                    for j in range(4):
                        if board[col_index + j][row_index] == horz_player:
                            horz_count += 1
                        else:
                            horz_player = board[col_index + j][row_index]
                            horz_count = 0
                    if horz_count == 3:
                        return horz_player
                # Check for 4 diagonally down entries from maximally point (4,3)
                if col_index <= 3 and row_index <= 2:
                    for j in range(4):
                        if board[col_index + j][row_index + j] == diag_down_player:
                            diag_down_count += 1
                        else:
                            diag_down_player = board[col_index + j][row_index + j]
                            diag_down_count = 0
                    if diag_down_count == 3:
                        return diag_down_player
                # Check for 4 diagonally up entries from maximally point (4,4)
                if col_index <= 3 and row_index >= 3:
                    for j in range(4):
                        if board[col_index + j][row_index - j] == diag_up_player:
                            diag_up_count += 1
                        else:
                            diag_up_player = board[col_index + j][row_index - j]
                            diag_up_count = 0
                    if diag_up_count == 3:
                        return diag_up_player
            row_index += 1
        col_index += 1


# Calculate what happens when the game is played out randomly
def CalculateGame(testBoard):
    result = None
    # While there is no result yet, keep dropping in discs in random positions till there is a winner or draw
    while result is None:
        result = CheckForWin(testBoard)
        if DropDisc(testBoard, random.randint(1, 8), "O") == "Full":
            result = "Draw"
        if DropDisc(testBoard, random.randint(1, 8), "X") == "Full":
            result = "Draw"
        # print(result)
    return result


# Calculate the score when the game is played from one starting column for count times
def CalculateColumnScore(startBoard, startcol, count):
    score = 0
    # Reset the board and put a disc in the starting column
    for i in range(count):
        testBoard = [x[:] for x in startBoard]
        DropDisc(testBoard, startcol, "X")
        result = CalculateGame(testBoard)
        if result == "O":
            score -= 1
        elif result == "X":
            score += 1
    # print(str(startcol) + " - " + str(score))
    return score


# Calculate the best starting column
def CalculateBestMove(test_board):
    highest_score = -1001
    best_column = 0
    # Calculate the score for each of the 7 columns
    for i in range(1, 8):
        score = CalculateColumnScore(test_board, i, 400)
        if score > highest_score:
            highest_score = score
            best_column = i
    return best_column


while True:
    # Check if someone won
    result = CheckForWin(board)
    ShowBoard(board)
    if result != None:
        print("Player " + result + " won!")
        exit()
    choice = input("Choose a column to drop a disc in [1-7]: ")
    if choice == "":
        print("Enter a number between 1 and 7")
    else:
        state = DropDisc(board, int(choice), "O")
        result = CheckForWin(board)
        if result != None:
            ShowBoard(board)
            print("Player " + result + " won!")
            exit()
        if state == "Success":
            # Old 'AI':
            # DropDisc(board, random.randint(1,8), "X")

            # New 'AI':
            best_column = CalculateBestMove(board)
            DropDisc(board, best_column, "X")
        elif state == "Invalid":
            print("This is not a valid column!")
        elif state == "Col Full":
            print("This column is already full!")
        elif state == "Full":
            print("Board is full! It's a draw!")
