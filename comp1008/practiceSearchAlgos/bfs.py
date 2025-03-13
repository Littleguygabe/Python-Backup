import random

class Queue():
    def __init__(self) -> None:
        self.queue = []

    def push(self,x):
        self.queue.append(x)

    def pop(self):
        popped = self.queue.pop(0)
        return popped


def bfs(maze):
    searchQueue = Queue()



# Create an empty 10x10 grid filled with walls
maze = [['X','X','X','X','X','X','X','X','X','X'],
        ['0',' ',' ',' ',' ',' ',' ',' ',' ','X'],
        ['X',' ',' ',' ',' ',' ',' ',' ',' ','X'],
        ['X',' ',' ',' ',' ',' ',' ',' ',' ','X'],
        ['X',' ',' ',' ',' ',' ',' ',' ',' ','X'],
        ['X',' ',' ',' ',' ',' ',' ',' ',' ','X'],
        ['X',' ',' ',' ',' ',' ',' ',' ',' ','X'],
        ['X',' ',' ',' ',' ',' ',' ',' ',' ','X'],
        ['X',' ',' ',' ',' ',' ',' ',' ',' ','1'],
        ['X','X','X','X','X','X','X','X','X','X'],
        ]

for row in maze:
    print(' '.join(row))

