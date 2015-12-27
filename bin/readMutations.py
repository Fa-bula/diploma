# Module for reading files with mutations.

def mutations(mutationsFileName, givenChromosome = '', givenMutationType = '', givenSampleName = ''):
    """
    input: file with mutations, maybe specified chromosome or type or sampleName
    output: list with mutations with specified parameters, every item in list is class
    """
    with open(mutationsFileName) as mutationsFile:
        lines = mutationsFile.readlines()
    
    allMutations = []
    for line in lines:
        splittedLine = line.split('\t')
        mutation = {}
        sampleName, mutationType, chromosome, positionFrom, positionTo, initialNucl, finalNucl, info = line.split('\t')
        if givenChromosome != '' and givenChromosome != chromosome:
            continue

        if givenSampleName != '' and givenSampleName != sampleName:
            continue

        if givenMutationType != '' and givenMutationType != mutationType:
            continue
            
        mutation['sampleName'] = sampleName
        mutation['mutationType'] = mutationType
        mutation['chromosome'] = chromosome
        mutation['positionFrom'] = int(positionFrom)
        mutation['positionTo'] = int(positionTo)
        mutation['initialNucl'] = initialNucl
        mutation['finalNucl'] = finalNucl
        mutation['info'] = info
        allMutations.append(mutation)

    return allMutations    
