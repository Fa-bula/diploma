#!/usr/bin/python
import analyseMutations as am
import sys
import os

# Find out replication timing of all mutated nucleodtides
# Use enrichment file as list of sample names
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage {0} {1} {2} {3}".format(sys.argv[0],
                                             "mutations.txt",
                                             "enrichment.txt",
                                             "out_Directory"))
        sys.exit()

    replicationTimingSets = am.create_rep_time_sets()
    sampleNames = am.get_sample_names()

    for sampleName in sampleNames:
        mutationReplicationTiming = am.get_mutation_rep_time(sys.argv[1], sampleName,
                                                  replicationTimingSets)

        outFileName = os.path.join(sys.argv[3], sampleName)
        with open(outFileName, 'w') as outFile:
            for repTime in mutationReplicationTiming:
                outFile.write(str(repTime) + '\n')
