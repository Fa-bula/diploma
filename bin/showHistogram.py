#!/usr/bin/python
import matplotlib.pyplot as plt
import os
import analyseMutations as am
import sys

def showHist(dataFile, outDir, ignoreValue):
    """ Shows histogram of values, stored in file, ignoring some
    values, for example -1, because -1 is no replication timing """
    values = []
    with open(dataFile, 'r') as readFile:
        for line in readFile:
            currentValue = float(line)
            if currentValue != ignoreValue:
                values.append(currentValue)

    plt.hist(values)
    outFileName = os.path.join(outDir, os.path.basename(dataFile) + '.png')
    plt.savefig(outFileName)
    return


def drawAllPlots(dataDir, outputDir):
    fileNames = am.onlyFiles(dataDir)
    for fileName in fileNames:
        y = []
        with open(fileName) as readFile:
            for line in readFile:
                y.append(float(line))
        del y[0]
        x = [10 * i for i in range(9)]
        plt.bar(x, y, width=10)
        # plt.show()
        plt.savefig(os.path.join(outputDir,
                                 os.path.basename(fileName)))
    return



if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: {0} dataDir outDir'.format(sys.argv[0]))

    drawAllPlots(sys.argv[1], sys.argv[2])
    

    
# #!/bin/bash
# ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
# BIN=$ROOT/bin
# DATA=$ROOT/breast_canser_data/mutation_replication_time
# for file in $DATA/*; do
#     $BIN/showHistogram.py $file
# done
