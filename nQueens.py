from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.queens=0
    data.cols=0
    data.rows=0
    data.row=0
    data.col=0
    data.step=0
    data.queenRow=[]
    data.gridW=20
    data.gridH=20
    data.stepWork=False 
   
    
    data.answer=[]
    data.play=False 
    data.ggwp=False 
    data.count=0
def mousePressed(event, data):
    if (data.ggwp==False):
        if (data.stepWork==False):
            if (event.x>=720 and event.x<=770  and event.y>=70 and event.y<=120 
                and data.queens>0):
                data.queens-=1
            if (event.x>=930 and event.x<=980  and event.y>=70 and event.y<=120):
                data.queens+=1
        
        if (event.x>=930 and event.x<=980  and event.y>=510 and event.y<=560
            and data.queens>3):
            data.stepWork=True 
            data.step+=1 
            data.queenRow=[-1]*data.queens
            solve(data,0)
        if (event.x>=720 and event.x<=980  and event.y>=270 and event.y<=320
            and data.queens>3):
            data.stepWork=True 
            data.play=True 
            data.queenRow=[-1]*data.queens
            solve(data,0)
    if (event.x>=720 and event.x<=770  and event.y>=510 and event.y<=560
            and data.step>1):
        data.step-=1 
        data.ggwp=False 
    if (event.x>=720 and event.x<=980  and event.y>=210 and event.y<=260
         and data.queens>0):
        data.stepWork=False 
        data.queenRow=[]
        data.answer=[]
        data.queens=0
        data.step=0
        data.play=False 
        data.ggwp=False 
        data.count=0

def keyPressed(event, data):
    if (data.ggwp==False):
        if (data.stepWork==False):
            if (event.keysym=="Right"):
                data.queens+=1
            if (event.keysym=="Left" and data.queens>0):
                data.queens-=1
                
        if (event.keysym=="Up" and data.queens>3):
            data.stepWork=True 
            data.step+=1 
            data.queenRow=[-1]*data.queens
            solve(data,0)
            
        if (event.keysym=="p" and data.queens>3):
            data.stepWork=True 
            data.play=True 
            data.queenRow=[-1]*data.queens
            solve(data,0)
            
    if (event.keysym=="Down" and data.step>1):
        data.step-=1 
        data.ggwp=False 
    if ((event.keysym=="r" or event.keysym=="R") and data.queens>0):
        data.stepWork=False 
        data.queenRow=[]
        data.answer=[]
        data.queens=0
        data.step=0
        data.play=False 
        data.ggwp=False 
        data.count=0
        
def timerFired(data):
    data.cols=data.queens
    data.rows=data.queens
    data.move=data.step
    if (data.rows>=1 and data.cols>=1):
        data.gridW=700/data.cols
        data.gridH=640/data.rows
    if (data.rows>=1 and data.cols>=1):
        data.col=data.step%data.cols
        data.row=data.step//data.rows
   
def isLegal(data,row, col):
    for qcol in range(col):
        qrow = data.queenRow[qcol]
        if ((qrow == row) or
                (qcol == col) or
                (qrow+qcol == row+col) or
                (qrow-qcol == row-col)):
            return False
    return True
        
def solve(data,col):
    if (col == data.cols):
        data.count+=1
        return data.queenRow
    else:
        for row in range(data.queens):                    
            if ((data.step>0 or data.play==True) and data.count==0):
                if isLegal(data,row,col):
                    data.queenRow[col] = row
                    egg=tuple(data.queenRow) 
                    data.answer.append(egg)
                    solution = solve(data,col+1)                  
                    if (solution!=None):
                        return solution 
                    data.queenRow[col]=-1            
        return None
    return solve(data,0)

def drawBackground(canvas,data):
    textMsg="nQueens(Up Down:Step. Left Right:Queen Num. R:Reset)"
    canvas.create_rectangle(0,10,1000,790,fill="grey")
    canvas.create_rectangle(0,50,700,690,fill="black")
    #title
    canvas.create_text(data.width/2,30,text=textMsg,font="Arial 20")
    #discs
   
    canvas.create_text(850,45,text="Queens",font="Arial 24")

    # -
    canvas.create_rectangle(720,70,770,120,fill="white",width=0)
    canvas.create_text(745,95,text="-",font="Arial 24")
    # +
    canvas.create_rectangle(930,70,980,120,fill="white",width=0)
    canvas.create_text(955,95,text="+",font="Arial 24")
    
    canvas.create_text(850,95,text="%d" %data.queens,font="Arial 24")
    
    #restart
    canvas.create_rectangle(720,210,980,260,fill="white",width=0)
    canvas.create_text(850,235,text="RESTART",font="Arial 24")
    #automatic
    canvas.create_rectangle(720,270,980,320,fill="white",width=0)
    canvas.create_text(850,295,text="PLAY",font="Arial 24")
    #step choose
    canvas.create_text(850,475,text="STEPS",font="Arial 24")
    # last
    canvas.create_rectangle(720,510,770,560,fill="white",width=0)
    canvas.create_text(745,535,text="-",font="Arial 24")
    # next
    canvas.create_text(850,535,text="%d"%data.step,font="Arial 24")
    canvas.create_rectangle(930,510,980,560,fill="white",width=0)
    canvas.create_text(955,535,text="+",font="Arial 24")

def drawBoard(canvas,data):
    for row in range (data.rows):
        for col in range(data.cols):
            canvas.create_rectangle(data.gridW*col,50+data.gridH*row,
                 data.gridW*(col+1), 50+data.gridH*(row+1),fill="white")


                    
def drawStepAnswer(canvas,data):
    if (data.step==len(data.answer)):
        data.ggwp=True 
    for eachNumber in range(len(data.answer[data.step-1])):
        if (eachNumber!=-1):
            row=eachNumber
            col=data.answer[data.step-1][eachNumber]
            canvas.create_text(data.gridW*(col+0.5),50+data.gridH*(row+0.5),
                    text="Q",font="Arial 24")

def redrawAll(canvas, data):
    drawBackground(canvas,data)
    drawBoard(canvas,data)
    if (data.play==True):
        data.play=False 
        data.step=len(data.answer)
    if (data.stepWork==True and data.queens>0):
        drawStepAnswer(canvas,data)
        
        
        
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
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
    data.timerDelay = 100 # milliseconds
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

run(1000, 1000)