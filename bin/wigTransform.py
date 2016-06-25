#!/usr/bin/python
import sys

def wigTransform(wigFileName, outFileName):
    """ Transform given .wig file to human-readable format:
    chrNo_position_replicationTime """
    with open(wigFileName, 'r') as wigFile:
        lines = wigFile.readlines()

        with open(outFileName, 'w') as outputFile:
            for line in lines: 
                if line[0] == 'f':
                    splittedLine = line.split(' ')
                    position = int(splittedLine[2][6:])
                    chromosome = splittedLine[1][9:]
                else:
                    outputFile.write('{0} {1} {2}\n'.format(chromosome, position, line[:-1]))
                    position += 1000

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: {0} {1} {2}'.format(sys.argv[0], 'input.wig', 'output.txt')
        sys.exit('')
    wigTransform(sys.argv[1], sys.argv[2])
