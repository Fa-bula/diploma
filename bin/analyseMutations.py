#!/usr/bin/python
import sys
import os
import readMutations as rm

def calculateReplicationTiming(replicationTiming, position):
    neighbour = (position - position % 1000) + 500
    if neighbour in replicationTiming:
        return replicationTiming[neighbour]
    else:
        return -1

if (len(sys.argv) != 4):
    print 'Usage: {0} mutations.txt genome_dir replicationTiming.txt'.format(sys.argv[0])
    sys.exit()

genomeDir = sys.argv[2]
if not os.path.isdir(genomeDir):
    sys.exit('second argument must be directory')

fileNames = {}
for name in os.listdir(genomeDir):
    fullPath = os.path.join(genomeDir, name)
    if os.path.isfile(fullPath):
        fileNames[name[20:]] = fullPath

replicationTimingSets = {}
for chromosome in fileNames:
    replicationTimingSets[chromosome] = {}

with open(sys.argv[3]) as replicationTimingFile:
    lines = replicationTimingFile.readlines()
    for line in lines:
        splittedLine = line.split(' ')
        chromosome = splittedLine[0]
        position = int(splittedLine[1])
        replicationTiming = float(splittedLine[2])
        replicationTimingSets[chromosome][position] = replicationTiming
      

Allmutations = rm.mutations(sys.argv[1])

# list of replication timings of mutations with apobeg motive
apobegMutationReplicationTimings = {}

# list of replication timings of apobeg motive occurences in genome
apobegMotiveReplicationTimings = []

# We consider chromosomes separately to avoid memory overflow:
# All genome in str format ~ 3.1 GB - too much for RAM in my PC
for chromosome in fileNames:
    with open(fileNames[chromosome], 'r') as genomeFile:
        genome = genomeFile.read()
    
    firstOccurence = -1
    while max(genome.find('TCT', firstOccurence + 1), genome.find('TCA', firstOccurence + 1)) >= 0:
        firstOccurence = min(genome.find('TCT', startOfFinding), genome.find('TCA', startOfFinding))
        apobegMotiveReplicationTimings.append(calculateReplicationTiming(replicationTimingSets[chromosome], firstOccurence + 1))        
        
    for mutation in Allmutations:
        if mutation['chromosome'] == chromosome:
            position = mutation['positionFrom']
            motive = genome[position - 2: position + 1]
            if genome[position - 1] != mutation['initialNucl']:
                print 'Warning: {0}:{1}'.format(chromosome, position)

            if (motive == 'TCA' or motive == 'TCT') and (mutation['finalNucl'] =='G' or mutation['finalNucl'] == 'T'):
                replicationTiming = calculateReplicationTiming(replicationTimingSets[chromosome], position)
                if replicationTiming == -1:
                    continue
                apobegMutationReplicationTimings.append(replicationTiming)
    del genome

# We have apobegMutationReplicationTimings and apobegMotiveReplicationTimings lists at this point
# Now we should divide all replication timings to NumberOfBins different bins

NumberOfBins = 10
apobegMutationReplicationTimings.sort()
apobegMotiveReplicationTimings.sort()
numberOfMutations = len(apobegMutationReplicationTimings)
endOfBin = [apobegMutationReplicationTimings[0.1 * i * numberOfMutations] for i in xrange(1, 11)]

numberOfMotivesInBin = [0 for i in range(10)]


    


