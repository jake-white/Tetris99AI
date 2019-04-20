from numpy import *
from copy import copy, deepcopy

#game data

#currentBoard and tetrominoQueue will be the two variables that need to be refreshed after each move, getting data from the capture card. 
#in order to account for delay in the capture card, we may need to run multiple moves in this program effectively blind 
#play the currentTetromino, and the next couple in the queue, before refreshing the queue). Proper integration for fast play will take some time



#given a tetromino, returns a 3D array of the possible rotation states of that tetromino
def generateRotatedList(tetromino):
    print(tetromino)
    if (array_equal(tetromino, [
    [1, 1, 0], 
    [0, 1, 1]])):
        rotatedList = [
    [
        [1, 1, 0], 
        [0, 1, 1]
    ],
    [
        [0, 1], 
        [1, 1], 
        [1, 0]
    ]]

    elif (array_equal(tetromino, [
    [0, 1, 1], 
    [1, 1, 0]])):
        rotatedList = [
    [
        [0, 1, 1], 
        [1, 1, 0]
    ],
    [
        [1, 0], 
        [1, 1], 
        [0, 1]
    ]]

    elif (array_equal(tetromino, [
    [1, 1], 
    [1, 1]])):
        rotatedList = [
    [
        [1, 1], 
        [1, 1]
    ],
    ]

    elif (array_equal(tetromino, [
    [1, 1, 1, 1] 
    ])):
        rotatedList = [
    [
        [1, 1, 1, 1] 
    ],
    [
        [1], 
        [1], 
        [1],
        [1]
    ]]

    elif (array_equal(tetromino, [
    [1, 0, 0],
    [1, 1, 1]])):
        rotatedList = [
    [
        [1, 0, 0],
        [1, 1, 1]
    ],
    [
        [1, 1], 
        [1, 0], 
        [1, 0]
    ],
    [
        [1, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 1], 
        [0, 1], 
        [1, 1]
    ]
    ]

    elif (array_equal(tetromino, [
    [0, 0, 1],
    [1, 1, 1]])):
        rotatedList = [
    [
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1, 0], 
        [1, 0], 
        [1, 1]
    ],
    [
        [1, 1, 1],
        [1, 0, 0]
    ],
    [
        [1, 1], 
        [0, 1], 
        [0, 1]
    ]
    ]

    elif (array_equal(tetromino, [
    [0, 1, 0],
    [1, 1, 1]])):
        rotatedList = [
    [
        [0, 1, 0],
        [1, 1, 1]
    ],
    [
        [1, 0], 
        [1, 1], 
        [1, 0]
    ],
    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1], 
        [1, 1], 
        [0, 1]
    ]
    ]


    return rotatedList


#returns the intitial horizontal index of a given tetromino post rotation (how far from left side). Will be either 3, 4, or 5.
def getInitialHorizontalIndex(rotatedTetromino):

    #if the initial horizontal index is 3
    if (array_equal(rotatedTetromino,[
    [1, 1, 1, 1]
    ]) 
    or (array_equal(rotatedTetromino,[
    [1, 0, 0],
    [1, 1, 1]]))
    or (array_equal(rotatedTetromino,[
    [0, 0, 1],
    [1, 1, 1]]))
    or (array_equal(rotatedTetromino,[
    [0, 1, 1],
    [1, 1, 0]]))
    or (array_equal(rotatedTetromino,[
    [0, 1, 0],
    [1, 1, 1]]))
    or (array_equal(rotatedTetromino,[
    [1, 1, 0],
    [0, 1, 1]]))
    or (array_equal(rotatedTetromino,[
    [1, 1, 1],
    [0, 0, 1]]))
    or (array_equal(rotatedTetromino,[
    [1, 1, 1],
    [1, 0, 0]]))
    or (array_equal(rotatedTetromino,[
    [1, 1, 1],
    [0, 1, 0]]))
    or (array_equal(rotatedTetromino,[
    [0, 1],
    [0, 1],
    [1, 1]]))
    or (array_equal(rotatedTetromino,[
    [1, 1],
    [0, 1],
    [0, 1]]))
    or (array_equal(rotatedTetromino,[
    [0, 1],
    [1, 1],
    [0, 1]]))
    
    ):
        return 3


    #if the initial horizontal index is 4
    elif (array_equal(rotatedTetromino,[
    [1, 1],
    [1, 1]
    ])
    or (array_equal(rotatedTetromino,[
    [1, 1],
    [1, 0],
    [1, 0]]))
    or (array_equal(rotatedTetromino,[
    [1, 0],
    [1, 0],
    [1, 1]]))
    or (array_equal(rotatedTetromino,[
    [1, 0],
    [1, 1],
    [0, 1]]))
    or (array_equal(rotatedTetromino,[
    [1, 0],
    [1, 1],
    [1, 0]]))
    or (array_equal(rotatedTetromino,[
    [0, 1],
    [1, 1],
    [1, 0]]))
  
    ):
        return 4


    #if the initial horizontal index is 5
    elif (array_equal(rotatedTetromino,[
    [1],
    [1],
    [1],
    [1]
    ])
        
    ):
        return 5




