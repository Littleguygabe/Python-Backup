class stack():
    def __init__(self) -> None:
        self.values = []
        
    def push(self,x):
        self.values.append(x)
        
    def pop(self):
        return self.values.pop(-1)
    
    def clear(self):
        self.values = []

def calculate(right,left,operator):
    if operator == '+':
        return left+right
    elif operator == '-':
        return left-right
    elif operator == '*':
        return left*right
    elif operator == '/':
        return left/right


def evaluateRPN(RPNequation):
    stack1 = stack()
    for character in RPNequation:
        try:
            intVal = int(character)
            stack1.push(intVal)
            
        except:
            right = stack1.pop()
            left = stack1.pop()
            
            result = calculate(right,left,character)
            
            stack1.push(result)
            
    result = stack1.pop()
    stack1.clear()
    return result

if __name__ == '__main__':
    print(evaluateRPN(str(input(':'))))