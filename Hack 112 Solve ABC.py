from tkinter import *
import copy
    
def init(data):
    data.index = 0
    (data.margin, data.step) = (100, 0)
    (data.rows, data.cols, data.blackBoard) = (5, 5, 700)
    data.blockX = (data.blackBoard - 2 * data.margin) / data.rows
    data.blockY = (data.blackBoard - 50 - 2 * data.margin) / data.cols
    data.A = [(0,4),(0,0),(1,2)]
    data.board = make2dListB(data)
    data.constraints = ["CHJXBOVLFNURGPEKWTSQDYMI","UHIPOYDMBKWGTNXSFCLEJVQR",
        "GKPSRYLOWTDEBFXHCMJIUVNQ"]
    data.play = False
    data.result = []
    data.result = solveABC(data)
    data.stepMax = len(data.result)
    data.result = []

def mousePressed(event, data):
    if 720 <= event.x <= 770 and 100 <= event.y <= 200 and data.index - 1 >= 0:
        index = data.index-1
        data.index = index
        data.board = make2dListB(data)
        data.step = 0
        data.result = []
        data.result = solveABC(data)
        data.stepMax = len(data.result)
        data.result = []
    elif 930 <= event.x <= 980 and 100 <= event.y <= 200 and data.index + 1 <= 2:
        index = data.index+1
        data.index = index
        data.board = make2dListB(data)
        data.step = 0
        data.result = []
        data.result = solveABC(data)
        data.stepMax = len(data.result)
        data.result = []
    elif 720 <= event.x <= 980 and 210 <= event.y <= 260:
        temp = data.index
        init(data)
        data.index = temp
        data.board = make2dListB(data)
    elif 720 <= event.x <= 980 and 270 <= event.y <= 320:
        data.board = showSolution(data)
        solveABC(data)
        data.step = data.stepMax-1
        data.board = list(data.result[data.step])
    elif 720 <= event.x <= 770 and 390 <= event.y <= 440 and data.step - 1 >= 0:
        data.step -= 1
        solveABC(data)
        data.board = list(data.result[data.step])
    elif 930 <= event.x <= 980 and 390 <= event.y <= 440: 
        data.step += 1
        if(data.step >= data.stepMax):
            data.step = 0
        solveABC(data)
        data.board = list(data.result[data.step])

def keyPressed(event, data):
    pass

def timerFired(data):
    pass    

def drawCell(canvas,data,row,col):
    constraintsR = makeDictPrep(data.constraints[data.index])[2] 
    constraintsC = makeDictPrep(data.constraints[data.index])[1]
    constraintsD = makeDictPrep(data.constraints[data.index])[0]
    cx = data.margin + data.blockX * col
    cy = data.margin + 50 + data.blockY * row
    cxBottom = cx + data.blockX
    cyBottom = cy + data.blockY
    canvas.create_rectangle(cx, cy, cxBottom, cyBottom, 
                            fill = "grey", width = 1)
    canvas.create_text((cx + cxBottom)/2, (cy + cyBottom)/2, 
            text = data.board[row][col], fill = "black" , font = "Times 35")
    canvas.create_text((cx + cxBottom)/2, 100, 
            text = constraintsC[col], fill = "white" , font = "Times 35")
    canvas.create_text((cx + cxBottom)/2, data.blackBoard - 50, 
            text = constraintsC[10-col-1], fill = "white" , font = "Times 35")
    canvas.create_text(data.margin/2, (cy + cyBottom)/2 , 
            text = constraintsR[10-row-1], fill = "white" , font = "Times 35")
    canvas.create_text(data.blackBoard - data.margin/2, (cy + cyBottom)/2, 
            text = constraintsR[row], fill = "white" , font = "Times 35")
    if(row == col):
        canvas.create_text(50, 100, text = constraintsD[0],
                fill = "white", font = "Times 35")
        canvas.create_text(650, 650, text = constraintsD[2], 
                fill = "white", font = "Times 35")
    elif((row + col) == data.rows - 1):
        canvas.create_text(50, 650, text = constraintsD[1],
                 fill = "white", font = "Times 35")
        canvas.create_text(650, 100, text = constraintsD[3], 
                fill = "white", font = "Times 35")

