#!/usr/bin/python
""" Generate file with mutation signature pairs. Signatures in pairs are complementary"""
import itertools
import sys

complementary_dict = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'}

def get_complementary(motif):
    substituted = [complementary_dict[i] for i in motif]
    complementary = list(reversed(substituted))
    return complementary


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage {0} motif_length output_file".format(sys.argv[0]))
    length = int(sys.argv[1])
    
    # Generate (motif, complementary_motif) for all possible motifs
    pairs = [(''.join(i), ''.join(get_complementary(i))) for i in itertools.product("ACGT",
                                                                           repeat = length)]
    # Sort pairs by minimum of two motifs to remove duplicates
    sorted_pairs = sorted(pairs, key = lambda x: min(x[0], x[1]))
    unique_pairs = sorted_pairs[1::2]

    signatures = []
    for nucl in complementary_dict:
        for pair in unique_pairs:
            if pair[0][length / 2] != nucl:
                signatures.append((pair[0], nucl, pair[1], complementary_dict[nucl]))
                
    with open(sys.argv[2], "w") as fout:
        for p in signatures:
            fout.write("{0} {1} {2} {3}\n".format(p[0], p[1], p[2], p[3]))
