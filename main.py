#!/usr/bin/env python3
from game.engine import Engine

__author__ = 'Cody Huzarski'


def main():

    engine = Engine()

    engine.initGame()
    while engine.getStateFlag() != engine.stateFlags[0]:
        engine.update()
        engine.takeInput()

main()