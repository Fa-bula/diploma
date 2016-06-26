#!/usr/bin/python
import sys
import os
import readMutations as rm
MOTIFS = ['TCT', 'TCA']         # initial motif
FINAL_NUCL = ['G', 'T']         # final nucleotide

HOME = '/home/bulat/diploma/'
MUTATION_FILE = os.path.join(HOME, 'breast_canser_data/mutations')
GENOME_DIR = os.path.join(HOME, 'genome/seq')
BREAST_DIR = os.path.join(HOME, 'breast_canser_data')
REP_TIME_FILE = os.path.join(BREAST_DIR, 'replicationTiming')
ENRICHMENT_FILE = os.path.join(BREAST_DIR, 'enrichment')
# Borders of bins, where we collect replication times
BIN_START = [10 * i for i in range(9)]

def calculate_replication_timing(replicationTimingSet, position):
    """ Linear approximation of replication time between two points
    with known replication time. Returns -1 if one of neighbour has no
    known replication time
    in: dictionary with replication timings in positions 500, 1500, 2500,..
    and position
    out: linear approximation of replication timing in position"""
    if position % 1000 == 500:
        if position in replicationTimingSet:
            return replicationTimingSet[position]
        else:
            return -1
    floor = (position - position % 1000)
    if position % 1000 > 500:
        leftNeighbour = floor + 500
        rightNeighbour = floor + 1500
    else:
        leftNeighbour = floor - 500
        rightNeighbour = floor + 500
    
    if leftNeighbour in replicationTimingSet and rightNeighbour in replicationTimingSet:
        leftValue = replicationTimingSet[leftNeighbour]
        rightValue = replicationTimingSet[rightNeighbour]
        return leftValue + 1.0 * (rightValue - leftValue) * (position - leftNeighbour) / 1000
    else:
        return -1


def get_genome_file_names(genomeDir):
    """ in: directory with genome sequence files by chromosomes
    out: a dictionary, where genomeFileNames[chrNum] = full/path/to/seq/file """
    genomeFileNames = {}
    for name in os.listdir(genomeDir):
        fullPath = os.path.join(genomeDir, name)
        if os.path.isfile(fullPath):
            genomeFileNames[name[20:]] = fullPath
    return genomeFileNames


GENOME_FILE_NAMES = get_genome_file_names(GENOME_DIR)

def create_rep_time_sets():
    """ out: dict with data from replication timing file with format:
    replicationTimingSets[chromosome][position] = replicationTiming"""
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


def get_mutation_rep_time(mutationFileName, sampleName, replicationTimingSets):
    """ Returns list with replication timings of mutated nucleotides with
    given sample name, mutation motif and final nucleotide """

    allMutations = rm.readMutations(mutationFileName, 'subs', sampleName)
    apobegMutationReplicationTimings = []

    # We consider chromosomes separately to avoid memory overflow:
    # All genome in str format ~ 3.1 GB - too much for RAM in my PC
    for chromosome in GENOME_FILE_NAMES:
        print('Considering chromosome #{0}...'.format(chromosome))
        with open(GENOME_FILE_NAMES[chromosome], 'r') as genomeFile:
            genome = genomeFile.read()

        for mutation in allMutations:
            # FIXME: Considering allMutation 20 times - unefficient
            if mutation['chromosome'] == chromosome:
                position = mutation['positionFrom']
                if genome[position - 1] != mutation['initialNucl']:
                    sys.exit('chromosome {0} position {1} nucl malfolmed')
                motif = genome[position - 2: position + 1]
                if motif in MOTIFS and mutation['finalNucl'] in FINAL_NUCL and mutation['sampleName'] == sampleName:
                    replicationTiming = calculate_replication_timing(replicationTimingSets[chromosome], position)
                    if replicationTiming == -1:
                        print('uncalculatable replication time at {0}:{1}'.format(chromosome, position))
                    apobegMutationReplicationTimings.append(replicationTiming)
        del genome

    return apobegMutationReplicationTimings


def get_motif_rep_time(replicationTimingSets, chromosome):
    """ Returns list of replication timings of positions in genome
    with particular motif and given chromosome """
    motifRepTimings = []
   
    with open(GENOME_FILE_NAMES[chromosome], 'r') as genomeFile:
        genome = genomeFile.read()
    for motif in MOTIFS:
        # First occurence of beginning of motif
        firstOccurrence = genome.find(motif, 0)
        while firstOccurrence >= 0:
            # One +1 because str.find finds start of motif, but we want center
            # Second +1 because str begins with 0th element
            replicationTiming = calculate_replication_timing(replicationTimingSets[chromosome],
                                                           firstOccurrence + 2)
            if replicationTiming == -1:
                print('uncalculatable replication time at {0}:{1}'.format(chromosome, firstOccurrence + 2))
            motifRepTimings.append(replicationTiming)
            firstOccurrence = genome.find(motif, firstOccurrence + 1)
    return motifRepTimings


def get_only_files(directory):
    """ Returns list of full paths of files in directory """
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]


def get_sample_names():
    """ out: list of sample names from enrichment file """
    sampleNames = []
    with open(ENRICHMENT_FILE, 'r') as enrichmentFile:
        for line in enrichmentFile:
            sampleNames.append(line.split('\t')[0])
    return sampleNames


def split_to_bins(points, binStart):
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
