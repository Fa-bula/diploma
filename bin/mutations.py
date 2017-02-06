#!/usr/bin/python
""" Find out replication timing of all mutated nucleodtides
Use enrichment file as list of sample names"""
import sys
sys.path.append('/home/fa_bula/diploma/bin/')
import core
import os


def get_sample_names(enrichment_file):
    """ out: list of sample names from enrichment file """
    sample_names = []
    with open(enrichment_file, 'r') as input_file:
        next(input_file)        # Ignoring header
        for line in input_file:
            if line.split('\t')[0] != "\n":
                sample_names.append(line.split('\t')[0])
    return sample_names


def get_mutation_rep_time(mutation_file, sample_name):
    """ Returns list with replication timings of mutated nucleotides
    with given sample name, mutation motif and final nucleotide"""
    sys.stdout.write("\nConsidering {0} sample: ".format(sample_name))
    mutation_rep_time = []
    genome_file_names = core.get_genome_file_names()

    mutations_list = core.read_mutations(mutation_file,
                                         mutation_type='subs',
                                         chromosomes = [ch for ch in genome_file_names],
                                         sample_names=[sample_name],
                                         final_nucleotides=core.FINAL_NUCL,
                                         init_nucleotides=core.INIT_NUCL)
    genome = {}
    for chromosome in genome_file_names:
        with open(genome_file_names[chromosome]) as genome_file:
            genome[chromosome] = genome_file.read()
            
    for index, mutation in mutations_list.iterrows():
        position = mutation['positionFrom']
        chromosome = mutation['chromosome']
        motif = genome[chromosome][position - 2: position + 1]
        if motif in core.MOTIFS:
            rep_time = core.calculate_replication_timing(chromosome,
                                                         position)
            if rep_time == -1:
                print '\nuncalculatable replication time at\
                {0}:{1}'.format(chromosome, position)
            mutation_rep_time.append(rep_time)
            
    del genome
    return mutation_rep_time


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit("Usage {0} mutations enrichment outDir".format(sys.argv[0]))

    sample_names = get_sample_names(sys.argv[2])
    for sample in sample_names:
        result = get_mutation_rep_time(sys.argv[1], sample)
        outFileName = os.path.join(sys.argv[3], sample)
        with open(outFileName, 'w') as outFile:
            for repTime in result:
                outFile.write(str(repTime) + '\n')
