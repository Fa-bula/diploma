#!/usr/bin/python
import os
import sys
import analyseMutations as am

# Normalize number of mutations with each replication time
# by number of APOBEC-motifs in genome with this replication time
# This way, we get estimation of probability of mutation
# Writes to output file outDir/<sampleName>:
# <replicationTiming>\t<mutationProbability> 

def normalizeResults(borders, normalizer, dataDir, outDir):
    """ Split data in bins, defined by borders list.
    Then divide numberOfPointsInBin[i] by normalizer[i]
    IN: borders - list of bin's borders,
    normalizer - list of normalization coefficients
    dataDir - directory with data, should be splitted and normalized """
    if len(normalizer) != len(borders) + 1:
        sys.exit("Length of normalizer ({0}) should be equal to\
        number of bins({1})".format(len(normalizer), len(borders) + 1))

    dataFileNames = am.onlyFiles(dataDir)

    for dataFileName in dataFileNames:
        points = []
        with open(dataFileName, 'r') as dataFile:
            for line in dataFile:
                points.append(float(line))

        numberOfPointsInBin = am.splitToBins(points, borders)
        for i, normCoeff in enumerate(normalizer):
            numberOfPointsInBin[i] = numberOfPointsInBin[i] * 1.0 / normCoeff
        outFileName = os.path.join(outDir, os.path.basename(dataFileName))
        with open(outFileName, 'w') as outputFile:
            outputFile.write("replicationTiming\tprobability\n")
            for i, probability in enumerate(numberOfPointsInBin):
                if 0 == i or i + 1 == len(numberOfPointsInBin):
                    continue
                replicationTiming = 1.0 * (borders[i - 1] + borders[i]) / 2
                outputFile.write("{0}\t{1}\n".format(replicationTiming,
                                                   probability))
    return


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit("Usage: {0} motifRepTimeDir mutationRepTimeDir\
        outDir".format(sys.argv[0]))

    motifDir = sys.argv[1]
    normalizer = [0] * (len(am.BIN_START) + 1)
    motifRepTimeFileList = am.onlyFiles(motifDir)
    for fileName in motifRepTimeFileList:
        with open(fileName) as readFile:
            for i, line in enumerate(readFile):
                normalizer[i] += int(line)

    dataDir = sys.argv[2]
    outDir = sys.argv[3]
    normalizeResults(am.BIN_START, normalizer, dataDir, outDir)
