#!/usr/bin/python
import sys
import os
import readMutations as rm


def calculateReplicationTiming(replicationTiming, position):
    """ Linear approximation of replication time between two points
    with known replication time. Returns -1 if one of neighbour has no
    known replication time """
    # TODO: implement
    neighbour = (position - position % 1000) + 500
    if neighbour in replicationTiming:
        return replicationTiming[neighbour]
    else:
        return -1


def checkArgs(sysArgv):
    """ Checks given sys.args list of args """
    USAGE_STRING = 'Usage: {0} mutations genomeDir repTiming sampleName'


def getGenomeFileNames(genomeDir):
    """ Returns a dict: genomeFileNames[chrNum] = full/path/to/seq/file """
    genomeFileNames = {}
    for name in os.listdir(genomeDir):
        fullPath = os.path.join(genomeDir, name)
        if os.path.isfile(fullPath):
            genomeFileNames[name[20:]] = fullPath
    return genomeFileNames


def fillRepTimingSets(repTimeFileName, replicationTimingSets):
    """ Fill given dict with data from file """
    with open(repTimeFileName) as readFile:
        lines = readFile.readlines()

    for line in lines:
        splittedLine = line.split(' ')
        chromosome = splittedLine[0]
        position = int(splittedLine[1])
        replicationTiming = float(splittedLine[2])
        replicationTimingSets[chromosome][position] = replicationTiming


# TODO: Rename
MOTIVES = ['TCT', 'TCA']
FINAL_NUCL = ['G', 'T']


def getRepTime(mutationFileName, genomeDir, repTimeFileName, sampleName):
    """ Returns list with replication timings of mutated nucleotides with
    given sample name, mutation motif and final nucleotide """
    
    genomeFileNames = getGenomeFileNames(genomeDir)

    replicationTimingSets = {}
    for chromosome in genomeFileNames:
        replicationTimingSets[chromosome] = {}
    fillRepTimingSets(repTimeFileName, replicationTimingSets)
    allMutations = rm.readMutations(mutationFileName, 'subs')
    apobegMutationReplicationTimings = []

    # We consider chromosomes separately to avoid memory overflow:
    # All genome in str format ~ 3.1 GB - too much for RAM in my PC
    for chromosome in genomeFileNames:
        print('Considering chromosome #{0}'.format(chromosome))
        with open(genomeFileNames[chromosome], 'r') as genomeFile:
            genome = genomeFile.read()

        for mutation in allMutations:
            # FIXME: Considering allMutation 20 times - unefficient
            if mutation['chromosome'] == chromosome:
                position = mutation['positionFrom']
                if genome[position - 1] != mutation['initialNucl']:
                    sys.exit('chromosome {0} position {1} nucl malfolmed')
                motif = genome[position - 2: position + 1]
                if motif in MOTIVES and mutation['finalNucl'] in FINAL_NUCL and mutation['sampleName'] == sampleName:
                    replicationTiming = calculateReplicationTiming(replicationTimingSets[chromosome], position)
                    if replicationTiming == -1:
                        print('uncalculatable replication time at {0}:{1}'.format(chromosome, position))
                    apobegMutationReplicationTimings.append(replicationTiming)
        del genome

    return apobegMutationReplicationTimings


def splitToBins(points, binStart):
    """ Splits points to bins, defined by binStart list
    Returns number of points in each bin """
    numberOfPointsInBin = [0 for start in binStart]
    for point in points:
        for i, start in enumerate(binStart):
            if point < start:
                numberOfPointsInBin[i - 1] += 1
                break
    return numberOfPointsInBin


if __name__ == '__main__':
    replicationTimings = getRepTime()
    with open('out.txt', 'w') as outputFile:
        for time in replicationTimings:
            outputFile.write("{0}\n".format(time))
