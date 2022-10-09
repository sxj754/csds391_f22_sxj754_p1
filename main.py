import random
from utils import printState, move, randomizeState
from astar import solveAStar

STATE = []
random.seed(11)
MAX_NODES = 0


def solveLocalBeam():
    pass


with open("command.txt") as file:
    commands = file.readlines()
    for command in commands:
        args = command.split()

        if args[0] == "setState":
            state = args[1] + args[2] + args[3]
            STATE = list(state)
            print("State set")
            printState(STATE)

        elif args[0] == "printState":
            printState(STATE)

        elif args[0] == "move":
            result = move(STATE, args[1])
            if result:
                STATE = result

        elif args[0] == "randomizeState":
            STATE = randomizeState(args[1])

        elif args[0] == "solve":
            if args[1] == "A-star":
                STATE = solveAStar(STATE)

            elif args[1] == "beam":
                solveLocalBeam()
