#Aarushi Wadhwa - aarushiw

### TETRIS ###

# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random
import string
import copy

####################################
# customize these functions
####################################

def playTetris():
    (rows, cols) = (15, 10)
    cellwh = 19
    margin = 25
    run(rows, cols)

def make2dlist(rows, cols, emptyColor):
    a = []
    for row in range(rows): a += [[emptyColor]*cols]
    return a

def tetrisPieces():
    iPiece = [
        [ True, True, True, True]
             ]
    jPiece = [
        [ True, False, False ],
        [ True, True,  True  ]
             ]
    lPiece = [
        [ False, False, True ],
        [ True,  True,  True ]
             ]
    oPiece = [
        [ True, True ],
        [ True, True ]
             ]
    sPiece = [
        [ False, True, True ],
        [ True,  True, False ]
             ]
    tPiece = [
        [ False, True, False ],
        [ True,  True, True  ]
             ]
    zPiece = [
        [ True,  True, False ],
        [ False, True, True  ]
             ]
    return [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    
def tetrisPieceColors():
    return [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]

def init(data): #initialize
    data.margin = 25
    (data.rows, data.cols) = (15, 10)
    data.cellwh = 18 #cell's width/height
    data.cellmargin = 1
    data.cell = data.cellwh+(2*data.cellmargin)
    data.boardwidth = data.cols*data.cell
    data.boardheight = data.rows*data.cell
    data.width = (data.boardwidth) + (2 * data.margin)
    data.height = (data.boardheight) + (2 * data.margin)
    data.emptyColor = "blue"
    data.board = make2dlist(data.rows, data.cols, data.emptyColor)
    data.tetrisPieces = tetrisPieces()
    data.tetrisPieceColors = tetrisPieceColors()
    data.score=0
    data.isGameOver=False
    newFallingPiece(data)

def newFallingPiece(data):
    length = len(data.tetrisPieces)
    num = random.randint(0,length-1) #random index
    data.fallingPiece = data.tetrisPieces[num]
    lens = len(data.tetrisPieceColors)
    nums = random.randint(0,lens-1) #random index
    data.fallingPieceColor=data.tetrisPieceColors[nums]
    (data.fallingPieceRows,data.fallingPieceCols) = (
                            len(data.fallingPiece),len(data.fallingPiece[0]))
    data.fallingPieceRow = 0
    data.fallingPieceCol = (data.cols//2) - (data.fallingPieceCols//2)

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym=="Down": moveFallingPiece(data, 1, 0) 
    elif event.keysym=="Right": moveFallingPiece(data, 0, 1) 
    elif event.keysym=="Left": moveFallingPiece(data, 0, -1) 
    elif event.keysym=="Up": rotateFallingPiece(data) 
    elif event.keysym=="r": init(data) #reset 
    
def timerFired(data):
    if data.isGameOver==True: return 
    if moveFallingPiece(data,1,0)==False:
        placeFallingPiece(data)
        newFallingPiece(data)
        if fallingPieceIsLegal(data)==False:
            data.isGameOver=True

def placeFallingPiece(data):
    for row in range(data.fallingPieceRows):
        for col in range(data.fallingPieceCols):
            if data.fallingPiece[row][col]==True:
                currentrow=data.fallingPieceRow+row
                currentcol=data.fallingPieceCol+col
                data.board[currentrow][currentcol]=data.fallingPieceColor
    removeFullRows(data)

def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow+=drow
    data.fallingPieceCol+=dcol
    if fallingPieceIsLegal(data)==False:
        data.fallingPieceRow-=drow
        data.fallingPieceCol-=dcol
        return False
    return True

def fallingPieceIsLegal(data):
    for row in range(data.fallingPieceRows):
        for col in range(data.fallingPieceCols):
            if (row+data.fallingPieceRow>=data.rows
                or row+data.fallingPieceRow<0
                or col+data.fallingPieceCol>=data.cols
                or col+data.fallingPieceCol<0
                or (data.fallingPiece[row][col]==True and 
                    (data.board[row+data.fallingPieceRow]
                    [col+data.fallingPieceCol]!=data.emptyColor))):
                        return False
    return True

def rotateFallingPiece(data):
    oldPiece = copy.copy(data.fallingPiece)
    (oldRow, oldRows) = (data.fallingPieceRow, data.fallingPieceRows)
    (oldCol, oldCols) = (data.fallingPieceCol, data.fallingPieceCols)
    (newRows, newCols) = (oldCols, oldRows)
    newPiece = []
    for row in range(newRows): newPiece += [[False]*newCols]
    for row in range(oldRows):
        for col in range(oldCols):
            if data.fallingPiece[row][col]==True:
                newPiece[newRows-col-1][row]=True
    oldCenterRow = oldRow + oldRows//2
    newCenterRow = oldCenterRow
    newRow = newCenterRow - newRows//2
    oldCenterCol = oldCol + oldCols//2
    newCenterCol = oldCenterCol
    newCol = newCenterCol - newCols//2
    data.fallingPiece = newPiece
    (data.fallingPieceRows, data.fallingPieceCols) = (newRows, newCols)
    (data.fallingPieceRow, data.fallingPieceCol) = (newRow, newCol)
    if fallingPieceIsLegal(data)!=True:
        data.fallingPiece = oldPiece
        (data.fallingPieceRows, data.fallingPieceCols) = (oldRows, oldCols)
        (data.fallingPieceRow, data.fallingPieceCol)= (oldRow, oldCol)
    
def removeFullRows(data):
    newBoard = []
    for row in range(data.rows): newBoard += [[data.emptyColor]*data.cols]
    newRow=data.rows-1
    counter=0
    for oldRow in range(data.rows-1, 0, -1):
        count=0
        for spot in data.board[oldRow]:
            if spot==data.emptyColor: 
                copyRow=copy.deepcopy(data.board[oldRow])
                newBoard[newRow]=copyRow
                newRow-=1
                break
            else: count+=1
        if count==data.cols: counter+=1
    data.score+=counter**2
    data.board=newBoard

def drawGame(canvas, data): #draw/view function
    canvas.create_rectangle(0,0,data.width,data.height,fill="orange",width=0)
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    
def drawBoard(canvas, data):    
    for row in range(data.rows):
        for col in range(data.cols): 
            color = data.board[row][col]
            drawCell(canvas, data, row, col, color)

def drawCell(canvas, data, row, col, color):    
    x0 = data.margin + (data.cell*col)
    y0 = data.margin + (data.cell*row)
    x1 = x0 + data.cell
    y1 = y0 + data.cell 
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+data.cellmargin, y0+data.cellmargin,
                        x1-data.cellmargin, y1-data.cellmargin, fill=color)

def drawFallingPiece(canvas, data):
    if data.isGameOver==True: 
        canvas.create_text(data.width/2, data.height/2, text="Game Over")
    for row in range(data.fallingPieceRows):
        for col in range(data.fallingPieceCols):
            if data.fallingPiece[row][col]==True:
                color = data.fallingPieceColor
                (r,c)=(row + data.fallingPieceRow, col + data.fallingPieceCol)
                drawCell(canvas, data, r, c, color)

def drawScore(canvas, data):
    marginScore = 4
    canvas.create_text(data.margin, data.margin/marginScore, 
                                    anchor=NW, text="Score="+str(data.score))

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def drawGameWrapper(canvas, data):
        canvas.delete(ALL)
        drawGame(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        drawGameWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        drawGameWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        drawGameWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)

