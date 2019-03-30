#!/usr/bin/python
""" Find out replication timing of all nucleotides, included in given motifs"""
import sys
import os
sys.path.append('/home/fa_bula/diploma/bin/')
import core

def get_motif_rep_time(chromosome, signatures, replication_timing_file):
    """ Returns list of replication timings of positions in genome
    with particular motifs and given chromosome"""
    motif_rep_time = []
    genome_file_names = core.get_genome_file_names()
    with open(genome_file_names[chromosome], 'r') as f:
        genome = f.read()
    for sig in signatures:
        motif = sig.motif
        # First occurence of beginning of motif
        first_occurence = genome.find(motif, 0)
        while first_occurence >= 0:
            # One +1 because str.find finds start of motif, but we want center
            # Second +1 because str begins with 0th element
            replication_timing = core.calculate_replication_timing(chromosome,
                                                                   first_occurence + 2,
                                                                   replication_timing_file)
            if replication_timing is None:
                print 'uncalculatable replication time at {0}:{1}'\
                    .format(chromosome, first_occurence + 2)
            else:
                motif_rep_time.append(replication_timing)
            first_occurence = genome.find(motif, first_occurence + 1)
    del genome
    return motif_rep_time


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage {0} outDir".format(sys.argv[0]))
    genome_file_names = core.get_genome_file_names()
    for chromosome in genome_file_names:
        motifReplicationTiming = get_motif_rep_time(chromosome)
        print "Chromosome #{0} motifs has been considered\n".format(chromosome)
        outFileName = os.path.join(sys.argv[1], chromosome)
        with open(outFileName, 'w') as fout:
            for time in motifReplicationTiming:
                fout.write(str(time) + '\n')
        del motifReplicationTiming
