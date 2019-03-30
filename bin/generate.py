#!/usr/bin/python
""" Generate file with mutation signature pairs. Signatures in pairs are complementary"""
import itertools
import sys
sys.path.append('/home/fa_bula/diploma/bin/')
import core

complementary_dict = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'}

def get_complementary(motif):
    """ Returns complementary motif"""
    # Replace nucleotedes with complementary
    substituted = [complementary_dict[i] for i in motif]
    # Reverse nucleotide sequence
    complementary = list(reversed(substituted))
    return complementary


def generate_signatures(motif_length):
    """ Creates list of all distinct complementary mutation signatures"""
    # Generate (motif, complementary_motif) for all possible motifs
    pairs = [(''.join(i), ''.join(get_complementary(i))) for i in itertools.product("ACGT",
                                                                                    repeat = motif_length)]
    # Sort pairs by minimum of two motifs to remove duplicates
    sorted_pairs = sorted(pairs, key = lambda x: min(x[0], x[1]))
    unique_pairs = sorted_pairs[1::2]

    signatures = []
    for nucl in complementary_dict:
        for pair in unique_pairs:
            if pair[0][motif_length / 2] != nucl:
                first = core.Mutation_Signature((pair[0], nucl), 'subs')
                second = core.Mutation_Signature((pair[1], complementary_dict[nucl]), 'subs')
                signatures.append((first, second))
    # signatures = [p for p in signatures if p[0].motif == "TCA" or p[0].motif == "TCT" or p[1].motif == "TCT" or p[1].motif == "TCA"]
    return signatures
                
    
if __name__ == '__main__':
    # Use if you want to check, what signatures created
    if len(sys.argv) != 3:
        sys.exit("Usage {0} motif_length output_file".format(sys.argv[0]))
    length = int(sys.argv[1])
    
    signatures = generate_signatures(length)
    with open(sys.argv[2], "w") as fout:
        for p in signatures:
            fout.write("{0} {1}\n".format(p[0], p[1]))
