#!/usr/bin/python
import sys
import os

if len(sys.argv) != 4:
    print "Usage: {0} mutations.txt chromosome_genome chromosome_num".format(sys.argv[0])
    sys.exit()


with open(sys.argv[2], 'r') as genomeFile:
    genomeSequence = genomeFile.read()

chromosomeNumber = sys.argv[3]
                
with open(sys.argv[1]) as mutationFile:
    lines = mutationFile.readlines()
    for line in lines:
        if len(line) > 1:
            splittedLine = line.split('\t')
            mutationNucleotide = splittedLine[5]
            position = int(splittedLine[3])
            chromosome = splittedLine[2]
            if chromosome == chromosomeNumber:
                genomeNucleotide = genomeSequence[position - 1]
                if genomeNucleotide != mutationNucleotide:
                    print position, mutationNucleotide, genomeNucleotide, chromosome
                    sys.exit()

print "Chromosome #{0} check OK".format(chromosomeNumber)
