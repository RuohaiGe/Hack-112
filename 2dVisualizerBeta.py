from tkinter import *
from tkinter import simpledialog

####################################
# customize these functions
####################################
class List(object):
    HGT=50
    def __init__(self,left,top,len):
        self.left=left
        self.top=top
        self.len=len
        self.blockHgt=self.HGT
        self.blockWid=50
        self.inPoint=(left,top)
        
class OnedList(List):
    def __init__(self,left,top,len):
        super().__init__(left,top,len)
        self.list=[0 for i in range(self.len)]
        self.startPoints=[(self.left+(i+1/2)*self.blockWid,(self.top+self.HGT)) 
                            for i in range(self.len)]
        self.endPoints=[(self.left+(i+1/2)*self.blockWid,self.top) 
                            for i in range(self.len)]
        self.textCenter=[(self.left+(i+1/2)*self.blockWid,(self.top+self.HGT/2)) 
                            for i in range(self.len)]

class TwodList(List):
    def __init__(self,left,top,len):
        super().__init__(left,top,len)
        self.startPoints=[(self.left+(i+1/2)*self.blockWid,(self.top+self.HGT/2)) 
                            for i in range(self.len)]
        self.endPoints=[(self.left+(i+1/2)*self.blockWid,self.top)
                        for i in range(self.len)]

class Pointer(object):
    def __init__(self,left,top,right,bot):
        self.left=left
        self.top=top
        self.right=right
        self.bot=bot

class Txt(object):
    def __init__(self,cenX,cenY,text,color):
        self.cenX=cenX
        self.cenY=cenY
        self.text=text
        self.color=color

def init(data):
    data.flag='starter'
    data.pause=True
    data.step=0
    data.strLen=0
    data.pointerList=[]
    data.listList=[]
    data.textList=[]
    data.width,data.height=1000,800
    data.animWid,data.animHgt=700,650
    data.but1L,data.but1R,data.but1T,data.but1B=100,400,500,600
    data.but2L,data.but2R,data.but2T,data.but2B=600,900,500,600
    data.but3L,data.but3R,data.but3T,data.but3B=350,650,650,750
    data.but4L,data.but4R,data.but4T,data.but4B=720,980,100,180

def mousePressed(event, data):
    if data.flag=='starter':
        if data.but1L<event.x<data.but1R and data.but1T<event.y<data.but1B:
            data.flag='1d'
        elif data.but2L<event.x<data.but2R and data.but2T<event.y<data.but2B:
            data.flag='2d'
    elif data.flag=='1d':
        if data.but1L<event.x<data.but1R and data.but1T<event.y<data.but1B:
            data.flag='1dAlias'
        elif data.but2L<event.x<data.but2R and data.but2T<event.y<data.but2B:
            data.flag='1dCopy'
    elif data.flag=='2d':
        if data.but1L<event.x<data.but1R and data.but1T<event.y<data.but1B:
            data.flag='2dFalse'
        elif data.but2L<event.x<data.but2R and data.but2T<event.y<data.but2B:
            data.flag='2dCopy'
        elif data.but3L<event.x<data.but3R and data.but3T<event.y<data.but3B:
            data.flag='2dDeep'
    elif data.flag=='1dAlias' or data.flag=='1dCopy':
        if data.pause==False:
            if data.but4L<event.x<data.but4R and data.but4T<event.y<data.but4B:
                nextStep1d(data)
    elif data.flag=='2dFalse':
        if data.pause==False:
            if data.but4L<event.x<data.but4R and data.but4T<event.y<data.but4B:
                nextStep2dFalse(data)
    elif data.flag=='2dCopy' or data.flag=='2dDeep':
        if data.pause==False:
            if data.but4L<event.x<data.but4R and data.but4T<event.y<data.but4B:
                nextStep2d(data)

def keyPressed(event, data):
    if data.flag=='end':
        if event.keysym=='Return':
            init(data)

def timerFired(data):
    x=None
    if ((data.flag=='1dAlias' or data.flag=='1dCopy' or data.flag=='2dFalse')
        and data.pause==True):
        while x==None:
            x=simpledialog.askstring('Window',
                                     'Please input a number (from 1 to 7):')
        data.strLen=int(x)
        data.pause=False
    elif (data.flag=='2dCopy' or data.flag=='2dDeep') and data.pause==True:
        while x==None:
            x=simpledialog.askstring('Window',
                                     'Please input a number (from 1 to 5):')
        data.strLen=int(x)
        data.pause=False

def nextStep2dFalse(data):
    if data.step==0:
        data.step+=1
        data.textList.append(Txt(50,200,'a','White'))
        list1=TwodList(200,200,data.strLen)
        list2=OnedList(200,500,data.strLen)
        data.listList.append(list1)
        data.listList.append(list2)
        data.textList.append(Txt(850,500,'a=[[0]*%d]*%d'%(data.strLen,data.strLen),'White'))
        right,bot=list2.left,list2.top
        data.pointerList.append(Pointer(60,200,200,225))
        for i in range(len(list1.startPoints)):
            left,top=list1.startPoints[i]
            data.pointerList.append(Pointer(left,top,right,bot))
    elif data.step==1:
        data.step+=1
        data.textList.pop(-1)
        data.textList.append(Txt(850,500,'a[0][0]=42','White'))
        data.listList[1].list[0]=42
    elif data.step==2:
        data.step+=1
        data.pointerList=[]
        data.textList.pop(-1)
        data.textList.append(Txt(850,400,'a=','White'))
        for i in range(data.strLen):
            data.textList.append(Txt(850,432+i*32,str([42]+[0]*(data.strLen-1)),'White'))
    elif data.step==3:
        data.flag='end'

