#!/usr/bin/python
import sys

# Transforms .fa file to sequence of nucleotides
if len(sys.argv) != 2:
    print "Usage: {0} chromosome.fa".format(sys.argv[0])
    sys.exit()

genomeSequence = ''
with open(sys.argv[1], 'r') as genomeFile:
        line = genomeFile.readline() # Miss header
        while line != '':
            line = genomeFile.readline()
            genomeSequence += line[:-1]

with open(sys.argv[1][:-3], 'w') as outFile:
    outFile.write(genomeSequence)
