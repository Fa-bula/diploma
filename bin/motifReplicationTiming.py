#!/usr/bin/python
import analyseMutations as am
import sys
import os

# Find out replication timing of all nucleotides, included in
# APOBEC-motif: MOTIFS = ['TCT', 'TCA']

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage {0} {1}".format(sys.argv[0], "out_directory"))
        sys.exit()
    replicationTimingSets = am.createRepTimingSets()
    for chromosome in am.GENOME_FILE_NAMES:
        motifReplicationTiming = am.getMotifRepTime(replicationTimingSets,
                                                    chromosome)
        numberOfPointsInBin = am.splitToBins(motifReplicationTiming,
                                          am.BIN_START)
        outFileName = os.path.join(sys.argv[1], chromosome)
        with open(outFileName, 'w') as outFile:
            for pointNumber in numberOfPointsInBin:
                outFile.write(str(pointNumber) + '\n')
