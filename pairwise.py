### imports
# for calling bash commands
from subprocess import call
# for parsing command line arguments
import sys
###

### HELPER FUNCTIONS
def readFile(path):
    '''
    Helper function used to read in contents of a file. Returns as a string stored in memory

    :param path: path to the file to be read into memory
    :return: return a string representing the file. 
    '''
    with open (path, "r") as inputSequence:
        data=inputSequence.read()
    return data

'''
 	This script will take two fasta files containg multiple sequences. It will preform
 	pairwise alignments for each pair of sequences in the two fasta files by making a call to the 
 	needle command line program.

 	if call to script in command line is supplied with argument "-p", then the pairwise alignment
 	will be preformed for two protein sequences. Otherwise, alignment is preformed for two nucleotide
 	sequences

 	Dependencies: Needle command line tool
'''
####################### 
# HELP
#######################

if sys.argv[1] == '-h' or sys.argv[1] == '-help':
	print("Arguments:\n-n\trun the pairwise alignment on two nucleotide sequences\n" + 
		"-p\trun the pairwise alignment on two protein sequences")
	quit()

####################### 
# PUT STRAIN NAMES HERE
#######################
 
secondStrainFileName = "cds_aa/filtered_proteins/Rhiir2_1_GeneCatalog_proteins_20160502_filtered.aa"
firstStrainFileName = "cds_aa/filtered_proteins/RhiirC2_GeneCatalog_proteins_20150810_filtered_LIST2.aa"


#####################################################################################################################################

# Split strains into lists, each element is a gene sequence in fasta format
firstStrain = (readFile(firstStrainFileName + ".fasta")).split(">")
secondStrain = (readFile(secondStrainFileName + ".fasta")).split(">")
# first element in each list is null, remove it
del firstStrain[0] 
del secondStrain[0]

### for displaying current progress
progress = 0
numberOfGenes = len(firstStrain)
###

### initilize variables
pairwiseResults = []
pairwiseMatrix = []
outputFile = "pairwiseResults.txt"
###

### Loop over every sequence in both fasta files
for i in firstStrain:
	
	### create name for tmp fasta file, write gene sequence i to it
	tmpFileNameS1 = (i.split('\n'))[0].split('|')[1] + "_" + (i.split('\n'))[0].split('|')[3] + ".fasta"
	# Opens new file, tmpFileNameS1 and saves gene sequence i to it
	with open(tmpFileNameS1, "w") as f:
		f.write(">" + i.strip())
	###

	for j in secondStrain:
		
		### create name for tmp fasta file, write gene sequence j to it
		tmpFileNameS2 = (j.split('\n'))[0].split('|')[1] + "_" + (j.split('\n'))[0].split('|')[3] + ".fasta"
		with open(tmpFileNameS2, "w") as f:
			f.write(">" + j.strip())
		###

		### create tmp file name for file that stores alignment results
		fileName = tmpFileNameS1 + "_Vs_" + tmpFileNameS2 + ".txt"
		### 
		
		### call needle and then remove the tmp file for sequence j
		# If -p argument supplied with call to script, call needle protein alignment
		if sys.argv[1] == "-n":
			call(["needle", tmpFileNameS1, tmpFileNameS2, "-auto", "-outfile", fileName])
		elif sys.argv[1] == "-p":
			call(["needle", tmpFileNameS1,"-sprotein1", "Y", tmpFileNameS2, "-sprotein2", "Y", "-auto", "-outfile", fileName])
			
		call(["rm", tmpFileNameS2])
		###

		### read in alignment results, and extract the percent identity 
		# If -p argument supplied with call to script, we need to parse the result file differently
		pairwise = readFile(fileName)
		if sys.argv[1] == "-p":
			pairwise = pairwise.split("\n")[25].split(" ")
		elif sys.argv[1] == "-n":
			pairwise = pairwise.split("\n")[22].split(" ")

		pairwise = pairwise[len(pairwise) - 1]
		pairwise = pairwise.replace("%", "")
		pairwise = pairwise.replace(")", "")
		pairwise = pairwise.replace("(", "")
		# append the % for each i to j sequence alignment to a list
		pairwiseResults.append(pairwise)
		# remove tmp pairwise sequence results file
		call(["rm", fileName])
		###

	### Append results for every i to j sequence alignment as a "row" in a "matrix"
	pairwiseMatrix.append(pairwiseResults)
	# clear pairwiseResults	
	pairwiseResults = []
	# rm tmp file for sequence i
	call(["rm",tmpFileNameS1])
	###

	### for displaying current progress
	progress += 1
	print("Progress ... " + str(int(progress/numberOfGenes*100)) + "%")
	###

### Printing results to the console
print("\n" + "#"*100)
# print name of strain on the horizontal and vertical axis of the table
print("\nHorizontal: {} \nVertical: {}\n".format(secondStrainFileName, firstStrainFileName))
print("#"*100 + "\n")
# Each row represnts the sequence alighment results between a sequence i, and all sequences j
for row in pairwiseMatrix:
	print(' '.join(row))
print("")
###