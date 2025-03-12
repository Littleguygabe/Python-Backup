class LinkedList():
    def __init__(self) -> None:
        self.head = None
        
    def addNode(self,data):
        if not self.head:
            self.head = Node(data)

        else:
            current = self.head
            while current.next:
                current = current.next

            current.next = Node(data)

    def printList(self):
        cur = self.head
        while cur:
            print(cur.data,end=' -> ')
            cur = cur.next

        print('None')

class Node():
    def __init__(self,data) -> None:
        self.data = data
        self.next = None

def main():

    ll = LinkedList()
    for i in range(10):
        ll.addNode(i+1)

    ll.printList()
    

if __name__ == '__main__':
    main()