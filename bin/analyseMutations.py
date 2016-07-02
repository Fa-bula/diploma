#!/usr/bin/python
""" This module include basic functions to work with mutations"""
import sys
import os
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


def read_mutations(mutationsFileName, mutationType='', sampleNames=''):
    """ in: file with mutations, maybe specified type of mutation and set of sample names
    out: list of mutations with given mutationType, every item in list is dictionary """

    with open(mutationsFileName) as mutationsFile:
        lines = mutationsFile.readlines()

    allMutations = []
    for line in lines:
        splittedLine = line.split('\t')
        if mutationType != '' and mutationType != splittedLine[1]:
            continue

        if sampleNames != '' and splittedLine[0] not in sampleNames:
            continue
        
        mutation = {}
        mutation['sampleName'] = splittedLine[0]
        mutation['mutationType'] = splittedLine[1]
        mutation['chromosome'] = splittedLine[2]
        mutation['positionFrom'] = int(splittedLine[3])
        mutation['positionTo'] = int(splittedLine[4])
        mutation['initialNucl'] = splittedLine[5]
        mutation['finalNucl'] = splittedLine[6]
        mutation['info'] = splittedLine[7]
        allMutations.append(mutation)

    return allMutations


def calculate_replication_timing(replication_timing_set, position):
    """ Linear approximation of replication time between two points
    with known replication time. Returns -1 if one of neighbour has no
    known replication time
    in: dictionary with replication timings in positions 500, 1500, 2500,..
    and position
    out: linear approximation of replication timing in position"""
    if position % 1000 == 500:
        if position in replication_timing_set:
            return replication_timing_set[position]
        else:
            return -1
    floor = (position - position % 1000)
    if position % 1000 > 500:
        leftNeighbour = floor + 500
        rightNeighbour = floor + 1500
    else:
        leftNeighbour = floor - 500
        rightNeighbour = floor + 500
    
    if leftNeighbour in replication_timing_set and rightNeighbour in replication_timing_set:
        leftValue = replication_timing_set[leftNeighbour]
        rightValue = replication_timing_set[rightNeighbour]
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
    replication_timing_sets[chromosome][position] = replicationTiming"""
    replication_timing_sets = {}
    # GENOME_FILE_NAMES[chromosome] = '/path/to/genome/'
    for chromosome in GENOME_FILE_NAMES:
        replication_timing_sets[chromosome] = {}

    with open(REP_TIME_FILE) as readFile:
        lines = readFile.readlines()
        for line in lines:
            splittedLine = line.split(' ')
            chromosome = splittedLine[0]
            position = int(splittedLine[1])
            replicationTiming = float(splittedLine[2])
            replication_timing_sets[chromosome][position] = replicationTiming

    return replication_timing_sets


def get_mutation_rep_time(mutationFileName, sampleName, replication_timing_sets):
    """ Returns list with replication timings of mutated nucleotides with
    given sample name, mutation motif and final nucleotide """

    allMutations = read_mutations(mutationFileName, 'subs', sampleName)
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
                    replicationTiming = calculate_replication_timing(replication_timing_sets[chromosome], position)
                    if replicationTiming == -1:
                        print('uncalculatable replication time at {0}:{1}'.format(chromosome, position))
                    apobegMutationReplicationTimings.append(replicationTiming)
        del genome

    return apobegMutationReplicationTimings


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

