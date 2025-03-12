equation = input()
class lists():
    def __init__(self):
        self.stack = []
    
    def push(self,x):
        self.stack.append(x)
    
    def pop(self,x):
        self.stack.pop()

stack1 = lists