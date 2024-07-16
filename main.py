import pyautogui as ap
import sys
import time

#Global constants
SLEEP_TIME = 0.02
BOARD = [[0 for col in range (0,8)]for row in range(0,8)]

#Max moves to be qued, changing this effects performance,
#lower -> higher chance of geting stuck, higher -> slower
#as more redundant moves are made, you can change this.
#I reccomend 5-10 as the max in most cases
MAX = 2
moves = 0

#COLOR RECOGNITION FUNCTIONS

def getAvg(x,y,im):
    avgR = 0
    avgG = 0
    avgB = 0
    for i in range (-2, 3):
        for j in range(-2, 3):
            r,g,b = im.load()[x+i, y+j]
            avgR += r
            avgG += g
            avgB += b
    avgR = int(avgR/25)
    avgG = int(avgG / 25)
    avgB = int(avgB / 25)
    return avgR, avgG, avgB

def getDistance(r1, g1, b1, r2, g2, b2):
    return abs(r2-r1)**2 + abs(g2-g1)**2 + abs(b2-b1)**2


#"BLANK" means that the gem is not recognised as any of the
# defined gem colors Red,Blue,White,Yellow,Orange,Green,Purple
def getCol(r1,g1,b1):
    colName = ["R", "Y", "P", "T", "B", "S"]
    colValues = [(154, 9, 1), (221, 131, 15), (161, 2, 142), (7, 70, 71), (19, 31, 154), (36, 1, 1)]
    distance = []
    for i in range(0,6):
        r2, g2, b2 = colValues[i]
        distance.append(getDistance(r1, g1, b1, r2, g2, b2))
    return colName[min(range(len(distance)), key=distance.__getitem__)]

#MOUSE FUNCTIONS
def leftClick():
    ap.mouseDown(button='left')
    time.sleep(SLEEP_TIME)

def releaseLeft():
    ap.mouseUp(button='left')
    time.sleep(SLEEP_TIME)

def moveMouse(x,y):
    ap.moveTo(x,y)
    time.sleep(SLEEP_TIME)

def click(x,y):
    moveMouse(x,y)
    leftClick()
    releaseLeft()

#Maps 0..7 in 8x8 grid co-ordinates to return the real
#screen co-ordinates for use with mouse functions.
def mapMove(x,y):
    xOff = 90
    yOff = 60
    realX = xOff + (x*90)
    realY = yOff + (y*90)
    return (int(realX),int(realY))

#Takes a screenshot of the board and grabs the RGB values
#of each gem, feeds them to color recognition function getCol
#then puts
def getBoard():
    import PIL.ImageGrab
    im = PIL.ImageGrab.grab(bbox=(208,117,960,883))
    #im.save("testpic.jpg")
    for i in range (0,8):
        for j in range (0,8):
            x,y = mapMove(j,i)
            #print(str(x) + " " + str(y))
            r,g,b = getAvg(x,y,im)
            BOARD[i][j] = getCol(r,g,b)
    print(BOARD)

#Checks wether the gems at 2 positions are the same color
def same(x1,y1,x2,y2):
    #check positions passed are in the 8x8 grid
    if (x1<0 or x1>7 or y1<0 or y1>7 or x2<0 or x2>7 or y2<0 or y2>7):
        return False
    if (BOARD[y1][x1] == BOARD[y2][x2]):
        return True

#moves a gem from (x1,y1) to (x2,y2)
def move(x1,y1,x2,y2):
    print("swapping "+str(x1)+","+str(y1)+" with "+str(x2)+","+str(y2))
    global moves
    startX,startY = mapMove(x1,y1)
    startX+=178
    startY+=117
    ap.moveTo(startX, startY)
    time.sleep(0.05)
    endX,endY = mapMove(x2,y2)
    endX += 178
    endY += 117
    ap.dragTo(endX, endY, duration = 0.25)
    moves = moves + 1

#MAIN
def main():
    #initialisation/setup
    global MAX
    global moves
    time.sleep(1)

    while True:

        #get the board info
        moves = 0
        getBoard()
        #for every tile in the board
        for y in range (0,8):
            #if we have tried more moves than allowed in the que
            #break and get the board info again
            if (moves > MAX):
                break
            for x in range (0,8):
                #Algorithm to find matches 5 big cases (UGLY)
                #Looks at where matches could be given 2 gems of the same color next to each other
                #for the majority of cases.

                #gem above current is same color
                if same(x,y,x,y-1):
                    if same(x,y,x-1,y-2): move(x-1,y-2,x,y-2)
                    if same(x,y,x+1,y-2): move(x+1,y-2,x,y-2)
                    if same(x,y,x,y-3): move (x,y-3,x,y-2)
                #gem below current is same color
                if same(x,y,x,y+1):
                    if same(x,y,x-1,y+2): move(x-1,y+2,x,y+2)
                    if same(x,y,x+1,y+2): move(x+1,y+2,x,y+2)
                    if same(x,y,x,y+3): move(x,y+3,x,y+2)
                #gem left of current is same color
                if same(x,y,x-1,y):
                    if same(x,y,x-3,y): move(x-3,y,x-2,y)
                    if same(x,y,x-2,y-1): move(x-2,y-1,x-2,y)
                    if same(x,y,x-2,y+1): move(x-2,y+1,x-2,y)
                #gem right of current is same color
                if same(x,y,x+1,y):
                    if same(x,y,x+3,y): move(x+3,y,x+2,y)
                    if same(x,y,x+2,y-1): move(x+2,y-1,x+2,y)
                    if same(x,y,x+2,y+1): move(x+2,y+1,x+2,y)
                #holes vertical
                if same(x,y,x,y+2):
                    if same(x,y,x-1,y+1): move(x-1,y+1,x,y+1)
                    if same(x,y,x+1,y+1): move(x+1,y+1,x,y+1)
                #holes horizontal
                if same(x,y,x+2,y):
                    if same(x,y,x+1,y-1): move(x+1,y-1,x+1,y)
                    if same(x,y,x+1,y+1): move(x+1,y+1,x+1,y)
#call main
main()