#Height analysis functions (for tetromino's, boards, and determining collisions)

# takes in the current Tetromino and returns a height map (how far down does each column of the piece extend)
# examples:
# [1,1,1,1] returns [1,1,1,1]
# [1,1,1],
# [0,1,0] returns [1,2,1]
# [1,1],
# [1,1] returns [2,2]
# [0,1],
# [1,1],
# [1,0] returns [3,2]
def CTHeight(currentTetromino):
    # (height, width) of currentTetromino 2D array
    dimensions = currentTetromino.shape
    # will hold heightList, will be returned
    heightList = []
    # for each column of tetromino
    for i in range(0, dimensions[1]):
        # columnHeight initialized to 0
        columnHeight = 0
        # iterate down through each row of current column
        for j in range(0, dimensions[0]):
            # if the current space contains a block (is a 1, not a 0),
            # columnHeight is set to j+1 (+1 is to account for 0 indexing of arrays)
            if currentTetromino[j][i] == 1:
                columnHeight = j + 1
        # append the columnHeight to the heightList
        heightList.append(columnHeight)
    return heightList


#takes in the currentBoard and returns a heightmap (highest block for each column)
#example: currentBoard is 
#...
#    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
#    [1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
#    [1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
#    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1]

#    [3, 3, 2, 2, 3, 4, 3, 1, 0, 4] will be the return value
def boardHeight(currentBoard):
    # will hold heightList, will be returned
    heightList = []
    # for each column of board
    for i in range(10):
        # columnHeight initialized to 0
        columnHeight = 0
        # iterate up through each row of current column, until the top (0)
        for j in range(19, -1, -1):
            # if the current space contains a block (is a 1, not a 0),
            # columnHeight is set to 20 - j
            if currentBoard[j][i] == 1:
                columnHeight = 20 - j 
        # append the columnHeight to the heightList
        heightList.append(columnHeight)
    return heightList


#returns a list of how many spaces down the current tetromino can move before it makes contact with a piece on the board (collision). 
#Indexed to go from leftmost to rightmost side. Since some tetrominos are wider than others, the list can have a variable length:
#up to 10 if the tetromino is width 1 (a height difference for each column), as small as 7 if teromino is width 4
# First element will always represent the furthest left the tetromino can be, last element the furthest right. 
#example return: [15, 15, 16, 15, 14, 14, 15, 17, 14]
#takes in the currentTetromino and heightLists for it and the board
def minHeightDiff(currentTetromino, CTHeightList, CBHeightList):
    #list of minimum height differences, left to right, will be returned.
    heightDiffList = [] 
    #tetrominoDimensions[1] will be width of current tetromino
    tetrominoDimensions = currentTetromino.shape
    #start at left of board, go right until you hit the wall with the current tetromino, accounting for variable width
    for i in range(0, 10 - (tetrominoDimensions[1] - 1)):
        #height differences for each column of the tetromino
        heightDiffs = []
        #cycle through each column of the currentTetromino
        for j in range(0, len(CTHeightList)):
            #calculate the height difference between bottom of tetromino and highest piece of board FOR THIS COLUMN
            heightDiff = 20 - (CTHeightList[j] + CBHeightList[i+j])
            heightDiffs.append(heightDiff)
        #the minHeightDiff is how far the tetromino can be moved down before contacting a board piece. Append to the final heightDiffList
        minHeightDiff = min(heightDiffs)
        heightDiffList.append(minHeightDiff)
    return heightDiffList