def nextStep2d(data):
    if data.step==0:
        data.step+=1
        data.textList.append(Txt(50,100,'a','White'))
        data.textList.append(Txt(675,125,'b','White'))
        data.pointerList.append(Pointer(60,100,100,100))
        data.pointerList.append(Pointer(400+data.strLen*50,175,665,125))
        list1=TwodList(100,75,data.strLen)
        list2=TwodList(400,150,data.strLen)
        data.listList.append(list1)
        data.listList.append(list2)
        data.textList.append(Txt(850,500,'a=[[0]*%d\nfor i in range(%d)]'%(data.strLen,data.strLen),'White'))
        if data.flag=='2dCopy':
            data.textList.append(Txt(850,700,'b=copy.copy(a)','White'))
        else:
            data.textList.append(Txt(850,700,'b=\ncopy.deepcopy(a)','White'))
        for i in range(len(list1.startPoints)):
            left,top=list1.startPoints[i]
            data.listList.append(OnedList(100,200+(500/data.strLen)*i,data.strLen))
            data.pointerList.append(Pointer(left,top,100,225+(500/data.strLen)*i))
        if data.flag=='2dCopy':
            for i in range(len(list2.startPoints)):
                left,top=list2.startPoints[i]
                data.pointerList.append(Pointer(left,top,100,225+(500/data.strLen)*i))
        elif data.flag=='2dDeep':
            for i in range(len(list2.startPoints)):
                left,top=list2.startPoints[i]
                data.listList.append(OnedList(400,225+(500/data.strLen)*i,data.strLen))
                data.pointerList.append(Pointer(left,top,400,250+(500/data.strLen)*i))
    elif data.step==1:
        data.step+=1
        data.textList.pop(-1)
        data.textList.pop(-1)
        data.textList.append(Txt(850,500,'a[0][0]=42','White'))
        if data.flag=='2dDeep':
            data.listList[-data.strLen*2].list[0]=42
        elif data.flag=='2dCopy':
            data.listList[-data.strLen].list[0]=42
    elif data.step==2:
        data.step+=1
        data.textList.pop(-1)
        data.textList.append(Txt(850,220,'a=\n%s'%str([42]+[0]*(data.strLen-1)),'White'))
        data.pointerList=[]
        for i in range(data.strLen-1):
            data.textList.append(Txt(850,280+i*32,str([0]*data.strLen),'White'))
        if data.flag=='2dCopy':
            data.textList.append(Txt(850,500,'b=\n%s'%str([42]+[0]*(data.strLen-1)),'White'))
            for i in range(data.strLen-1):
                data.textList.append(Txt(850,560+i*32,str([0]*data.strLen),'White'))
        if data.flag=='2dDeep':
            data.textList.append(Txt(850,500,'b=','White'))
            for i in range(data.strLen):
                data.textList.append(Txt(850,532+i*32,str([0]*data.strLen),'White'))
    elif data.step==3:
        data.flag='end'

def nextStep1d(data):
    if data.step==0:
        data.step+=1
        data.textList.append(Txt(50,200,'a','White'))
        data.textList.append(Txt(50,400,'b','White'))
        data.listList.append(OnedList(200,200,data.strLen))
        data.pointerList.append(Pointer(60,200,200,220))
        data.textList.append(Txt(850,500,'a=\n%s'%str([0]*data.strLen),'White'))
        if data.flag=='1dCopy':
            data.listList.append(OnedList(200,500,data.strLen))
            data.pointerList.append(Pointer(60,400,200,520))
            data.textList.append(Txt(850,700,'b=\n%s'%'copy.copy(a)','White'))
        elif data.flag=='1dAlias':
            data.pointerList.append(Pointer(60,400,200,220))
            data.textList.append(Txt(850,700,'b=a','White'))
    elif data.step==1:
        data.textList.pop(-1)
        data.textList.pop(-1)
        data.textList.append(Txt(850,500,'a[0]=42','White'))
        data.step+=1
        data.listList[0].list[0]=42
    elif data.step==2:
        data.step+=1
        data.textList.pop(-1)
        data.pointerList=[]
        data.textList.append(Txt(850,500,'a=\n%s'%str(data.listList[0].list),'White'))
        if data.flag=='1dAlias':
            data.textList.append(Txt(850,700,'b=\n%s'%str(data.listList[0].list),'White'))
        elif data.flag=='1dCopy':
            data.textList.append(Txt(850,700,'b=\n%s'%str(data.listList[1].list),'White'))
    elif data.step==3:
        data.flag='end'

