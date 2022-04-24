import math
import random
from tkinter import *


def hueristic(a, z):
    dist = abs(a.i - z.i) + abs(a.j - z.j)
    return dist


x = 15
y = 20
grid = [[0 for w in range(y)] for h in range(x)]

open_set = []
closed_set = []


class cell:

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.show = 'white'
        self.neighbors = []
        self.prev = None
        self.barrier = False

    def random_barrier(self):
        if(random.randint(0, 10) < 5):
            self.barrier = True

    def find_neighbors(self):
        neighbors = []
        if self.i < (x - 1):
            if grid[self.i + 1][self.j].barrier == False:
                neighbors.append(grid[self.i + 1][self.j])
        if self.i > 0:
            if grid[self.i - 1][self.j].barrier == False:
                neighbors.append(grid[self.i - 1][self.j])
        if self.j < (y - 1):
            if grid[self.i][self.j + 1].barrier == False:
                neighbors.append(grid[self.i][self.j + 1])
        if self.j > 0:
            if grid[self.i][self.j - 1].barrier == False:
                neighbors.append(grid[self.i][self.j - 1])

        if self.i < (x - 1) and self.j < (y - 1):
            if grid[self.i + 1][self.j + 1].barrier == False:
                neighbors.append(grid[self.i + 1][self.j + 1])
        if self.i > 0 and self.j < (y - 1):
            if grid[self.i - 1][self.j + 1].barrier == False:
                neighbors.append(grid[self.i - 1][self.j + 1])
        if self.i < (x - 1) and self.j > 0:
            if grid[self.i + 1][self.j - 1].barrier == False:
                neighbors.append(grid[self.i + 1][self.j - 1])
        if self.i > 0 and self.j > 0:
            if grid[self.i - 1][self.j - 1].barrier == False:
                neighbors.append(grid[self.i - 1][self.j - 1])

        self.neighbors = neighbors


for i in range(0, x):
    for j in range(0, y):
        grid[i][j] = cell(i, j)

start = grid[0][0]

end = grid[x - 1][y - 1]
end.show = 'blue'

for i in range(0, x):
    for j in range(0, y):
        if grid[i][j] != start and grid[i][j] != end:
            grid[i][j].random_barrier()
            if grid[i][j].barrier == True:
                grid[i][j].show = 'black'
for i in range(0, x):
    for j in range(0, y):
        grid[i][j].find_neighbors()


open_set.append(start)

for i in range(len(open_set)):
    open_set[i].show = 'green'

for i in range(len(closed_set)):
    closed_set[i].show = 'red'

root = Tk()
button_grid = [[0 for w in range(y)] for h in range(x)]
for col in range(x):
    for row in range(y):
        button_grid[col][row] = Button(
            root, padx=10, pady=5, borderwidth=0, text="%s" % (grid[col][row].f))
        button_grid[col][row].grid(row=row, column=col, sticky="nsew")

over = False
while len(open_set) > 0 and over == False:
    for col in range(x):
        for row in range(y):
            if grid[col][row].f == 0:
                button_grid[col][row]['text'] = str(grid[col][row].f) + '0'
            else:
                button_grid[col][row]['text'] = grid[col][row].f
            button_grid[col][row]['bg'] = grid[col][row].show

    lowest_index = 0
    for i in range(len(open_set)):
        if open_set[i].f < open_set[lowest_index].f:
            lowest_index = i
    current = open_set[lowest_index]

    if current == end:
        current.prev.show = 'blue'
        over = True

    open_set.remove(current)
    closed_set.append(current)

    neighbors = current.neighbors
    for i in range(len(neighbors)):
        neighbor = neighbors[i]
        if neighbor not in closed_set:
            g_is_less = False
            g = current.g + 1
            if neighbor in open_set:
                if g < neighbor.g:
                    neighbor.g = g
                    g_is_less = True
            else:
                neighbor.g = g
                open_set.append(neighbor)
                g_is_less = True
            if g_is_less:
                neighbor.h = hueristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.prev = current

    for i in range(len(open_set)):
        open_set[i].show = 'green'

    for i in range(len(closed_set)):
        closed_set[i].show = 'red'
    current.show = 'blue'
    path = []
    temp = current
    path.append(temp)
    while(temp.prev):
        temp.prev.show = 'blue'
        path.append(temp.prev)
        temp = temp.prev
    root.update()
    end.show = 'blue'

root.mainloop()
