#!/usr/bin/python
import sys
import os
import readMutations as rm
import matplotlib.pyplot as plt

# Signature of APOBEG mutations
MOTIFS = ['TCT', 'TCA']         # initial motif
FINAL_NUCL = ['G', 'T']         # final nucleotide

HOME = '/home/bulat/diploma/'
MUTATION_FILE = os.path.join(HOME, 'breast_canser_data/mutations')
GENOME_DIR = os.path.join(HOME, 'genome/seq')
BREAST_DIR = os.path.join(HOME, 'breast_canser_data')
REP_TIME_FILE = os.path.join(BREAST_DIR, 'replicationTiming')


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


def getGenomeFileNames(genomeDir):
    """ Returns a dict: genomeFileNames[chrNum] = full/path/to/seq/file """
    genomeFileNames = {}
    for name in os.listdir(genomeDir):
        fullPath = os.path.join(genomeDir, name)
        if os.path.isfile(fullPath):
            genomeFileNames[name[20:]] = fullPath
    return genomeFileNames


GENOME_FILE_NAMES = getGenomeFileNames(GENOME_DIR)


def createRepTimingSets():
    """ Create dict with data from replication timing file """
    replicationTimingSets = {}
    # GENOME_FILE_NAMES[chromosome] = '/path/to/genome/'
    for chromosome in GENOME_FILE_NAMES:
        replicationTimingSets[chromosome] = {}

    with open(REP_TIME_FILE) as readFile:
        lines = readFile.readlines()
        for line in lines:
            splittedLine = line.split(' ')
            chromosome = splittedLine[0]
            position = int(splittedLine[1])
            replicationTiming = float(splittedLine[2])
            replicationTimingSets[chromosome][position] = replicationTiming

    return replicationTimingSets


def getRepTime(mutationFileName, sampleName, replicationTimingSets):
    """ Returns list with replication timings of mutated nucleotides with
    given sample name, mutation motif and final nucleotide """

    allMutations = rm.readMutations(mutationFileName, 'subs', sampleName)
    apobegMutationReplicationTimings = []

    # We consider chromosomes separately to avoid memory overflow:
    # All genome in str format ~ 3.1 GB - too much for RAM in my PC
    for chromosome in genomeFileNames:
        print('Considering chromosome #{0}...'.format(chromosome))
        with open(genomeFileNames[chromosome], 'r') as genomeFile:
            genome = genomeFile.read()

        for mutation in allMutations:
            # FIXME: Considering allMutation 20 times - unefficient
            if mutation['chromosome'] == chromosome:
                position = mutation['positionFrom']
                if genome[position - 1] != mutation['initialNucl']:
                    sys.exit('chromosome {0} position {1} nucl malfolmed')
                motif = genome[position - 2: position + 1]
                if motif in MOTIFS and mutation['finalNucl'] in FINAL_NUCL and mutation['sampleName'] == sampleName:
                    replicationTiming = calculateReplicationTiming(replicationTimingSets[chromosome], position)
                    if replicationTiming == -1:
                        print('uncalculatable replication time at {0}:{1}'.format(chromosome, position))
                    apobegMutationReplicationTimings.append(replicationTiming)
        del genome

    return apobegMutationReplicationTimings


def getMotifRepTime(chromosome, replicationTimingSets):
    """ Retutns list of replication timings of positions in genome
    with particular motif and given chromosome """
    with open(GENOME_FILE_NAMES[chromosome], 'r') as genomeFile:
        genome = genomeFile.read()

    motifRepTimings = []
    for motif in MOTIFS:
        firstOccurrence = 0
        while firstOccurrence >= 0:
            firstOccurrence = genome.find(motif, firstOccurrence + 1)
            # FIXME: maybe there should be  +1 or -1
            replicationTiming = calculateReplicationTiming(replicationTimingSets[chromosome], firstOccurrence + 1)
            motifRepTimings.append(replicationTiming)
    return motifRepTimings


def splitToBins(points, binStart):
    """ Splits points to bins, defined by binStart list:
    (-inf, binStart[0]), [binStart[0], binStart[1]), [binStart[1], inf)
    Returns number of points in each bin """
    numberOfPointsInBin = [0] * (len(binStart) + 1)
    for point in points:
        for i, start in enumerate(binStart):
            if point < start:
                numberOfPointsInBin[i] += 1
                break
        if point >= binStart[-1]:
            numberOfPointsInBin[-1] += 1

    return numberOfPointsInBin


def onlyFiles(directory):
    """ Returns list of full paths of files in directory """
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]


def drawAllPlots(dataDir, outputDir):
    fileNames = onlyFiles(dataDir)
    for fileName in fileNames:
        y = []
        with open(fileName) as readFile:
            for line in readFile:
                y.append(float(line))
        del y[0]
        x = [5 + 10 * i for i in range(9)]
        # # print(fileName)
        # print(x)
        # print(y)
        plt.bar(x, y, width=10)
        plt.show()
        # plt.savefig(os.path.join(outputDir, os.path.basename(fileName)))
    return


if __name__ == '__main__':
    DATA_DIR = os.path.join(BREAST_DIR, 'mutation_replication_time',
                            'test')
    OUTPUT_DIR = os.path.join(DATA_DIR, 'hist')
    drawAllPlots(DATA_DIR, OUTPUT_DIR)

    # replicationTimingSets = createRepTimingSets()
    # OUTPUT_DIR = os.path.join(BREAST_DIR, 'genome_replication_time')
    # motifRepTime = []

    # for chromosome in GENOME_FILE_NAMES:
    #     motifRepTime += getMotifRepTime(chromosome, replicationTimingSets)

    # with open(os.path.join(OUTPUT_DIR, 'genome'), 'w') as outputFile:
    #     for repTime in motifRepTime:
    #         outputFile.write(str(repTime) + '\n')

    # with open(os.path.join(HOME, 'breast_canser_data/enrichment')) as enrichment:
    #     lines = enrichment.readlines()
    # for line in lines:
    #     # SAMPLE_NAME = 'PD3851a'
    #     SAMPLE_NAME = line.split('\t')[0]
    #     print('considering {0} sample...'.format(SAMPLE_NAME))
    #     replicationTimings = getRepTime(MUTATION_FILE_NAME, GENOME_DIR, REP_TIME_FILE_NAME, SAMPLE_NAME)
    #     with open(os.path.join(HOME, 'breast_canser_data/repTime of mutations', SAMPLE_NAME), 'w') as outputFile:
    #         for time in replicationTimings:
    #             outputFile.write("{0}\n".format(time))
