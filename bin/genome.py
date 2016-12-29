#!/usr/bin/python
"""Transforms all .fa files in given directory to sequence of
nucleotides and writes it to output directory"""
import sys
sys.path.append('/home/fa_bula/diploma/bin/')
import os
import core

def transform_fa(fa_file):
    """ Transforms .fa file to sequence of nucleotides"""
    with open(fa_file) as f:
        genome_sequence = ''
        line = f.readline()     # Missing header
        while line != '':
            line = f.readline()
            genome_sequence += line[:-1]
    return genome_sequence

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: {0} faFilesDir outDir".format(sys.argv[0]))

    fa_files = core.get_only_files(sys.argv[1])
    for file_name in fa_files:
        out_file_name = os.path.join(sys.argv[2],
                                   os.path.basename(file_name)[:-3])
        with open(out_file_name, 'w') as f:
            f.write(transform_fa(file_name))