def make2dListB(data): 
    board = []
    boardPerRow = []
    for row in range(data.rows):
        for col in range(data.cols):
            if(row == data.A[data.index][0] and col == data.A[data.index][1]):
                boardPerRow.append("A")
            else:
                boardPerRow.append("")
        board.append(boardPerRow)
        boardPerRow = [] 
    return board 

def drawBoard(canvas, data): 
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col)

def make2dList(rows, cols):
    # to create a 2d list 
    a=[]
    perRow = []
    for row in range(rows): 
        for col in range(cols):
            perRow.append("")
        a.append(perRow)
        perRow = []
    return a

def makeDictPrep(constraints):
    # tr to put right alphabet in to right place
    (diaganol, row, col, diaganolflag) = ([], [], [], 6)
    # where to split the stirng to put in row
    (indexForRight, indexForAnotheRight) = (7,11)
    (indexForLeft, indexForAnotheLeft) = (19,24)
    test = list(constraints)
    for index in range(len(test)):
        if((index % diaganolflag) == 0):
            diaganol.append(test[index])
        elif((index <= indexForAnotheRight and index >= indexForRight) or
                (index <= indexForAnotheLeft and index >= indexForLeft)):
                 row.append(test[index])
        else:
            col.append(test[index])
    return (diaganol,col,row)

def makeDictDiaganol(constraints):
    # put diagnal in a dict with key of the location on board in tuple
    result = dict()
    (diaganol, size) = (makeDictPrep(constraints)[0], 5)
    (indexForRight, indexForAnotheRight) = (0,2)
    (indexForLeft, indexForAnotheLeft) = (1,3)
    for row in range(size):
        for col in range(size):
            if(row == col):
                # if there is not a key, create one
                if((row, col) not in result):
                    result[(row,col)] = ""
                result[(row,col)] += diaganol[indexForRight]                    
                result[(row,col)] += diaganol[indexForAnotheRight]
            elif(row + col == size -1):
                if((row, col) not in result):
                    result[(row,col)] = ""
                result[(row,col)] += diaganol[indexForLeft]
                result[(row,col)] += diaganol[indexForAnotheLeft]
    return result  

def makeDictRow(constraints):
    # put row in a dict with key of the location on board in tuple
    result = dict()
    (rows, size) = (makeDictPrep(constraints)[2], 5)
    for row in range(size):
        for col in range(size):
            # if there is not a key, create one 
            if((row, col) not in result):
                result[(row,col)] = ""
            result[(row,col)] += rows[row]
            result[(row,col)] += rows[-(row + 1)]
    return result

def makeDictCol(constraints):
    # put col in a dict with key of the location on board in tuple 
    result = dict()
    (cols, size) = (makeDictPrep(constraints)[1], 5)
    for col in range(size):
        for row in range(size):
            # if there is not a key, create one
            if((row, col) not in result):
                result[(row,col)] = ""
            result[(row,col)] += cols[col]
            result[(row,col)] += cols[-(col +1)]
    return result

def makeDict(constraints):
    # to put all three together making a whol dict in other to facilitate
    # is legal in the main function
    parts= [makeDictDiaganol(constraints), makeDictCol(constraints),
                        makeDictRow(constraints)]
    result = dict()
    (diaganol,row,col) = (0,1,2)
    # put diaganol
    for key in parts[diaganol]:
        if(key not in result):
            result[key] = parts[diaganol][key]
    # put row
    for key in parts[1]:
        if(key not in result):
            result[key] = parts[row][key]
        else:
            result[key] += parts[row][key]
    # put col
    for key in parts[col]:
        result[key] += parts[col][key]
    return result

