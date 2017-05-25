import tkinter as tk
from tkinter import *
from tkinter.simpledialog import askstring

def evalPrefixNotation1(L):
    # we want to store operators and values in different lists 
    operatorList=[]
    resultList=[]
    # if we only have one value in the list, return directly 
    if (len(L)==1):
        return L[0]
    else:
        
        return evalPrefixNotationWrap1(L,operatorList,resultList)
        
def evalPrefixNotationWrap1(L,operatorList,resultL):
    calculateOperand=2 
    
    if (len(L) == 0): return resultL[0]
    currVal=L.pop()
    if (isinstance(currVal,str) and currVal not in "*-+"):
        raise Exception('Unknown operator: ' + operator)
    else:
        if (currVal=="*" or currVal=="-" or currVal=="+"): 
            operatorList.append(currVal)
        else: resultL.insert(0,currVal)
        
        if (len(resultL)>=calculateOperand and operatorList!=[]):
            lastOperator=operatorList.pop()
            firstOperand=resultL.pop(0)
            secondOperand=resultL.pop(0)
            if (lastOperator=="*"): resultL.insert(0,firstOperand*secondOperand)
            elif (lastOperator=="+"):
                resultL.insert(0,firstOperand+secondOperand)
                
            elif (lastOperator=="-"):
                resultL.insert(0,firstOperand-secondOperand)
        
        return evalPrefixNotationWrap1(L,operatorList,resultL)
 
 


####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
   
    data.result=None 
    data.operatorList1=[]
    data.resultL=[]
    data.operations=[]
def mousePressed(event, data):
    if (event.x>=720 and event.x<=980 and event.y>=600 and event.y<=650):
        data.result=evalPrefixNotation1(data.List2)
    
    if (event.x>=720 and event.x<=980  and event.y>=510 and event.y<=560):
        evalPrefixNotation(data)
    

def evalPrefixNotation(data):
    # we want to store operators and values in different lists 
   
    # if we only have one value in the list, return directly 
    if (len(data.List)==1):
        return data.List[0]
    else:
        return evalPrefixNotationWrap(data)
        
def evalPrefixNotationWrap(data):
    calculateOperand=2 
    if (len(data.List)== 0): 
        return data.result 
    currVal=data.List.pop()
    if (isinstance(currVal,str) and currVal not in "*-+"):
        raise Exception('Unknown operator: ' + operator)
    else:
        if (currVal=="*" or currVal=="-" or currVal=="+"): 
            data.operatorList1.append(currVal)
        else: data.resultL.insert(0,currVal)
        
        if (len(data.resultL)>=calculateOperand and data.operatorList1!=[]):
            lastOperator=data.operatorList1.pop()
            firstOperand=data.resultL.pop(0)
            secondOperand=data.resultL.pop(0)
            if (lastOperator=="*"): 
                data.resultL.insert(0,firstOperand*secondOperand)
                data.operations.append("%d*%d=%d"%(firstOperand,secondOperand,
                    firstOperand*secondOperand))
            elif (lastOperator=="+"):
                data.resultL.insert(0,firstOperand+secondOperand)
                data.operations.append("%d+%d=%d"%(firstOperand,secondOperand,
                    firstOperand+secondOperand))
            elif (lastOperator=="-"):
                data.resultL.insert(0,firstOperand-secondOperand)
                data.operations.append("%d-%d=%d"%(firstOperand,secondOperand,
                    firstOperand-secondOperand))
        return evalPrefixNotationWrap(data)


def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass
    
def drawBackground(canvas,data):
    
    textMsg="evalWithPrefix"
    canvas.create_rectangle(0,10,1000,790,fill="grey")
    canvas.create_rectangle(0,50,700,690,fill="black")
    #title
    canvas.create_text(100,30,text=textMsg,font="Arial 20")
   
    canvas.create_text(850,45,text="Operator List",font="Arial 24")
    canvas.create_rectangle(720,70,980,120,fill="white",width=0)

    canvas.create_text(850,180,text="Digit List",font="Arial 24")
   
    canvas.create_text(850,310,text="Result",font="Arial 24")
   
    canvas.create_rectangle(720,340,980,390,fill="white",width=0)
    #restart
    canvas.create_rectangle(720,210,980,260,fill="white",width=0)
    #step choose
    canvas.create_text(850,475,text="STEPS",font="Arial 24")
    # last
    canvas.create_rectangle(720,510,980,560,fill="white",width=0)
    canvas.create_text(855,535,text="showSteps",font="Arial 24")
        
    canvas.create_rectangle(720,600,980,650,fill="white",width=0)
    canvas.create_text(850,625,text="Calculate",font="Arial 24")
    canvas.create_text(850,90,text="%s"%(str(data.operatorList)),font="Arial 24")
    canvas.create_text(850,230,text="%s"%(str(data.digitList)),font="Arial 24")
    
    if (data.result!=None):
        canvas.create_text(850,365,text="%d"%data.result,fill="black",
            font="Arial 24")
    
def drawAnswer(canvas,data):
    xPos=50
    yPos=50
    for eachOperation in range(len(data.operations)):
        yPos+=40
        msg=data.operations[eachOperation]
        canvas.create_text(xPos,yPos,text=msg,fill="white",font="Arial 24")
            
def redrawAll(canvas, data):
    drawBackground(canvas,data)
    drawAnswer(canvas,data)

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
    data.List=[]
    data.digitList=[]
    data.operatorList=[]
    data.List2=[]
    name = askstring("EvalwithPrefixx", "Enter calculation")
    for eL in name.strip(","):
        if (eL.isdigit() or eL=="+" or eL=="-" or eL=="*"):
            if (eL.isdigit()):
                eL=int(eL)
                data.digitList.append(eL)
            else:
                data.operatorList.append(eL)
            data.List.append(eL)
            data.List2.append(eL)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000,800)