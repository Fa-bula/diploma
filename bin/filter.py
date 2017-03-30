#!/usr/bin/python
""" Removes exsome samples from mutations file"""
import sys
sys.path.append('/home/fa_bula/diploma/bin/')
import core


def filterMutations(mutations_file, catalogFileName, out_file):
    """ in: file with mutations; catalog with list of genome samples
    out: writes all mutations (exclude exome samples) to out_file; returns nothing """
    genomeSampleNames = []      # all samples except exome samples
    with open(catalogFileName) as catalogFile:
        genomeSampleNames = catalogFile.readline()[:-1].split('\t')
        genomeSampleNames.pop(0) # First and second words are "Mutation type"

    mutations = core.read_mutations(infile=mutations_file,
                                    sample_names=genomeSampleNames)
    mutations.to_csv(out_file, sep='\t', header=False, index=False)
    return


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} mutations.txt catalog.txt out.txt".format(sys.argv[0])
        sys.exit()
    filterMutations(sys.argv[1], sys.argv[2], sys.argv[3])
