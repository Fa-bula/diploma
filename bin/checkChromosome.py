#!/usr/bin/python
""" Checks is nucleotides in mutation file placed according to genome
Genome sequence files should be named like "hs_ref_GRCh37.p5_chr1" """
import sys
import os
import analyseMutations as am

def check_chromosome(genome_file, mutations_file, chromosome):
    """Checks is (initialNucleotide, position) in mutations_file
    placed according to genome_file"""
    with open(genome_file, 'r') as f:
        genome_sequence = f.read()

    mutations_list = am.read_mutations(mutations_file,
                                       mutation_type='subs',
                                       chromosome=chromosome)
    for index, mutation in mutations_list.iterrows():
        position = mutation['positionFrom']
        genome_nucleotide = genome_sequence[position - 1]
        mutation_nucleotide = mutation['initialNucl']
        if  genome_nucleotide != mutation_nucleotide:
            message = '\n{0}:{1} nucleotide in genome ({2}) and\
            mutations file ({3}) not equal'
            sys.exit(message.format(chromosome, position,
                                    genome_nucleotide,
                                    mutation_nucleotide))
    print "Chromosome {0} check succeed".format(chromosome)
    return


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: {0} mutations genomeDir".format(sys.argv[0]))
    genome_files = am.get_only_files(sys.argv[2])
    for file_name in genome_files:
        chromosome = os.path.basename(file_name)[20:]
        check_chromosome(file_name, sys.argv[1], chromosome)