#AI Stuff (Node/State Generation and Heuristic Analysis)

#will return a 3D array (2D array of all possible boards/moves with the current Tetromino). 
#assumes direct drops only
def generatePossibleBoards(currentTetromino, currentBoard, heightDiffList):
    #array will hold 2D array boards and be returned
    possibleBoards = []
    #height and width of currentTetromino
    dimensions = currentTetromino.shape
    #used to make the tetromino increment/travel rightwards, for each possible move
    count = 0 
    #for each minHeight (distance Tetromino must travel down before collision), create a possible board
    for minHeight in heightDiffList:
        #testBoard must be a COPY of the current board, not a reference to it
        testBoard = deepcopy(currentBoard)
        # for each column of tetromino
        for i in range(0, dimensions[1]):
            # iterate down through each row of current column
            for j in range(0, dimensions[0]):
                #adding the tetromino to the board. Coordinates use j and i, and BOARD coordinate is offset by minHeight (how far down to move piece) and count (how far right to move piece)
                testBoard[j + minHeight][i+count] += (currentTetromino[j][i])
        count += 1 #right one
        possibleBoards.append(testBoard) #append to final returned possibleBoards list
    return(possibleBoards)


#given a board state, computes number of complete lines
def computeCompleteLines(board):
    #number of complete lines initialized to 0
    completeLines = 0
    #for each row/line of the board, check if it is complete (all 1s)
    for row in range (20):
        #complete initialized to True, switched to False if 0 is in line
        complete = True
        #for each column in line
        for column in range(10):
            #if 0 is found, line isn't complete, break the loop
            if (board[row][column]) == 0:
                complete = False
                break
        #if the line is complete, increment completeLines
        if (complete):
            completeLines = completeLines + 1
    return (completeLines)


#computes and returns the number of holes in the board (0s with 1s somewhere above them)
def computeHoles(board, boardHeightList):
    #we need the indexes of the height coordinates, e.g., not 0 for the bottom, but 19
    heightIndexList = []
    for i in range (size(boardHeightList)):
        heightIndexList.append(20 - boardHeightList[i])

    #number of holes initialized to 0
    holes = 0
    #for each column of the board
    for column in range (10):
        #check each row, from the index of the highest 1 in the column down to the bottom of the board. If a 0 is found, it by definition has a 1 above it and is a hole
        for row in range(heightIndexList[column], 20):
            if (board[row][column] == 0):
                holes = holes + 1 #increment hole counter
    return holes


#computes and returns the variation between adjacent column heights (bumpiness, wells, etc). 
#a relatively flat grid is desirable as there is less risk to create holes
def computeBumpiness(boardHeightList):
    bumpinessTotal = 0
    #only for i in range 9 becuase last column is reached via i+1
    for i in range (9):
        #variation between columnHeight and the next
        variation = abs(boardHeightList[i] - boardHeightList[i+1])
        #add variation to the bumpinessTotal
        bumpinessTotal = bumpinessTotal + variation
    return(bumpinessTotal)


#returns the heuristic value of a board, taking into account:
#aggregate height, complete lines, holes, and bumpiness
def computeHeuristicVal(board):
    boardHeightList = boardHeight(board)

    #4 heuristics
    aggregateHeight = sum(boardHeightList)
    completeLines = computeCompleteLines(board)
    holes = computeHoles(board, boardHeightList)
    bumpiness = computeBumpiness(boardHeightList)

    #parameters/values to multiply each heuristic by, since the scales and level of importance are not equal
    ParamAggregateHeight = -0.5
    ParamCompleteLines = 0.75   #positive because this should be maximized, not minimized!
    ParamHoles = -0.33
    ParamBumpiness = -0.2
    
    #puts heuristic together into value to evaluate (higher is better)
    heuristicVal = ParamAggregateHeight * aggregateHeight + ParamCompleteLines * completeLines + ParamHoles * holes + ParamBumpiness * bumpiness

    #print("A Test Board (NOT currentBoard; currentTetromino is placed)")
    #print(board)
    #print("Aggregate Height: ", aggregateHeight)
    #print("Complete Lines: ", completeLines)
    #print("Holes: ", holes)
    #print("Bumpiness: ", bumpiness)
    #print("Heuristic Value: ", heuristicVal, "\n")

    return heuristicVal




