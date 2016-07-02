#!/usr/bin/python
""" Calculates frequency of APOBEC-mutation in bin[i]
frequency = {#mutations in bin[i]} / {#APOBEC-motifs in bin[i]}"""
from __future__ import division # This way {int} / {int} = {float}
import os
import sys
import analyseMutations as am
from operator import add



def calculate_frequency(bin_borders, attempts_in_bin, event_positions):
    """ Calculates frequency of events in bin[i]
    IN: bin_borders - list of bin's borders,
    attempts_in_bin - list of number of attempts to occur event in bin[i]
    event_positions - points, where event occur"""
    if len(attempts_in_bin) != len(bin_borders) + 1:
        sys.exit("Length of attempts_in_bin ({0}) should be equal to\
        number of bins({1})".format(len(attempts_in_bin), len(bin_borders) + 1))

    events_in_bin = am.split_to_bins(event_positions, bin_borders)
    frequency = [0] * len(events_in_bin)
    for i in range(len(events_in_bin)):
        frequency[i] = events_in_bin[i] / attempts_in_bin[i]
    return frequency


def estimate_conditional_probability(bin_borders, event_positions):
    """ P{event occurred in bin[i] | event occurred}
    dataDir - directory with data, should be splitted and normalized """
    events_in_bin = am.split_to_bins(event_positions, bin_borders)
    conditional_probability = [0] * len(events_in_bin)
    number_of_events = sum(events_in_bin)
    for i in range(len(events_in_bin)):
        conditional_probability[i] = 1.0 * events_in_bin[i] / number_of_events

    return conditional_probability


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit("Usage: {0} motifRepTimeDir mutationRepTimeDir\
        outDir".format(sys.argv[0]))
    OUT_DIR = sys.argv[3]
    motif_rep_time_files = am.get_only_files(sys.argv[1])
    motifs_in_bin = [0] * (len(am.BIN_START) + 1)
    for motif_file in motif_rep_time_files:
        with open(motif_file) as f:
            motifs_in_bin = map(add, motifs_in_bin, map(int, f))

    mutation_rep_time_files = am.get_only_files(sys.argv[2])
    for mutation_file in mutation_rep_time_files:
        with open(mutation_file) as f:
            replication_timings = map(float, f)
        frequency = calculate_frequency(am.BIN_START, motifs_in_bin,
                                        replication_timings)
        outFile = os.path.join(OUT_DIR, os.path.basename(mutation_file))
        with open(outFile, 'w') as f:
            f.write("replicationTiming\tfrequency\n")
            for i in range(1, len(frequency) - 1):
                x = (am.BIN_START[i - 1] + am.BIN_START[i]) / 2
                f.write("{0}\t{1}\n".format(x, frequency[i]))