def solve(data, cons, dirs, row, col, answer, letter):
    # Base case is when it reach Z then it should be end
    temp = tuple(copy.deepcopy(answer))
    data.result.append(temp)
    if(letter == ord("Z")):
        return answer
    else:
        # test for all direcitons for each letter
        for dir in range(len(dirs)):
            (drow, dcol) = (dirs[dir])
            # try every directions
            (startRow, startCol, size) = (drow + row, dcol + col, 5)
            # avoid off the board or in place where there is an number
            if(startCol < size and startRow < size and 
                startCol >= 0 and startRow >= 0 and 
                answer[startRow][startCol] == ""):
                # first put the letter on the board
                answer[startRow][startCol] = chr(letter)
                # test if it follows the rule
                if(answer[startRow][startCol] in cons[(startRow,startCol)]):
                    solve(data, cons, dirs, startRow, startCol, 
                            answer, letter+1)
                    # if there is Y on the board, then the whole program should
                    # end right now
                    for testEndRow in range(len(answer)):
                        if("Y" in answer[testEndRow]):
                            return answer
                # it is wrong, pick it up, then try another direction
                answer[startRow][startCol] = ""
            # when it is offboard, just ignore
            else:continue
    # there is a problem, go back to the previous letter
    return answer

def solveABC(data):
    # set up initial parametert
    (cons, size) = (makeDict(data.constraints[data.index]), 5)
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    answer = [[""] * size for row in range(size)]
    (row, col) = data.A[data.index]
    # start with B and put A in the right position
    letter = ord("B")
    answer[row][col] = "A"
    solve(data, cons, dirs, row, col, answer, letter)
    return data.result

def showSolution(data):
    # set up initial parametert
    (cons, size) = (makeDict(data.constraints[data.index]), 5)
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    answer = [[""] * size for row in range(size)]
    (row, col) = data.A[data.index]
    # start with B and put A in the right position
    letter = ord("B")
    answer[row][col] = "A"
    answer = solve(data, cons, dirs, row, col, answer, letter)
    return answer

def drawBackground(canvas,data):
    canvas.create_rectangle(0, 10, 1000, 790,  fill="grey")
    canvas.create_rectangle(0, 50, data.blackBoard, data.blackBoard
            , fill="black")

    canvas.create_rectangle(0,10,1000,790,fill="grey")
    canvas.create_rectangle(0,50,700,690,fill="black")
    #title
    canvas.create_text(100,30,text="Solve ABC",font="Arial 24")
    canvas.create_text(850,80,text="Constraints and Alocation",font="Arial 24")
    #level choose
    # <<
    canvas.create_rectangle(720,100,770,200,fill="white",width=0)
    canvas.create_text(745,150,text="<<",font="Arial 24")
    # >>
    canvas.create_rectangle(930,100,980,200,fill="white",width=0)
    canvas.create_text(955,150,text=">>",font="Arial 24")
    #level
    canvas.create_rectangle(780,100,920,200,width=2,outline="white")
    canvas.create_text(850,125,text=data.constraints[data.index][:12],
        font="Arial 16")
    canvas.create_text(850,150,text=data.constraints[data.index][12:],
        font="Arial 16")
    canvas.create_text(850,175,text="(%d, %d)" % (data.A[data.index][0], 
        data.A[data.index][1]),
        font="Arial 20")
    #restart
    canvas.create_rectangle(720,210,980,260,fill="white",width=0)
    canvas.create_text(850,235,text="RESTART",font="Arial 24")
    #automatic
    canvas.create_rectangle(720,270,980,320,fill="white",width=0)
    canvas.create_text(850,295,text="SOLUTION",font="Arial 24")
    # last
    canvas.create_rectangle(720,390,770,440,fill="white",width=0)
    canvas.create_text(745,415,text="-",font="Arial 24")
    # next
    canvas.create_rectangle(930,390,980,440,fill="white",width=0)
    canvas.create_text(955,415,text="+",font="Arial 24")
    # step choose
    canvas.create_text(850,355,text="STEPS",font="Arial 24")
    # step
    canvas.create_rectangle(780,390,920,440,width=2,outline="white")
    canvas.create_text(850,415,text=data.step,font="Arial 24")

def redrawAll(canvas, data):
    drawBackground(canvas,data)
    drawBoard(canvas, data)
 
def run(width=1000, height=800):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
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

run()