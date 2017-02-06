#!/usr/bin/python
""" Calculates frequency of APOBEC-mutation in bin[i]
frequency = {#mutations in bin[i]} / {#APOBEC-motifs in bin[i]}"""
from __future__ import division # This way {int} / {int} = {float}
import os
import sys

sys.path.append('/home/fa_bula/diploma/bin/')
import core
# from operator import add
import numpy as np
import pandas


def calculate_frequency(attempts_in_bin, event_positions):
    """ Calculates frequency of events in bin[i]
    IN: bin_borders - list of bin's borders,
    attempts_in_bin - list of number of attempts to occur event in bin[i]
    event_positions - points, where event occur"""
    bin_borders = [attempts_in_bin['bin_start'][0]]
    bin_borders += list(attempts_in_bin['bin_end'])
    attempts_in_bin['mutations'] = pandas.Series(np.histogram(event_positions,
                                                           bins=bin_borders)[0],
                                              index=attempts_in_bin.index)
    frequency = 1. * attempts_in_bin['mutations'] / attempts_in_bin['motifs']
    attempts_in_bin['frequency'] = pandas.Series(frequency,
                                                 index=attempts_in_bin.index)
    return attempts_in_bin


def estimate_conditional_probability(bin_borders, event_positions):
    """ P{event occurred in bin[i] | event occurred}
    dataDir - directory with data, should be splitted and normalized """
    events_in_bin = core.split_to_bins(event_positions, bin_borders)
    conditional_probability = [0] * len(events_in_bin)
    number_of_events = sum(events_in_bin)
    for i in range(len(events_in_bin)):
        conditional_probability[i] = events_in_bin[i] / number_of_events
    return conditional_probability


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit("Usage: {0} motifRepTimeBins mutationRepTimeDir "
                 "outDir".format(sys.argv[0]))
    OUT_DIR = sys.argv[3]
    motifs_in_bin = pandas.read_csv(sys.argv[1], sep='\t')

    mutation_rep_time_files = core.get_only_files(sys.argv[2])
    for mutation_file in mutation_rep_time_files:
        with open(mutation_file) as f:
            replication_timings = map(float, f)
        frequency = calculate_frequency(motifs_in_bin, replication_timings)
        outFile = os.path.join(OUT_DIR, os.path.basename(mutation_file))
        frequency.to_csv(outFile, sep='\t')
