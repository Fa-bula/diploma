#!/usr/bin/python
""" Splits replication timings of APOBEC-motif in bins with equal number
of points in each bin"""
import numpy as np
from scipy import stats
import sys
sys.path.append('/home/fa_bula/diploma/bin/')
import core

def calculate_borders(motifRepTimeDir, outFileName):
    replication_timings = np.array([])
    file_names = core.get_only_files(motifRepTimeDir)
    for name in file_names:
        with open(name) as fin:
            l = np.array(map(float, fin))
            l = l[l != -1]
            replication_timings = np.concatenate((replication_timings,
                                                  l), axis=1)

    borders = np.linspace(0, 1, num=core.BIN_QUANTITY + 1, endpoint=True)
    bin_borders = stats.mstats.mquantiles(replication_timings, borders)
    with open(outFileName, 'w') as fout:
        fout.write('bin_start\tbin_end\tmotifs\n')
        for i in range(len(bin_borders) - 1):
            print "Bin #{0}".format(i)
            point_number = sum(map(lambda x: bin_borders[i] < x and
                                   x < bin_borders[i + 1],
                                   replication_timings))
            fout.write("{0}\t{1}\t{2}\n".format(bin_borders[i],
                                                bin_borders[i + 1],
                                                point_number))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: {0} motifRepTimeDir outFile".format(sys.argv[0]))
    calculate_borders(sys.argv[1], sys.argv[2])
