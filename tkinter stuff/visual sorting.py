from tkinter import *
import random, time, winsound
root = Tk()
width = 870
height = 950
root.geometry('1000x1000')
sleeptime = 0

clicked = StringVar()
clicked.set('Bubble')

sortTypes = ['Bubble',
            'Insertion',
            'Selection',
            'Quick',
            'Cocktail',]

canvas = Canvas(root,width = width, height = height,bg='gray')

hex='#000000'

def rgb_to_hex(event):
    global hex
    r = red.get()
    g = green.get()
    b = blue.get()
    hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    drawlines(randarray)

def drawlines(randarray):
    #rgb_to_hex()
    canvas.delete('all')
    margin = width/len(randarray)
    offset=5
    for i in range(0,len(randarray)):
        yval = (randarray[i]/slider1.get())*height
        canvas.create_line(offset,yval,offset,0,fill = hex , width = margin)
        offset+=margin
        Tk.update(root)
        
        #play corresponding sound
        freq = int((yval/height)*2500)+37
        winsound.Beep(freq,25)

def createarray():
    canvas.delete('all')
    red['state'] = 'normal'
    green['state'] = 'normal'
    blue['state'] = 'normal'
    global randarray
    randarray = []
    sliderval = slider1.get()
    while len(randarray)!=sliderval:
        randomnum = random.randint(1,sliderval)
        if randomnum not in randarray:
            randarray.append(randomnum)
    drawlines(randarray)

def bubblesort():
    slider1['state'] = 'disabled'
    solved = False
    start=time.time()
    passes = 0
    while not solved:
        time.sleep(sleeptime)
        changes = 0
        passes+=1
        for i in range(0,len(randarray)-1):
            temp1 = randarray[i]
            temp2 = randarray[i+1]
            if temp1>temp2:
                randarray[i+1] = temp1
                randarray[i] = temp2
                changes+=1
        drawlines(randarray)

        if changes == 0:
            solved = True

    timecount = time.time()-start
    print(f'sorted in {timecount}s')
    print(f'{passes} passes')
    slider1['state'] = 'normal'

def insertionSort():
    passes = 0
    start = time.time()
     
    if (n := len(randarray)) <= 1:
      return
    for i in range(1, n):
        key = randarray[i]
        j = i-1
        while j >=0 and key < randarray[j] :
                randarray[j+1] = randarray[j]
                j -= 1
                
        randarray[j+1] = key
        drawlines(randarray)
        passes+=1
        time.sleep(sleeptime)
        
    timecount = time.time() - start
    print(f'sorted in {timecount}s')
    print(f'{passes} passes')


def selectionSort():
    passes = 0
    start = time.time()
    for base in range(0,len(randarray)-1):
        #minimum algorithm
        minimum = len(randarray)
        minimumIndex = 0
        for i in range(base,len(randarray)):
            if randarray[i]<minimum:
                minimum = randarray[i]
                minimumIndex = i

        temp1 = randarray[base]
        randarray[minimumIndex] = temp1

        randarray[base] = minimum

        passes+=1
        drawlines(randarray)

    timecount = time.time()-start
    print(f'sorted in {timecount}s')
    print(f'{passes} passes')
    
def quicksort(array):

    start = time.time()
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)

        
        if len(less)>0:
            drawlines(less)
        if len(equal)>0:
            drawlines(equal)
        if len(greater)>0:
            drawlines(greater)


        return quicksort(less)+equal+quicksort(greater)
    else:
        timecount = time.time()-start
        print(f'sorted in {timecount}s')
        return array
        

def sortdetection():
    if clicked.get() == 'Bubble':
        bubblesort()

    elif clicked.get() == 'Insertion':
        insertionSort()

    elif clicked.get() == 'Selection':
        selectionSort()

    elif clicked.get() == 'Quick':
        drawlines(quicksort(randarray))

    elif clicked.get() == 'Cocktail':
        cocktailsort()


def cocktailsort():
    start = time.time()
    sorted = False
    while sorted == False:
        for i in range(0,round(len(randarray)/2)):
            changes = 0
            lowerindex = i
            upperindex = len(randarray)-1-i

            templower = randarray[lowerindex]
            if randarray[lowerindex]>randarray[lowerindex+1]:
                randarray[lowerindex] = randarray[lowerindex+1]
                randarray[lowerindex+1] = templower
                changes+=1
                drawlines(randarray)

            tempupper = randarray[upperindex]
            if randarray[upperindex]<randarray[upperindex-1]:
                randarray[upperindex]=randarray[upperindex-1]
                randarray[upperindex-1]=tempupper
                changes+=1
                drawlines(randarray)


            if changes == 0:
                sorted = True
    
    timecount = time.time() - start
    print(f'finished in {timecount}s')
    print(randarray)



label1 = Label(root, text = 'Array Length')
slider1 = Scale(root,from_=1, to=100, orient=HORIZONTAL, length=100)
arraybutton = Button(root, text = 'Generate Array',padx = 6, command = createarray)
sortbutton = Button(root,text = 'Sort',padx = 35,command = sortdetection)

rlabel = Label(root, text = 'Red')
red = Scale(root,from_=0, to=255, orient=HORIZONTAL, length=100,command=rgb_to_hex, state='disabled')

glabel = Label(root, text = 'Green')
green = Scale(root,from_=0, to=255, orient=HORIZONTAL, length=100,command=rgb_to_hex, state='disabled')

blabel = Label(root, text = 'Blue')
blue = Scale(root,from_=0, to=255, orient=HORIZONTAL, length=100,command=rgb_to_hex, state='disabled')

dropdown = OptionMenu(root,clicked, *sortTypes,)

slider1.grid(column = '0',row = '1')
label1.grid(column = '0',row = '0')
arraybutton.grid(column = '0',row = '2')
sortbutton.grid(column = '0',row = '3')
canvas.grid(column = '2',row = '1', rowspan=300)

rlabel.grid(column='0',row='6')
red.grid(column='0',row='5')

glabel.grid(column='0',row='8')
green.grid(column='0',row='7')

blabel.grid(column='0',row='10')
blue.grid(column='0',row='9')

dropdown.grid(column = '0',row='4')

root.mainloop()