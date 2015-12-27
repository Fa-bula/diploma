#!/usr/bin/python

# Transform given .wig file to human-readable format:
# chrNo position replicationTime, where replicationTime specified for [position, position + 1000)
# output goes to fixed.txt

import sys

if len(sys.argv) != 2:
    print 'usage:' + sys.argv[0] + ' foo.wig'
    sys.exit('')

with open(sys.argv[1], 'r') as wigFile:
    lines = wigFile.readlines()

with open('fixed.txt', 'w') as outputFile:
    for line in lines: 
        if line[0] == 'f':
            splittedLine = line.split(' ')
            position = int(splittedLine[2][6:])
            chromosome = splittedLine[1][9:]
        else:
            outputFile.write('{0} {1} {2}\n'.format(chromosome, position, line[:-1]))
            position += 1000
