from graphics import *
import random
import time

###########################################################################
############# Section 1 --- User interface and Graphics
###########################################################################
def createWindow():
    """
    Creates and returns the game window as win.
    """
    win = GraphWin("Tic Tac Toe", 600, 600)
    win.setCoords(-0.25, 3.75, 3.25, -0.25) # give a little buffer
    win.setBackground("lightblue")
    return win

def setPlayerText(label, player):
    """
    Updates the label to show whose turn it is.
    """
    if player == 1:
        label.setText("Player 1's turn (X)")
    else:
        label.setText("Player 2's turn (O)")

class Button:
     """
    A class to represent a clickable button.
    """ 
     def __init__(self, win, center, width, height, label, color):
        """
        Initializes the button with its properties and draws it on the window.
        """
        self.win = win
        self.center = center
        self.width = width
        self.height = height
        self.label = label
       
        #create the button as a rectangle, Points calculate the top left and the bottom right corners 
        self.rect = Rectangle(Point(center.getX() - width/2, center.getY() - height/2), Point(center.getX() + width/2, center.getY() + height/2))
        self.rect.setFill(color)
        self.rect.draw(win)
        
        #set the label of the button at the center of the rectangle
        self.text = Text(center, label)
        self.text.draw(win)
        
     def was_clicked(self, pt):
        """
        Returns True if the button was clicked, based on the provided point.
        """
        pt1 = self.rect.getP1() #top left  (line 591 graphics)
        pt2 = self.rect.getP2() #bottom right

        #check if the point clicked is INSIDE the rectangle 
        horizontally_inside= pt1.getX() < pt.getX() < pt2.getX()
        vertically_inside= pt1.getY() < pt.getY() < pt2.getY()

        return  self.activate and horizontally_inside and vertically_inside
     
     def activate(self):
         """
        Activates the button, allowing it to be clicked.
        """
         self.activate=True

     def deactivate(self):
        """
        Deactivates the button, preventing it from being clicked.
        """
        self.activate=False
    
     def getLabel(self):
        """
        Returns the label of the button.
        """
        return self.label
    
def createMode_Buttons(win, WelcomeLabel, boardState):
    """
    Creates the mode selection buttons and handles their click events.
    """
    buttonMulti = Button(win, Point(0.75, 2.5), 0.75, 0.5, "Multiplayer", "lightpink")
    buttonSolo = Button(win, Point(2.25, 2.5), 0.75, 0.5, "Solo", "lightgreen")
    
    clicked_point = win.getMouse()

        #once a button is clicked bring up the board and run specific code
    if buttonMulti.was_clicked(clicked_point):
        drawBoard(win, buttonMulti, buttonSolo, WelcomeLabel)
        gameCode(win, boardState, "lightpink", "multiplayer")

    elif buttonSolo.was_clicked(clicked_point):
        drawBoard(win, buttonMulti, buttonSolo, WelcomeLabel,)
        gameCode(win, boardState, "lightgreen", "solo")

def drawBoard(win, buttonMulti, buttonSolo, WelcomeLabel):
    """
    Draws the game board after selection between multiplayer and solo modes;
    returns window, win
    """
    #undraw the welcome message and the buttons  
    WelcomeLabel.undraw()
    buttonMulti.rect.undraw()
    buttonMulti.text.undraw()
    buttonSolo.rect.undraw()
    buttonSolo.text.undraw()
    buttonMulti.deactivate()
    buttonSolo.deactivate()

    # Draw the lines
    for i in range(1, 3):
        horizontalLine = Line(Point(0, i), Point(3, i))
        horizontalLine.draw(win)
        
        verticalLine = Line(Point(i, 0), Point(i, 3))
        verticalLine.draw(win)

    return win
###########################################################################
############# Section 2 --- Making and Placing Pieces
###########################################################################
class Pieces:
    """
    Abstract class for pieces
    """
    def __init__(self, win, gridX, gridY):
        self.win = win
        self.gridX = gridX
        self.gridY = gridY

    def draw():
        raise NotImplementedError
    
    def get_pieceLabel():
        raise NotImplementedError

