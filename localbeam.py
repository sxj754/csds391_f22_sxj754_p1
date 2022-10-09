from node import Node
from utils import printState


def solveLocalBeam(startState, k):
    def sortKey(node):
        return node.evaluation

    def traceBack(node):
        # Recursive function to trace action
        if node.parent == None:
            return []
        else:
            return traceBack(node.parent) + [node.actionFromParent]

    print("=" * 20, "Local Beam search start", "=" * 20)
    initNode = Node(startState, None, None, 0)  # Initial state
    currentNodes = [initNode]  # contains nodes
    neighborNodes = []
    sequences = []  # Sequences of action from the starting state to the goal state

    print("start: ", list(map(lambda node: node.state, currentNodes)))

    # loop
    while True:
        if currentNodes[0].state == "b12345678":
            # Test if it is a goal state
            # Use currentNodes[0] because it will always be the closest node
            # from the goal state among the neighbors
            sequences = traceBack(currentNodes[0])
            print("\n========== finished ==========")
            print("initial state")
            printState(initNode.state)
            print("sequences: ", " - ".join(sequences))
            print("depth: ", currentNodes[0].depth)
            return currentNodes[0].state

        print("\n===== depth", currentNodes[0].depth, "=====")

        for node in currentNodes:
            possibleActions = node.findPossibleAction()
            for action in possibleActions:
                child = node.makeChildNode(action)
                if len(neighborNodes) < int(k):
                    # if the length of neighbor is less than k
                    # just insert the node
                    neighborNodes.append(child)
                elif all(node.evaluation < child.evaluation for node in neighborNodes):
                    # if the length of neighbor is greater than or equal to k
                    # and the evaluation of every node is less than the child,
                    # just discard the child
                    continue
                else:
                    # if something's evaluation is bigger than current child,
                    # discard the biggest thing and append current child
                    neighborNodes.pop()
                    neighborNodes.append(child)

                # Sort
                neighborNodes.sort(key=sortKey)
                print(list(map(lambda node: node.state, neighborNodes)))

        currentNodes = neighborNodes  # change current to it's child
        neighborNodes = []  # refresh the neighbor node

        # find successors of currentNode
        # sort it from the smallest to the biggest, and slice k items, add to the todo
        # repeat
