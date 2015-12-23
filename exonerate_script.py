from classLibrary import Exonerate

'''
This script will create a new instance of the Exonerate() object from class library in order to
run the exonerate program in the terminal. Uses a given protein fasta file query against a genome fasta file database
'''

# Creating a new instance of Exonerate with initilization parameters protein and genome
exoObject = Exonerate("protein.fa", "genome.fa")
# Setting the percent stringency to 100, note this will default to 50 if kept unchanged
exoObject.percent = "100"
# Invoke the run_protein2genome method on the exoObject. This will make the exonerate call of --model protein2genome
# to exonerate, with the given protein and genome files. 
exoObject.run_protein2genome()
