from utils import printState, move


class Node:
    def __init__(self, state, parent, actionFromParent, depth):
        self.state = "".join(state)  # self.state is string
        self.parent = parent
        # Action taken by parent to come to this state
        self.actionFromParent = actionFromParent
        self.depth = depth  # I set the depth itself as the cost of the node.
        self.heuristic = self.calcH1() + self.calcH2()
        self.evaluation = self.depth + self.heuristic  # f(n) = g(n) + h(n)

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
        return Node(nextState, self, action, self.depth + 1)