#driver functions

#given a tetromino in a specific rotation state, computes all positions it can be placed on the board and calls to compute the heuristic values of each board state
#returns a list of said heuristic values
def computeMove(currentTetromino):
    # get heightList of tetromino
    CTHeightList = CTHeight(currentTetromino)
    #print ("Current Tetromino Height List: ", CTHeightList)
    CBHeightList = boardHeight(currentBoard)
    #print ("Current Board     Height List: ", CBHeightList)
    heightDiffList = minHeightDiff(currentTetromino, CTHeightList, CBHeightList)
    #print("Height Difference (CB)   List: ", heightDiffList)
    possibleBoards = generatePossibleBoards(currentTetromino, currentBoard, heightDiffList)
    #print(possibleBoards)
    #will hold heuristic value for each possibleBoard
    heuristicValList = []
    for board in range(len(possibleBoards)):
        heuristicValList.append(computeHeuristicVal(possibleBoards[board]))
    return heuristicValList


# computes the best move for all rotation states of a given tetromino
# returns the heuristic value of that state, how many rotations of the tetromino are needed, and the horizontal index of that state how many moves right from furthest left the tetromino can be)
def generateTupleHeurData(currentTetromino):
    #get a 3D array back (array of the tetromino in all it's rotation states)
    rotatedList = generateRotatedList(currentTetromino)
    #2D array, an array of all moves for each rotation state of the tetromino
    heuristicVal2D = []
    #for each rotation state, compute what the best move would be
    for i in range(len(rotatedList)):
        rotatedList[i] = array(rotatedList[i])
        heuristicValList = computeMove(rotatedList[i])
        heuristicVal2D.append(heuristicValList)
    #for i in range(len(heuristicVal2D)):
        #print ("Heuristic Value List, Rotations", i, ":",heuristicVal2D[i])

    #will hold the max heuristic value of each rotation state
    bestHeurList = []
    #will hold the indexes of said maximum heurisitics
    bestHeurIndexList = []
    #for each of the lists in heurisitcVal2D (each rotation)
    for i in range(len(heuristicVal2D)):
        #the bestMove is the board with the maximum heuristic
        bestHeurList.append(max(heuristicVal2D[i]))
        #numpy.argmax gets the index of said maximum heuristic
        bestHeurIndexList.append(argmax(heuristicVal2D[i]))

    #The highest heuristic value, accounting for rotations
    bestHeurVal = max(bestHeurList)
    #how many rotations are needed for the tetromino to be in the orientation it is in for the bestHeurValue
    bestHeurValRotations = argmax(bestHeurList)
    #index of the maximum heuristic value in the specific list for a rotation state of a tetromino. E.G., if 0, tetromino is placed as far left as possible
    bestHeurValHorizontalIndex = argmax(heuristicVal2D[bestHeurValRotations])

    return bestHeurVal, bestHeurValRotations, bestHeurValHorizontalIndex


def generatePostMoveBoard(currentTetromino, bestHeurValRotations, bestHeurValHorizontalIndex):
    #get a 3D array back (array of the tetromino in all it's rotation states)
    rotatedList = generateRotatedList(currentTetromino)
    #rotatedTetromino is the currentTetromino in the correct rotation state for the chosen move
    rotatedTetromino = rotatedList[bestHeurValRotations]
    rotatedTetromino = array(rotatedTetromino)
    #height and width of rotatedTetromino
    dimensions = rotatedTetromino.shape
    
    # get heightList of tetromino and board, then get height difference list with that
    RTHeightList = CTHeight(rotatedTetromino)
    CBHeightList = boardHeight(currentBoard)
    heightDiffList = minHeightDiff(rotatedTetromino, RTHeightList, CBHeightList)
    # how far down rotatedTetromino goes for the chosen best move
    heightOffset = heightDiffList[bestHeurValHorizontalIndex]


    #testBoard must be a COPY of the current board, not a reference to it
    testBoard = deepcopy(currentBoard)
    # for each column of tetromino
    for i in range(0, dimensions[1]):
        # iterate down through each row of current column of tetromino
        for j in range(0, dimensions[0]):
            #adding the tetromino to the board. Coordinates use j and i, and BOARD coordinate is offset by heightOffset (how far down to move piece) and bestHeurValHorizontalIndex (how far right to move piece)
            testBoard[j + heightOffset][i + bestHeurValHorizontalIndex] += (rotatedTetromino[j][i])

    #remove complete lines from testboard
    testBoard = clearCompleteLines(testBoard)

    postMoveBoard = testBoard
    return(postMoveBoard, rotatedTetromino)


