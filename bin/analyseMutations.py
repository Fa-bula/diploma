#!/usr/bin/python
""" This module include basic functions to work with mutations"""
import os
import pandas
MOTIFS = ['TCT', 'TCA']         # initial motif
FINAL_NUCL = ['G', 'T']         # final nucleotide

HOME = '/home/bulat/diploma/'
MUTATION_FILE = os.path.join(HOME, 'breast_canser_data/mutations')
GENOME_DIR = os.path.join(HOME, 'genome/seq')
BREAST_DIR = os.path.join(HOME, 'breast_canser_data')
REP_TIME_FILE = os.path.join(BREAST_DIR, 'replicationTiming')
ENRICHMENT_FILE = os.path.join(BREAST_DIR, 'enrichment')
# Borders of bins, where we collect replication times
BIN_START = [10 * i for i in range(9)]


def read_mutations(mutations_file, mutation_type='', chromosome='',\
                   sample_names='', final_nucleotides=''):
    """ Reads mutation from mutations_file with given mutation_type,
    final nucleotide in final_nucl and sample in sample_names.
    Returns list of mutations, every item in list is dictionary,
    describing individual mutation"""
    column_names = ['sampleName', 'mutationType', 'chromosome',
                    'positionFrom', 'positionTo', 'initialNucl',
                    'finalNucl', 'info']
    mutations = pandas.read_csv(mutations_file, sep="\t", header=None,
                           names=column_names, index_col=False)
    if mutation_type:
        mask = mutations['mutationType'] == mutation_type
        mutations = mutations[mask]
    if chromosome:
        mask = mutations['chromosome'] == chromosome
        mutations = mutations[mask]
    if sample_names:
        mask = mutations.isin(sample_names)['sampleName']
        mutations = mutations[mask]
    if final_nucleotides:
        mask = mutations.isin(final_nucleotides)['finalNucl']
        mutations = mutations[mask]
    return mutations



def get_genome_file_names(genome_dir):
    """ in: directory with genome sequence files by chromosomes
    out: a dictionary genome_file_names[chrNum] = full/path/to/seq/file"""
    genome_file_names = {}
    for name in os.listdir(genome_dir):
        full_path = os.path.join(genome_dir, name)
        if os.path.isfile(full_path):
            genome_file_names[name[20:]] = full_path
    return genome_file_names


GENOME_FILE_NAMES = get_genome_file_names(GENOME_DIR)

def create_rep_time_set():
    """ returns dict with data from replication timing file
    replication_timing_sets[chromosome] = pandas.DataFrame('position',
    'replication_timing')"""
    data = pandas.read_csv(REP_TIME_FILE, sep=' ', dtype={'chromosome': str})
    replication_timing_set = {}
    # GENOME_FILE_NAMES[chromosome] = '/path/to/genome/'
    for chromosome in GENOME_FILE_NAMES:
        mask = data.chromosome == chromosome
        replication_timing_set[chromosome] = data[mask]
        del replication_timing_set[chromosome]['chromosome']
        replication_timing_set[chromosome].set_index('position',
                                                       inplace=True)
    return replication_timing_set

REP_TIME_SET = create_rep_time_set()


def calculate_replication_timing(chromosome, position):
    """ Linear approximation of replication time between two points
    with known replication time. Returns -1 if one of neighbour has no
    known replication time
    in: chromosome number and position in this chromosome
    out: linear approximation of replication timing"""
    rep_time_frame = REP_TIME_SET[chromosome]
    if position in rep_time_frame.index:
        return rep_time_frame.ix[position]

    floor = (position - position % 1000)
    if position % 1000 > 500:
        left_neighbour = floor + 500
        right_neighbour = floor + 1500
    else:
        left_neighbour = floor - 500
        right_neighbour = floor + 500

    if left_neighbour not in rep_time_frame.index or \
       right_neighbour not in rep_time_frame.index:
        return -1

    left_value = rep_time_frame[left_neighbour]
    right_value = rep_time_frame[right_neighbour]
    return left_value + 1.0 * (right_value - left_value) * \
        (position - left_neighbour) / 1000


def get_only_files(directory):
    """ Returns list of full paths of files in directory """
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]


def get_sample_names():
    """ out: list of sample names from enrichment file """
    sample_names = []
    with open(ENRICHMENT_FILE, 'r') as input_file:
        next(input_file)        # Ignoring header
        for line in input_file:
            if line.split('\t')[0] != "\n":
                sample_names.append(line.split('\t')[0])
    return sample_names


def split_to_bins(points, bin_start):
    """ Splits points to bins, defined by bin_start list:
    (-inf, bin_start[0]), [bin_start[0], bin_start[1]), [bin_start[1], inf)
    Returns number of points in each bin """
    number_of_points_in_bin = [0] * (len(bin_start) + 1)
    for point in points:
        for i, start in enumerate(bin_start):
            if point < start:
                number_of_points_in_bin[i] += 1
                break
        if point >= bin_start[-1]:
            number_of_points_in_bin[-1] += 1

    return number_of_points_in_bin
