#!/usr/bin/python
import sys
import readMutations as rm
# Transform data.txt file with mutations
# using catalog.txt as a file with genom sample names
# remove indel mutations and exsome samples
# Output goes to filtered.txt

if len(sys.argv) != 3:
    print "Usage: {0} data.txt catalog.txt".format(sys.argv[0])
    sys.exit()

with open(sys.argv[2]) as catalogFile:
    genomSampleNames = catalogFile.readline()[:-1].split('\t')
    genomSampleNames.pop(0) # First and second words are "Mutation type"


mutations = rm.mutations(sys.argv[1], givenMutationType = 'subs')
with open("filtered.txt", "w") as outputFile:
    for  mutation in mutations:
        if mutation['sampleName'] in genomSampleNames:
            # outputFile.write('\t'.join([mutation[tagName] for tagName in mutations]))
            # print [mutation[tagName] for tagName in mutations]
            outputFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(mutation['sampleName'],
                                                                               mutation['mutationType'],
                                                                               mutation['chromosome'],
                                                                               mutation['positionFrom'],
                                                                               mutation['positionTo'],
                                                                               mutation['initialNucl'],
                                                                               mutation['finalNucl'],
                                                                               mutation['info']))
    
