#!/usr/bin/python
""" This module include basic functions to work with mutations"""
import os
import pandas
HOME = '/home/fa_bula/diploma/'
GENOME_DIR = os.path.join(HOME, 'genome/seq')
# Number of bins to put replication timings
BIN_QUANTITY = 10
IS_REP_TIME_SETS_READY = False
REP_TIME_SET = 0

class Mutation_Signature:
    def __init__(self, pair, type):
        "Make mutation signature from pair (<MOTIF> <FINAL NUCLEOTIDE>)"
        if type == "subs":
            self.motif = pair[0]
            self.initial = pair[0][len(pair[0]) / 2]
            self.final = pair[1]
            self.type = type
        else:
            raise NotImplementedError

    def __str__(self):
        if self.type == "subs":
            return "{0}_{1}".format(self.motif, self.final)            
        else:
            raise NotImplementedError

    def __repr__(self):
        if self.type == "subs":
            return "{0}: {1}->{2}".format(self.motif, self.initial, self.final)
        else:
            raise NotImplementedError

        
def read_mutations(infile, genome='', sample_names='', signature=''):
    # TODO: Implement checking entire motif (init/final check now)
    """ Reads mutations from infile. signatures is a list of Mutation_Signature instances,
    describing possible mutations.
    Returns list of mutations, every item in list is dictionary,
    describing individual mutation"""
    # column_names = ['sampleName', 'mutationType', 'chromosome',
    #                 'positionFrom', 'positionTo', 'initialNucl',
    #                 'finalNucl', 'info']
    mutations = pandas.read_csv(infile, sep="\t", header=0,
                                # names=column_names,
                                index_col=False,
                                dtype={'Tumor_Sample_Barcode': str, 'Chromosome': str,
                                       'Start_position': int, 'Reference_Allele': str,
                                       'Tumor_Seq_Allele2': str, 'APOBEC_mutation': float,
                                       'APOBEC_enrich': float, 'APOBEC_MutLoad_MinEstimate': int,
                                       'Variant_Type': str})
    sample_names_stripped = [s.strip() for s in sample_names]
    if sample_names_stripped:
        mask = mutations.isin(sample_names_stripped)['Tumor_Sample_Barcode']
        mutations = mutations[mask]
    if genome:
        chromosomes = ['chr' + ch for ch in genome]
        mask = mutations.isin(chromosomes)['Chromosome']
        mutations = mutations[mask]

    # Filter mutations, fitting given signature
    if signature:
        # Create mask for choosing mutations, fitting given signature
        # mask = ((mutations['mutationType'] == signature.type) &
        # (mutations['finalNucl'] == signature.final) & (mutations['initialNucl'] == signature.initial))
        mask = ((mutations['Tumor_Seq_Allele2'] == signature.final) & (mutations['Reference_Allele'] == signature.initial))
        # Filter DataFrame, using created mask
        mutations = mutations[mask]
    return mutations


def get_genome_file_names():
    """ in: directory with genome sequence files by chromosomes
    out: a dictionary genome_file_names[chrNum] = full/path/to/seq/file"""
    genome_file_names = {}
    files_list = get_only_files(GENOME_DIR)
    for path in files_list:
        chromosome = os.path.basename(path)[20:]
        genome_file_names[chromosome] = path
    return genome_file_names


def create_rep_time_set(rep_time_file):
    """ returns dict with data from replication timing file
    replication_timing_sets[chromosome] = pandas.DataFrame('position',
    'replication_timing')"""
    data = pandas.read_csv(rep_time_file, sep=' ', dtype={'chromosome': str})
    replication_timing_set = {}
    # GENOME_FILE_NAMES[chromosome] = '/path/to/genome/'
    GENOME_FILE_NAMES = get_genome_file_names()
    for chromosome in GENOME_FILE_NAMES:
        mask = data.chromosome == chromosome
        replication_timing_set[chromosome] = data[mask]
        del replication_timing_set[chromosome]['chromosome']
        replication_timing_set[chromosome].set_index('position',
                                                       inplace=True)
    return replication_timing_set


def calculate_replication_timing(chromosome, position, replication_timing_file):
    """ Linear approximation of replication time between two points
    with known replication time. Returns -1 if one of neighbour has no
    known replication time
    in: chromosome number and position in this chromosome
    out: linear approximation of replication timing"""
    global REP_TIME_SET
    global IS_REP_TIME_SETS_READY
    if not IS_REP_TIME_SETS_READY:
        REP_TIME_SET = create_rep_time_set(replication_timing_file)
        IS_REP_TIME_SETS_READY = True

    rep_time_frame = REP_TIME_SET[chromosome]
    if position in rep_time_frame.index:
        return float(rep_time_frame.ix[position])

    floor = (position - position % 1000)
    if position % 1000 > 500:
        left_neighbour = floor + 500
        right_neighbour = floor + 1500
    else:
        left_neighbour = floor - 500
        right_neighbour = floor + 500

    if left_neighbour not in rep_time_frame.index or \
       right_neighbour not in rep_time_frame.index:
        return None

    left_value = float(rep_time_frame.ix[left_neighbour])
    right_value = float(rep_time_frame.ix[right_neighbour])
    return left_value + 1.0 * (right_value - left_value) * \
        (position - left_neighbour) / 1000


def get_only_files(directory):
    """ Returns list of full paths of files in directory """
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))]


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
 
