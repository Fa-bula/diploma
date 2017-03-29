#!/usr/bin/python
""" Perform all neaded calculations"""
import sys
import os
import pandas
sys.path.append('/home/fa_bula/diploma/bin/')
import core
import mutations
import motif
import split
import frequency
import generate


def create_if_needed(*dirnames):
    """ Check are given directories exist and create them,
    if they not created yet"""
    if len(dirnames) == 0:
        return
    for dir in dirnames:
        if not os.path.exists(dir):
            os.makedirs(dir)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit("Usage {0} mutations enrichment results_dir".format(sys.argv[0]))

    # generate.py part
    signature_pairs = generate.generate_signatures(3)
    
    # Take pairs for this thread only
    signatures = signature_pairs[int(os.environ['SGE_TASK_ID']) - 1] # Cuz SGE_TASK_ID begins with 1
    print "Considering {0} mutation signatures".format(signatures)

    # Creating result subdirecories for curren
    res_dir = os.path.join(sys.argv[3], "{0}+{1}".format(signatures[0], signatures[1]))
    mut_dir = os.path.join(res_dir, 'mutation_rep_time')
    gen_dir = os.path.join(res_dir, 'genome_rep_time')
    freq_dir = os.path.join(res_dir, 'mutations_frequency')
    gen_bins = os.path.join(res_dir, 'genome_rep_time_bins')
    create_if_needed(res_dir, mut_dir, gen_dir, freq_dir)

    # mutations.py part
    sample_names = mutations.get_sample_names(sys.argv[2])
    for sample in sample_names:
        print "Sample {0}\n".format(sample)
        result = mutations.get_mutation_rep_time(sys.argv[1], sample, signatures)
        outFileName = os.path.join(mut_dir, sample)
        with open(outFileName, 'w') as fout:
            for repTime in result:
                fout.write(str(repTime) + '\n')
    
    # motif.py part
    genome_file_names = core.get_genome_file_names()
    for chromosome in genome_file_names:
        motifReplicationTiming = motif.get_motif_rep_time(chromosome, signatures)
        print "Chromosome #{0} motifs has been considered\n".format(chromosome)
        outFileName = os.path.join(gen_dir, chromosome)
        with open(outFileName, 'w') as fout:
            for time in motifReplicationTiming:
                fout.write(str(time) + '\n')
            del motifReplicationTiming
    
    # split.py part
    split.calculate_borders(gen_dir, gen_bins)
    
    # frequency.py part
    motifs_in_bin = pandas.read_csv(gen_bins, sep='\t')
    mutation_rep_time_files = core.get_only_files(mut_dir)
    for mutation_file in mutation_rep_time_files:
        with open(mutation_file) as f:
            replication_timings = map(float, f)
            freq = frequency.calculate_frequency(motifs_in_bin,
                                                 replication_timings)
            outFile = os.path.join(freq_dir, os.path.basename(mutation_file))
            freq.to_csv(outFile, sep='\t')