def clearCompleteLines(testBoard):

    #for each row/line of the board, check if it is complete (all 1s)
    for row in range (20):
        #complete initialized to True, switched to False if 0 is in line
        complete = True
        #for each column in line
        for column in range(10):
            #if 0 is found, line isn't complete, break the loop
            if (testBoard[row][column]) == 0:
                complete = False
                break
        #if the line is complete, increment completeLines
        if (complete):
            #delete the row from the board (0 means axis is row)
            testBoard = delete(testBoard, row, 0)
            #add new row of all blanks to top
            testBoard = insert(testBoard, 0, 0, axis=0)

    return testBoard

def get_command(actual_tetrominoQueue, actual_currentBoard):
    #must be global so that it can be changed within main
    global tetrominoQueue
    global currentBoard

    tetrominoQueue = actual_tetrominoQueue
    currentBoard = actual_currentBoard
    
    for i in range(len(tetrominoQueue)):
        print("Current Board")
        print(currentBoard)
        # assign the current tetromino to be the tetromino at the top of the queue
        #currently, can test different tetrominos by changing index
        currentTetromino = tetrominoQueue[0]
        # delete the first/top tetromino from the queue (the currentTetromino)
        tetrominoQueue = delete(tetrominoQueue, 0)
        # has to be of type numpy array, not list
        currentTetromino = array(currentTetromino)

        #tuple contains best move heuristic value, rotations needed, and horizontal index
        tupleHeurData = generateTupleHeurData(currentTetromino)

        print("Best Move Heuristic Value: ", tupleHeurData[0])
        print("Rotations Needed:", tupleHeurData[1])
        print("Horizontal Index:", tupleHeurData[2])

        #will be the resulting board (2D array) after best move is executed
        postMoveBoard = generatePostMoveBoard(currentTetromino, tupleHeurData[1], tupleHeurData[2])
        currentBoard = postMoveBoard[0] #update currentboard
        rotatedTetromino = postMoveBoard[1] #get rotated tetromino

        #now, we have to send inputs to the switch
        #due to the rotation system of tetris, rotating a piece will change the horizontal position of its leftmost component (it will get further away from the left). Indexes are based on the left, so getInitialHorizontalIndex returns the initial horizontal index of a tetromino after it has been rotated properly
        initialHorizontalIndex = getInitialHorizontalIndex(rotatedTetromino)

        #now, to calculate moves, we need to find the difference between the index of the best move and the tetromino's initial index. This value represents number of moves right to send to the switch. If 0, none. If negative, that number of lefts.
        horizontalMoves =  tupleHeurData[2] - initialHorizontalIndex
        print("Horizontal Moves:", horizontalMoves)

        #inputs to send to the switch: rotate tupleHeurData[1] number of times, move left/right based on horizontal moves, then hard drop
        return [[horizontalMoves, tupleHeurData[1]]]
        

    #If that is too slow (too many inputs for switch), we could have a function that, given a rotated tetromino, returns which horizontal index it is in after entering the board and rotating. The result will be 3, 4, or 5. Then, we have the horizontal index of the best move, so the difference is found to compute the inputs necessary. 

if __name__ == '__main__':
    get_command()




#to-do
#switch, when generating currentBoard, should ignore the currentTetromino (ignore pieces at top of board that aren't in contact with another piece below them?). Could be done here or in C code

#optional
#if all heuristic values of possible boards are X amount worse than currentBoard, then evaluate holding the current piece (only execute if this brings an improvement)
#holes parameter should be more intense?...