def drawButton(canvas,data):
    if data.flag=='starter':
        canvas.create_text(data.width/2,data.height/3,text='112 List Visualization',font='Ariel 36')
        canvas.create_rectangle(data.but1L,data.but1T,data.but1R,data.but1B,fill
                                ='White')
        canvas.create_text((data.but1L+data.but1R)/2,(data.but1T+data.but1B)/2,
                           text='1D List',font='Ariel 24')
        canvas.create_rectangle(data.but2L,data.but2T,data.but2R,data.but2B,fill
                                ='White')
        canvas.create_text((data.but2L+data.but2R)/2,(data.but2T+data.but2B)/2,
                           text='2D List',font='Ariel 24')
    elif data.flag=='1d':
        canvas.create_text(data.width/2,data.height/3,text='1D List Visualization',font='Ariel 36')
        canvas.create_rectangle(data.but1L,data.but1T,data.but1R,data.but1B,fill
                                ='White')
        canvas.create_text((data.but1L+data.but1R)/2,(data.but1T+data.but1B)/2,
                           text='1D Alias',font='Ariel 24')
        canvas.create_rectangle(data.but2L,data.but2T,data.but2R,data.but2B,fill
                                ='White')
        canvas.create_text((data.but2L+data.but2R)/2,(data.but2T+data.but2B)/2,
                           text='1D Copy',font='Ariel 24')
    elif data.flag=='2d':
        canvas.create_text(data.width/2,data.height/3,text='2D List Visualization',font='Ariel 36')
        canvas.create_rectangle(data.but1L,data.but1T,data.but1R,data.but1B,fill
                                ='White')
        canvas.create_text((data.but1L+data.but1R)/2,(data.but1T+data.but1B)/2,
                           text='False Creation',font='Ariel 24')
        canvas.create_rectangle(data.but2L,data.but2T,data.but2R,data.but2B,fill
                                ='White')
        canvas.create_text((data.but2L+data.but2R)/2,(data.but2T+data.but2B)/2,
                           text='Shallow Copy',font='Ariel 24')
        canvas.create_rectangle(data.but3L,data.but3T,data.but3R,data.but3B,fill
                                ='White')
        canvas.create_text((data.but3L+data.but3R)/2,(data.but3T+data.but3B)/2,
                           text='Deep Copy',font='Ariel 24')
    elif (data.flag=='1dAlias' or data.flag=='1dCopy' or data.flag=='2dFalse' or 
          data.flag=='2dCopy' or data.flag=='2dDeep'):
        canvas.create_rectangle(data.but4L,data.but4T,data.but4R,data.but4B,fill
                                ='White')
        canvas.create_text((data.but4L+data.but4R)/2,(data.but4T+data.but4B)/2,
                           text='NextStep',font='Ariel 24')
        if data.flag=='1dAlias':
            canvas.create_text(50,750,text='1D List Alias',anchor='w',
                               fill='White',font='Ariel 24')
        elif data.flag=='1dCopy':
            canvas.create_text(50,750,text='1D List copy.copy()',anchor='w',
                               fill='White',font='Ariel 24')
        elif data.flag=='2dFalse':
            canvas.create_text(50,750,text='2D List False Creation',anchor='w',
                               fill='White',font='Ariel 24')
        elif data.flag=='2dCopy':
            canvas.create_text(50,750,text='2D List Shallow Copy',anchor='w',
                               fill='White',font='Ariel 24')
        elif data.flag=='2dDeep':
            canvas.create_text(50,750,text='2D List Deep Copy',anchor='w',
                               fill='White',font='Ariel 24')

def drawWin(canvas,data):
    for item in data.pointerList:
        canvas.create_line(item.left,item.top,item.right,item.bot,fill='White')
    for item in data.listList:
        for i in range(item.len):
            canvas.create_rectangle(item.left+i*item.blockWid,item.top,
                                    item.left+(i+1)*item.blockWid,
                                    item.top+item.blockHgt,outline='White')
            if isinstance(item,OnedList):
                for i in range(item.len):
                    cenX,cenY=item.textCenter[i]
                    canvas.create_text(cenX,cenY,text=str(item.list[i]),
                                       fill='White',font='Ariel 24')
    for item in data.textList:
        canvas.create_text(item.cenX,item.cenY,text=item.text,fill=item.color,
                           font='Ariel 24')

def drawEnd(canvas,data):
    canvas.create_text(300,300,text='Finished all steps',fill='White',font='Ariel 24')
    canvas.create_text(300,400,text='Press Enter to return to main menu',
                       fill='White',font='Ariel 24')

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill='grey')
    if data.flag!='starter' and data.flag!='1d' and data.flag!='2d':
        canvas.create_rectangle(0,50,data.animWid,data.animHgt+50,fill='black')
        canvas.create_text(50,25,text='List Visualization',anchor='w',
                           fill='White',font='Ariel 24')
    drawButton(canvas,data)
    if (data.flag=='1dAlias' or data.flag=='1dCopy' or data.flag=='2dFalse' or 
        data.flag=='2dCopy' or data.flag=='2dDeep'):
        drawWin(canvas,data)
    if data.flag=='end':
        drawEnd(canvas,data)

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

run(400, 200)