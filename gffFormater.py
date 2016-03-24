__author__ = 'johngiorgi'

import collections

############## Classes ##############
class Gene:

    def __init__(self, name, listOfExons, listOfCDS, derivedLine):
        self.name = name
        self.listOfExons = listOfExons
        self.listOfCDS = listOfCDS
        self.derivedLine = derivedLine


    def get_listOfExons(self):
        return self.listOfExons
    def get_listOfCDS(self):
        return self.listOfCDS
    def get_derivedLine(self):
        return self.derivedLine
############## Classes ##############


def formatGFF(input,output):
    '''
    This function will loop through every line of a GFF file, creating a new gene object in memory which will
    group all associated exons and CDS. This is determined by the exon and CDS objects "name" attribute. Finally,
    the function will deconstruct the information from the memory structure to create a new, properly formatted
    GFF file, where the hierarchy Gene > mRNA > exon > CDS is observed for every gene.

    Note: This function requires that the GFF follows the GFF3 sequence ontology formatting. What it will fix
    is issues with the hierarchical structure, i.e. not following a Gene > all of this genes mRNA > all of this
    genes Exons > all of this genes CDS layout. 

    :param input: directory path to the GFF file to be formatted
    :param output: directory path to the location to save a NEW formatted GFF
    '''

    # A ordered dictionary to store our genes
    geneDictionary = collections.OrderedDict()
    # A list of names
    geneNames = []


    # Store every line of the input GFF in an array, data
    with open(input, "r") as inputFile:
        data = inputFile.readlines()

    # Our loop condition. We want all lines in data that do not have ##gff-version in them
    loopCondition = (line for line in data if "##gff-version" not in line)

    '''(1) MEMORY: this loop will create our gene objects in memory, creating a hierarchical pattern (gene>exon>CDS)'''

    for line in loopCondition:

        # Get the name of the gene
        geneName = (((line.split("\t"))[8]).split(";"))[1]

        # If we have not already created a gene object of name "geneName" then
        # append a new Gene object to listOfGenes with name geneName.
        if geneName not in geneNames:

            # Create our "tempGene" to store the gene we are working with,
            # and append it to our gene dictionary
            tempGene = Gene(geneName, [], [], line)
            geneDictionary[geneName] = tempGene
            # Store the name of this gene
            geneNames.append(geneName)

        # Otherwise, if we have seen this name before, make our tempGene
        # equal to our already created gene object by accessing it from the
        # dictionary
        else:
            tempGene = geneDictionary[geneName]

        # Determine if the line represents an exon or CDS
        exonOrCDS = (line.split("\t"))[2]

        if exonOrCDS == "exon":
            # Append the line to the listOfExons in the gene object
            (tempGene.get_listOfExons()).append(line)
        elif exonOrCDS == "CDS":
            # Append the line to the listOfCDS in the gene object
            (tempGene.get_listOfCDS()).append(line)

    '''(2) FILE: this loop will deconstruct our gene objects in memory, producing a properly formatted GFF file'''

    with open(output, "w") as outputFile:
        for name in geneNames:

            # Our current gene will be accessed from the ordered dictionary by its name
            currentGene = geneDictionary[name]

            # Then we will get the line the gene was derived from, and change
            # it's "type" to gene
            currentGenesLine = currentGene.get_derivedLine()
            currentGenesLine = currentGenesLine.split("\t")
            currentGenesLine[2] = "gene"

            # Determine the start and stop positions of the gene based on the first exon
            # This is used as a starting point
            start = (((currentGene.get_listOfExons())[0]).split('\t'))[3]
            stop = (((currentGene.get_listOfExons())[0]).split('\t'))[4]

            # The loop will move through all exons of our gene, finding the smallest "start" and largest "stop"
            # thus finding the start and stop positions at the level of the gene.
            for item in currentGene.get_listOfExons():
                tempStart = (item.split("\t"))[3]
                tempStop = (item.split("\t"))[4]
                if tempStart < start:
                    start = tempStart
                if tempStop > stop:
                    stop = tempStop

            # Assign the gene its start and stop positions.
            currentGenesLine[3] = start
            currentGenesLine[4] = stop

            # Join our array, this will represent the "gene" line to write to the GFF3 file.
            currentGenesLine = "\t".join(currentGenesLine)

            # Finally, write out gene line to the GFF.
            outputFile.write(currentGenesLine)


            # These two foor loops will write all exons, and then all CDS of our gene to the GFF3 file.
            for item in currentGene.get_listOfExons():
                outputFile.write(item)
            for item in currentGene.get_listOfCDS():
                outputFile.write(item)



formatGFF("inccorectlyFormated_FORMATFIXED.gff", "inccorectlyFormated_FORMATFIXED_HIERARCHYFIXED.gff")


