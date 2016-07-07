#!/usr/bin/python
""" Removes indel mutations and exsome samples from mutations file"""
import sys
import analyseMutations as am


def filterMutations(mutations_file, catalogFileName, out_file):
    """ in: file with mutations; catalog with list of genome samples
    out: writes all mutations (exclude indel mutations and exome samples)
    to out file, specified by out_file; returns nothing """
    genomeSampleNames = []      # all samples except exome samples
    with open(catalogFileName) as catalogFile:
        genomeSampleNames = catalogFile.readline()[:-1].split('\t')
        genomeSampleNames.pop(0) # First and second words are "Mutation type"

    mutations = am.read_mutations(mutations_file, mutation_type='subs',
                                  sample_names=genomeSampleNames)
    mutations.to_csv(out_file, sep='\t', header=False, index=False)
    return


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} mutations.txt catalog.txt out.txt".format(sys.argv[0])
        sys.exit()
    filterMutations(sys.argv[1], sys.argv[2], sys.argv[3])
