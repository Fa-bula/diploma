#!/usr/bin/python
import os
import analyseMutations as am

HOME = '/home/bulat/diploma/'
MUTATION_FILE = os.path.join(HOME, 'breast_canser_data/mutations')
GENOME_DIR = os.path.join(HOME, 'genome/seq')
BREAST_DIR = os.path.join(HOME, 'breast_canser_data')
REP_TIME_FILE = os.path.join(BREAST_DIR, 'replicationTiming')


def normalizeResults(resultsDirectory, normalizer, borders):
    """ Split results in bins, defined by borders list.
    Then divide number of points in each bin by normalizer"""
    resultsFileNames = [f for f in os.listdir(resultsDirectory) if os.path.isfile(os.path.join(resultsDirectory, f))]
    OUTPUT_DIR = os.path.join(BREAST_DIR, 'mutation_replication_time', 'normalized')

    for fileName in resultsFileNames:
        results = []
        with open(os.path.join(resultsDirectory, fileName)) as readFile:
            for line in readFile:
                results.append(float(line))

        numberOfPointsInBin = am.splitToBins(results, borders)
        for i, normCoeff in enumerate(normalizer):
            numberOfPointsInBin[i] = numberOfPointsInBin[i] * 1.0 / normCoeff

        with open(os.path.join(OUTPUT_DIR, fileName), 'w') as outputFile:
            for result in numberOfPointsInBin:
                outputFile.write(str(result) + '\n')

    return


if __name__ == '__main__':
    RESULTS_DIRECTORY = os.path.join(BREAST_DIR, 'mutation_replication_time')
    NORMALIZER_FILE = os.path.join(BREAST_DIR, 'totalStatistics')
    normalizer = []
    with open(NORMALIZER_FILE) as readFile:
        for line in readFile:
            normalizer.append(int(line))

    borders = [i * 10 for i in range(9)]
    normalizeResults(RESULTS_DIRECTORY, normalizer, borders)
