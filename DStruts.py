class queue():
    def __init__(self) -> None:
        self.__data = []

    def pop(self):
        try:
            value = self.__data[0]
            del self.__data[0]
            return value
        except:
            return -1
        
    def push(self,value):
        self.__data.append(value)
    
    def peak(self):
        try:
            return self.__data[0]
        except:
            return -1
        
    def get(self):
        return self.__data
        

class priorityQueue():
    def __init__(self) -> None:
        self.__data = []

    def push(self,value,priority):
        try:
            value = int(value)
        except:
            pass

        try:
            priority = int(priority)
        
        except:
            priority = 0
        

        if len(self.__data) == 0:
            self.__data.append((value,priority))
            return
    
        for i in range(len(self.__data)):
            print(self.__data[i])
            if self.__data[i][1]>=priority:
                self.__data.insert(i,(value,priority))
                return
        
        self.__data.append((value,priority))

    def pop(self):
        try:
            return self.__data.pop()
        except:
            return self.__data
        
    def get(self):
        return self.__data
        

class stack():
    def __init__(self) -> None:
        self.__data = []

    def push(self,value):
        self.__data.append(value)

    def pop(self):
        try:
            return self.__data.pop()
        except:
            return self.__data()
        
    def peak(self):
        try:
            return self.__data[-1]
        except:
            return self.__data
        
    def get(self):
        return self.__data
    