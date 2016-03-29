#!/usr/bin/python
import matplotlib.pyplot as plt
import os
import sys

def showHist(fileName, ignoreValue):
    """ Shows histogram of values, stored in file, ignoring some values """
    values = []
    with open(fileName, 'r') as readFile:
        for line in readFile:
            currentValue = float(line)
            if currentValue != ignoreValue:
                values.append(currentValue)

    plt.hist(values)
    plt.savefig(fileName + '.png')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        showHist(sys.argv[1], -1)
    else:
        print('Usage: {0} data'.format(sys.argv[0]))
    

    