class XPiece(Pieces):
    """
    Actual class for player 1's pieces, "X"s
    """
    def __init__(self, win, gridX, gridY):
        Pieces.__init__(self,win, gridX, gridY)

    def draw(self):
        x_line1 = Line(Point(self.gridX+0.25, self.gridY+0.25), Point(self.gridX+0.75, self.gridY+0.75))
        x_line2 = Line(Point(self.gridX+0.25,self.gridY+0.75), Point(self.gridX+0.75,self.gridY+0.25))
        x_line1.draw(self.win)
        x_line1.setWidth(5)
        x_line2.draw(self.win)
        x_line2.setWidth(5)

    def get_pieceLabel(self):
        return "X Piece"

class OPiece(Pieces):
    """
    Actual class of Player 2's pieces, "O"s
    """
    def __init__(self, win, gridX, gridY):
        Pieces.__init__(self, win, gridX, gridY)

    def draw(self, background_color): 
        o = Circle(Point(self.gridX+0.5, self.gridY+0.5), 0.25)
        o.setFill(background_color)
        o.setWidth(5)
        o.draw(self.win)
    
    def get_pieceLabel(self):
        return "O piece"

def getGridLocation(point):
    gridX = int(point.getX())
    gridY = int(point.getY())
    return gridX, gridY

def drawPlayerMarker(win, boardState, gridX, gridY, player, background_color):
    if player == 1:
        piece = XPiece(win, gridX, gridY)
        piece.draw()
        boardState[gridY][gridX] = 1
    else: 
        piece = OPiece(win, gridX, gridY,)
        piece.draw(background_color)
        boardState[gridY][gridX] = 2

    return boardState[gridY][gridX]

###########################################################################
############# Section 4 --- Ending The Game
###########################################################################
def isValidGridCell(boardState, gridX, gridY):
    """
   Checks if parameters gridX and gridY point to an empty grid cell and within the grid range.
   Returns True if the grid cell is empty and within the grid range (contains None) and False otherwise
    """
    # Locate/pinpoint gridcell
    row = boardState[gridY]
    exactLocation = row[gridX] 
    
    # check if cell is empty and in bounds 
    if exactLocation == None and (0 <= gridX <= 3) and (0 <= gridY <= 3):
        return True
    else:
        return False   
    
def isDraw(boardState):
    """
    Checks if the game board is full (There is no grid cell that contains None).
    Returns True if all gridcells contain any value other than None.
    Returns False otherwise
    """
    for row in boardState:
        for col in row:
            if col == None:
                return False   
    return True

def didPlayerWinWithRow(boardState, player, gridY):
    """
    Checks if any player won with row (There are only 1s or 2s in a row)
    Returns true if any row wins
    Otherwise, returns False 
    """
    row = boardState[gridY]

    for i in row:
        if i != player:
            return False
    
    return True 

def didPlayerWinWithColumn(boardState, player, gridX):
    """
    Checks if any player won with column (There are only 1s or 2s in a row)
    Returns true if any column wins
    Otherwise, returns False 
    """
    for i in range(3):
        row = boardState[i]
        column = row[gridX]

        if column != player:
            return False
    
    return True

def didPlayerWinWithDiagonal(boardState, player):
    """
    Checks if any player won with diagonal (There are only 1s or 2s in a row)
    Returns true if any diagonal wins
    Otherwise, returns False 
    """

    leftDiag = []
    rightDiag = []

    # Right Diagonal
    for i in range(3):
        row = boardState[i]
        piece = row[i]
        rightDiag.append(piece)

    if rightDiag.count(player) == 3:
        return True
    
    # Left Diagonal
    for i in range(3):
        row = boardState[i]
        piece = row[2-i]
        leftDiag.append(piece)

    if leftDiag.count(player) == 3:
        return True
    
def didPlayerWin(boardState, player):
    """
    Runs all win-check functions defined above
    """
    # check the rows
    for row in range(3):
        if didPlayerWinWithRow(boardState, player, row):
            return True
    # check the columns
    for col in range(3):
        if didPlayerWinWithColumn(boardState, player, col):
            return True
        
    # check the diagonals
    if didPlayerWinWithDiagonal(boardState, player):
        return True
    
    # No win condition was met
    return False

