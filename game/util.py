__author__ = 'Cody Huzarski'

import time, sys, os

def tokenize(inStr):
    inStr = str(inStr)
    tokens = []
    ## Tokenizes a string based upon spaced
    tokens = inStr.split(" ")
    return tokens

def typewrite(chars, rate=0.04, lineBreak=True):
    # chars = str(chars) #ensure we are using a string
    #
    # for c in chars:
    #     sys.stdout.write(c)
    #     sys.stdout.flush()
    #     time.sleep(rate)
    #
    # if lineBreak == True:
    #     sys.stdout.write('\n')
    #     sys.stdout.flush()

    print(chars)
def clearScn():
    if sys.platform == "linux" or sys.platform == "darwin":
        os.system("clear")
    elif sys.platform == "win32":
        os.system("cls")