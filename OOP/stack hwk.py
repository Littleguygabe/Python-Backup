import random

class Stack():
    INDENT="      "
    BOTTOM="------------"
    TOP = "   TP>"
    SIDE ="|"
    def __init__(self,Name="Example Stack",Max=20):
        self._Size=0
        self._Max = Max
        self.Name = Name
        self._items=['']*self._Max

        self.frontPointer = 0

    def getSize(self):
        return self.frontPointer

    def getMax(self):
        return self._Max

    def isEmpty(self):
        pass

    def isFull(self):
        pass

    def push(self,value):
        if self.frontPointer<= self._Max:
            self._items[self.frontPointer] = value
            self.frontPointer+=1
            self._Size+=1
        
        else:
            print('Stack is full')
        
    def pop(self):
        if self.frontPointer>=0:
            self._items[self.frontPointer] = ''
            self.frontPointer+=1
            self._Size+=1
            print(self._items)
    
        else:
            print('stack is empty')
    def peek(self):
        topVal = self._items[self.frontPointer-1]
        return topVal


    def display(self,Name):
        print("\n\n {0}{1:^10s}\n".format(Stack.INDENT,Name))
        print(Stack.TOP,end="")
        print(Stack.SIDE,end="")
        print("{:^10s}".format(self._items[0]),end="")
        print(Stack.SIDE)
        for index in range(1,self._Size):
            print(Stack.INDENT,end="")
            print(Stack.SIDE,end="")
            print("{:^10s}".format(self._items[index]),end="")
            print(Stack.SIDE)
        print(Stack.INDENT+Stack.BOTTOM)
#main
StackOne=Stack("Stack One")
menu= "\tStack Menu\n\n\t0: End\n\t1: Enter Item (Push)\n\t2: Remove Item (POP)\n\t3: Check Size\n\t4: Peek\n\t5: Display Stack\n\n\tSelect>>"
Selection =9
while Selection!=0:
    Selection=int(input(menu))
    print("\n\n\n")
    if Selection == 1:
        Item = input("Enter Item to add to Stack >>")
        StackOne.push(Item)
    elif Selection == 2:
        Item = StackOne.pop()
        if Item !=None:
            print("Item popped from stack: {0}".format(Item))
    elif Selection == 3:
        print("Number of items on stack is {0}, maximum allowed is {1}".format(StackOne.getSize(),StackOne.getMax()))
    elif Selection ==4:
        Item = StackOne.peek()
        if Item !=None:
            print("Item at top of stack is {0}".format(Item))
    elif Selection==5:
        StackOne.display(StackOne.Name)
    print("\n\n\n")