###########################################################################
############# Section 5 --- Solo/Computer player Algorithm
###########################################################################    
def moves(boardState, number):
    """
    
    """
    l_diagonal = []
    r_diagonal = []
    for i in range (3): 
            row = boardState[i]
            column = [] 
            if (row.count(number) == 2 and row.count(None) == 1):
                chosen_cell = row.index(None)
                gridX, gridY = chosen_cell, i
                return gridX, gridY
            
            #top left to bottom right --- left diagonal
            l_diagonal.append(boardState[i][i])
            #top right to bottom left --- right diagonal
            r_diagonal.append(boardState[i][2-i])

            for row in boardState:
                column.append(row[i])
            if (column.count(number) == 2 and column.count(None) == 1):
                chosen_cell = column.index(None)
                gridX, gridY = i, chosen_cell
                return gridX, gridY
    
    if l_diagonal.count(number) == 2 and l_diagonal.count(None) == 1:
        chosen_cell = l_diagonal.index(None)
        return chosen_cell,chosen_cell #cells share row and column index's so return same thing
    
    if r_diagonal.count(number) == 2 and r_diagonal.count(None) == 1:
        chosen_cell = r_diagonal.index(None)
        return 2-chosen_cell, chosen_cell 
    
    return None
            
def compAlgorithms(boardState):
    """
    Use moves function to determine Player 2 in solo mode (the computer) should place a piece
    """
    # if player 1 hasn't placed an X at the center grid cell, place O at center
    if boardState[1][1] is None:
        return 1,1
    
    winning_move = moves(boardState,2)
    blocking_move = moves(boardState,1)

    if winning_move is not None:
        return winning_move
    
    if blocking_move is not None:
        return blocking_move
    
    # If no empty cell is found (board full), return None
    if isDraw(boardState):
        return None
    
    while True:
        gridX = random.randint(0,2)
        gridY = random.randint(0,2)
        if boardState[gridX][gridY] is None: 
            return gridX, gridY

###########################################################################
############# Section 6 --- play a game; multiplayer & solo code
###########################################################################

def gameCode(win, boardState, backgroundColor, mode):
    """
    Game's logic main code
    """
    win.setBackground(backgroundColor)

    textLabel = Text(Point(1.5, 3.5), "")
    textLabel.draw(win)

    win.getMouse()

    player = 1

    GameOver = False
    while not GameOver:
        # Update the player text
        setPlayerText(textLabel, player)

        # To place pieces, get clicks from player if in multiplayer mode
        if mode == "multiplayer":
            isValidCell = False
            while not isValidCell:
                gridX, gridY = getGridLocation(win.getMouse())
                isValidCell = isValidGridCell(boardState, gridX, gridY)   

        # To place peices, get clicks from player 1 and use compAlgorithm for player 2
        elif mode == "solo":
            isValidCell = False
            while not isValidCell:
                if player == 1:
                    gridX, gridY = getGridLocation(win.getMouse())
                    isValidCell = isValidGridCell(boardState, gridX, gridY)
                elif player == 2:
                    gridX, gridY = compAlgorithms(boardState)
                    isValidCell = isValidGridCell(boardState, gridX, gridY)
                    time.sleep(0.6)

        # Draw a marker for the current player
        drawPlayerMarker(win, boardState, gridX, gridY, player, backgroundColor)
        
        # Check if anyone won
        if didPlayerWin(boardState, player):
            textLabel.setText("Player {0} wins! --- click again to quit".format(player))
            GameOver = True
        elif isDraw(boardState):
            textLabel.setText("The game is a draw --- click again to quit")
            GameOver = True
        else:
            player = 3 - player # switches between 1 and 2

def main():
    """
    Creates a graphical window, initiates the board, and displays the welcome screen page
    """
    # Create and set up the board
    win = createWindow()
    
    # screen 1 welcome message 
    WelcomeLabel = Text(Point(1.5,1), "Welcome to TicTacToe!\n \n What mode do you want to play?")
    WelcomeLabel.setSize(20)
    WelcomeLabel.draw(win)

    boardState = [[None, None, None], # top row
                  [None, None, None], # middle row
                  [None, None, None]] # bottom row
    
    # Creates "Choose multiplayer or solo mode" button
    createMode_Buttons(win, WelcomeLabel, boardState)

    win.getMouse()
    win.close()

    return boardState

if __name__ == "__main__":
    main()