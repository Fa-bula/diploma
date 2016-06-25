# Module for reading files with mutations.


def readMutations(mutationsFileName, mutationType='', sampleNames=''):
    """ in: file with mutations, maybe specified type of mutation and set of sample names
    out: list of mutations with given mutationType, every item in list is dictionary """

    with open(mutationsFileName) as mutationsFile:
        lines = mutationsFile.readlines()

    allMutations = []
    for line in lines:
        splittedLine = line.split('\t')
        if mutationType != '' and mutationType != splittedLine[1]:
            continue

        if sampleNames != '' and splittedLine[0] not in sampleNames:
            continue
        
        mutation = {}
        mutation['sampleName'] = splittedLine[0]
        mutation['mutationType'] = splittedLine[1]
        mutation['chromosome'] = splittedLine[2]
        mutation['positionFrom'] = int(splittedLine[3])
        mutation['positionTo'] = int(splittedLine[4])
        mutation['initialNucl'] = splittedLine[5]
        mutation['finalNucl'] = splittedLine[6]
        mutation['info'] = splittedLine[7]
        allMutations.append(mutation)

    return allMutations
