# Module for reading files with mutations.


def readMutations(mutationsFileName, givenMutationType='', givenSampleName=''):
    """ in: file with mutations, maybe specified type of mutation and sample name
    out: list of mutations with givenMutationType, every item in list is class """

    with open(mutationsFileName) as mutationsFile:
        lines = mutationsFile.readlines()

    allMutations = []
    for line in lines:
        splittedLine = line.split('\t')
        if givenMutationType != '' and givenMutationType != splittedLine[1]:
            continue

        if givenSampleName != '' and givenSampleName != splittedLine[0]:
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
