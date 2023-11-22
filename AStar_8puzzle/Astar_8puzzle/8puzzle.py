from copy import deepcopy

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
print("Initial:")
startmatrix = []
for j in range(3):
    temp = input().split(" ")
    if temp[j] == 'X':
        temp[j] = 0
    temp = list(int(i) for i in temp)
    startmatrix.append(temp)

# print(startmatrix)

print()
print("Goal:")
EndMatrix = []
for j in range(3):
    temp = input().split(" ")
    if temp[j] == 'X':
        temp[j] = 0
    temp = list(int(i) for i in temp)
    EndMatrix.append(temp)


# print(EndMatrix)


def print_puzzle(array):
    for a in range(len(array)):

        for i in array[a]:
            if i == 0:
                print('X', end=" ")
            else:
                print(i, end=" ")
        print('')


class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h


def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))


def ManhattanDis(current_state):
    dis = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(EndMatrix, current_state[row][col])
            dis += abs(row - pos[0]) + abs(col - pos[1])
    return dis


def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0

            listNode.append(Node(newState, node.current_node, node.g + 1, ManhattanDis(newState), dir))

    return listNode


def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode


def shortestPath(closedSet):
    node = closedSet[str(EndMatrix)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch


def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, ManhattanDis(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == EndMatrix:
            return shortestPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]


if __name__ == '__main__':
    start= main(startmatrix)

    print()
    count = 0

    for b in start:
        count += 1
        print(f'step #{count}')
        print_puzzle(b['node'])
