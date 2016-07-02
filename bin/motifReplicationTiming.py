#!/usr/bin/python
""" Find out replication timing of all nucleotides, included in
APOBEC-motif: MOTIFS = ['TCT', 'TCA']"""

import analyseMutations as am
import sys
import os

def get_motif_rep_time(replication_timing_sets, chromosome):
    """ Returns list of replication timings of positions in genome
    with particular motif and given chromosome. Prints <chr>:<pos>,
    where replication timing couldn't be calculated"""
    motifRepTimings = []

    with open(am.GENOME_FILE_NAMES[chromosome], 'r') as genomeFile:
        genome = genomeFile.read()
    for motif in am.MOTIFS:
        # First occurence of beginning of motif
        firstOccurrence = genome.find(motif, 0)
        while firstOccurrence >= 0:
            # One +1 because str.find finds start of motif, but we want center
            # Second +1 because str begins with 0th element
            replicationTiming = am.calculate_replication_timing(replication_timing_sets[chromosome],
                                                           firstOccurrence + 2)
            if replicationTiming == -1:
                print '{0}:{1}'.format(chromosome, firstOccurrence + 2)
            motifRepTimings.append(replicationTiming)
            firstOccurrence = genome.find(motif, firstOccurrence + 1)
    return motifRepTimings


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage {0} {1}".format(sys.argv[0], "out_directory")
        sys.exit()
    replication_timing_sets = am.create_rep_time_sets()
    for chromosome in am.GENOME_FILE_NAMES:
        motifReplicationTiming = get_motif_rep_time(replication_timing_sets,
                                                    chromosome)
        numberOfPointsInBin = am.split_to_bins(motifReplicationTiming,
                                          am.BIN_START)
        outFileName = os.path.join(sys.argv[1], chromosome)
        with open(outFileName, 'w') as outFile:
            for pointNumber in numberOfPointsInBin:
                outFile.write(str(pointNumber) + '\n')
