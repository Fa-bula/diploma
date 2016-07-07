#!/usr/bin/python
""" Find out replication timing of all nucleotides, included in
APOBEC-motif: MOTIFS = ['TCT', 'TCA']"""
import analyseMutations as am
import sys
import os

def get_motif_rep_time(chromosome):
    """ Returns list of replication timings of positions in genome
    with particular motif and given chromosome"""
    motif_rep_time = []

    with open(am.GENOME_FILE_NAMES[chromosome], 'r') as f:
        genome = f.read()
    for motif in am.MOTIFS:
        # First occurence of beginning of motif
        first_occurence = genome.find(motif, 0)
        while first_occurence >= 0:
            # One +1 because str.find finds start of motif, but we want center
            # Second +1 because str begins with 0th element
            replication_timing = am.calculate_replication_timing(chromosome,
                                                           first_occurence + 2)
            if replication_timing == -1:
                print '\nuncalculatable replication time at {0}:{1}'\
                    .format(chromosome, first_occurence + 2)
            motif_rep_time.append(replication_timing)
            first_occurence = genome.find(motif, first_occurence + 1)
    return motif_rep_time


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage {0} {1}".format(sys.argv[0], "out_directory")
        sys.exit()
    for chromosome in am.GENOME_FILE_NAMES:
        motifReplicationTiming = get_motif_rep_time(chromosome)
        numberOfPointsInBin = am.split_to_bins(motifReplicationTiming,
                                          am.BIN_START)
        outFileName = os.path.join(sys.argv[1], chromosome)
        with open(outFileName, 'w') as outFile:
            for pointNumber in numberOfPointsInBin:
                outFile.write(str(pointNumber) + '\n')
