import random


def printState(state):
    print(" ".join(state[0:3]))
    print(" ".join(state[3:6]))
    print(" ".join(state[6:9]))
    print()


def move(state, direction):
    if isinstance(state, str):  # Check if the state is string
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
    state = "b12345678"
    directionList = ["up", "down", "left", "right"]
    i = 0
    print("========== randomizing ==========")
    while i < int(n):
        randomIdx = random.randint(0, 3)
        result = move(state, directionList[randomIdx])
        if result:  # Add 1 only if the move was successful
            state = result
            printState(state)
            i += 1
    return state


def traceBack(node):
    # Recursive function to trace action
    if node.parent == None:
        return []
    else:
        return traceBack(node.parent) + [node.actionFromParent]
