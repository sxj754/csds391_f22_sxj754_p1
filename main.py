from ast import Str
import random

STATE = []
# STATE is a 3x3 2-dimentional array
# Ex) [[b, 1, 2],
#      [3, 4, 5],
#      [6, 7, 8]]

MAX_NODES = 0


def setState(state):
    global STATE
    STATE = list(state)
    print("State set")
    printState(STATE)


def printState(state):
    print(" ".join(state[0:3]))
    print(" ".join(state[3:6]))
    print(" ".join(state[6:9]))
    print()


def move(state, direction):
    if type(state) == type("aaaaaaaaaaaaaa"):
        state = list(state)
    idx = state.index("b")
    if direction == "up":
        if idx < 3:  # First row
            return 0
        state[idx] = state[idx - 3]
        state[idx - 3] = "b"
        print("Blank was moved up")

    elif direction == "down":
        if idx > 5:  # Third row
            return 0
        state[idx] = state[idx + 3]
        state[idx + 3] = "b"
        print("Blank was moved down")

    elif direction == "left":
        if idx % 3 == 0:
            return 0
        state[idx] = state[idx - 1]
        state[idx - 1] = "b"
        print("Blank was moved left")

    elif direction == "right":
        if idx % 3 == 2:
            return 0
        state[idx] = state[idx + 1]
        state[idx + 1] = "b"
        print("Blank was moved right")

    return state


def randomizeState(n):
    global STATE
    setState("b12345678")
    directionList = ["up", "down", "left", "right"]
    i = 0
    while i < int(n):
        randomIdx = random.randint(0, 3)
        result = move(STATE, directionList[randomIdx])
        if result:  # Add 1 if the move was successful
            STATE = result
            printState(STATE)
            i += 1


class Node:
    def __init__(self, state, parent, depth):
        self.state = "".join(state)
        self.parent = parent
        self.depth = depth
        self.heuristic = self.calcH1() + self.calcH2()

    def calcH1(self):
        # h1 is the number of misplaced tiles
        goal = "b12345678"
        h1 = 0
        for i in range(9):
            if self.state[i] != goal[i]:
                h1 += 1
        return h1

    def calcH2(self):
        # h2 is the sum of the distances of the tiles from their goal positions
        goal = "b12345678"
        h2 = 0
        for idx, item in enumerate(self.state):
            curIdx = idx
            goalIdx = goal.index(item)
            row = curIdx // 3
            col = curIdx % 3
            goalRow = goalIdx // 3
            goalCol = goalIdx % 3

            deltaRow = abs(goalRow - row)
            deltaCol = abs(goalCol - col)
            h2 += deltaRow + deltaCol
        return h2

    def findPossibleAction(self):
        # Find possible actions from a certain state
        action = ["up", "down", "left", "right"]
        idx = self.state.index("b")

        if idx < 3:
            action.pop(action.index("up"))
        elif idx > 5:
            action.pop(action.index("down"))

        if idx % 3 == 0:
            action.pop(action.index("left"))
        elif idx % 3 == 2:
            action.pop(action.index("right"))

        return action

    def makeChildNode(self, action):
        nextState = move(self.state, action)
        printState(nextState)
        return Node(nextState, self, self.depth + 1)


def solveAStar(startState):
    def isGoal(state):
        if state == "b12345678":
            return 1
        else:
            return 0

    print("=" * 20, "A-Star search start", "=" * 20)
    initNode = Node(startState, None, 0)  # Initial state
    frontier = [initNode]  # contains nodes
    explored = []  # contains states
    actions = []  # Contains possible actions of a node

    # loop
    while len(frontier) != 0:
        currentNode = frontier.pop(0)
        if isGoal(currentNode.state):
            return currentNode
        explored.append(currentNode.state)
        actions = currentNode.findPossibleAction()

        for action in actions:  # search children
            print("\n===== loop =====")
            frontierStates = list(map(lambda node: node.state, frontier))
            child = currentNode.makeChildNode(action)
            if child.state not in explored and child.state not in frontierStates:
                # Insert child to an appropriate index of frontier
                # by finding the first index bigger than the child's heuristic
                if len(frontier) == 0:
                    frontier.append(child)
                elif all(node.heuristic < child.heuristic for node in frontier):
                    # If nothing is bigger than child's heuristic,
                    # just append at the end of the list
                    frontier.append(child)
                else:
                    for idx, node in enumerate(frontier):
                        if node.heuristic > child.heuristic:
                            frontier.insert(idx, child)
                            break

            elif child.state in frontierStates:
                # Find the index with same state and then check the heuristic
                # If this child's heuristic is smaller, change the node.
                idx = frontierStates.index(child.state)
                if frontier[idx].heuristic > child.heuristic:
                    frontier[idx] = child
            print("frontier: ", list(map(lambda node: node.state, frontier)))
            print("explored: ", explored)
            print("heuristic: ", child.heuristic)
        # TODO: traceback

    return 0


def solveLocalBeam():
    pass


with open("command.txt") as file:
    commands = file.readlines()
    for command in commands:
        args = command.split()

        if args[0] == "setState":
            state = args[1] + args[2] + args[3]
            setState(state)

        elif args[0] == "printState":
            printState(STATE)

        elif args[0] == "move":
            move(STATE, args[1])

        elif args[0] == "randomizeState":
            randomizeState(args[1])

        elif args[0] == "solve":
            if args[1] == "A-star":
                result = solveAStar(STATE)
                print("\nfinished: ", result.state)
                print("depth: ", result.depth)

            elif args[1] == "beam":
                solveLocalBeam()
