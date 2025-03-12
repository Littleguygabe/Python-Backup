import random, RPNevaluation

class equation():
    def __init__(self) -> None:
        self.expression = ''
        self.operators = ['+','-','*','/']
        
    def addToExpression(self,val):
        self.expression+=str(val)
        
    def findOperator(self,val):
        return self.operators[val]
    
    def clear(self):
        self.expression = ''
    
def createEquation(Nvals):
    for i in range(2):
        val = random.randint(1,9)
        equation1.addToExpression(val)
    
    operatorVal = random.randint(0,3)
    operator = equation1.findOperator(operatorVal)
    equation1.addToExpression(operator)
    
    for i in range(Nvals-2):
        equation1.addToExpression(random.randint(1,9))
        operatorVal = random.randint(0,3)
        operator = equation1.findOperator(operatorVal)
        equation1.addToExpression(operator)
        
    expression = equation1.expression
    equation1.clear()
    return expression

def inputEquation():
    Len = int(input('Enter the Amount of Values: '))
    while Len<2:
        print('Not Long Enough')
        Len = int(input('Enter the Amount of Values: '))
        
    return Len

def checkAnswer(Finalequation):
    UserAnswer = float(input('Enter Your Answer (3 dp): '))
    
    answer = round(RPNevaluation.evaluateRPN(Finalequation),3)
    if UserAnswer == answer:
        return True,None
    else:
        return False,answer

while True:
    equation1 = equation()
    EqLen = inputEquation()
    Finalequation = createEquation(EqLen)
    print(Finalequation)
    correct,answer = checkAnswer(Finalequation)
    if correct:
        print('Correct!')
    else:
        print(f'Incorrect, answer is: {answer}')
    
    
        
    