from multiprocessing import pool
from subprocess import call
import os

################
# Functions
################

def subdirChecker(subdir_name):
	'''
	Checks if a subdirectory exists. If not, creates it. If so, asks user if they would like to overwrite it and its contents. 
	'''
	if os.path.isdir(subdir_name) == False:
		call(["mkdir", subdir_name])		
	else:
		overwrite = input("The directory {} already exists, would you like to overwrite it and its contents (y/n)?\n".format(subdir_name)).lower().split()
		if overwrite == 'y':
			call(["rm", "-rf", "subdir_name"])
			call(["mkdir", subdir_name])
		elif overwrite == 'n':
			return None
	
###################
# Exonerate Class
####################

class Exonerate():
	percent = "50"
	def __init__(self, protein, genome):
		self.protein = protein
		self.genome = genome
	def run_protein2genome(self):
		call(["exonerate", "--model", "protein2genome", "--percent", self.percent, self.protein, self.genome])

###################
# Blast Class
####################
class Blast():
	'''
	Creates a subdirectory called "blast_output". If one already exits, prompts user for overwrite. Creates a blast database from the genome sequence
	that the Blast object is initilized with.

	Preconditions: genome sequence (input parameter genome) exits in same directory script is called from
	'''
	def __init__(self, genome):
		'''
		(Blast, fasta file) --> None
		'''
		self.genome = genome
	def create_blast_database(self):
		'''
		(Blast) --> None
		'''
		# Captures home directory
		home_directory = os.getcwd()
		# Function checks if subdirectory exits, if not creates one. Otherwise prompts user for overwrite
		subdirChecker("blast_output")
		# Copies the genome fasta file to the new subdirectory
		call(["cp", self.genome, home_directory + "/blast_output"])
		# Moves program into new subdirectory
		os.chdir(home_directory + "/blast_output")
		# Creates a custom BLAST database from genome file.
		call(["formatdb", "-p", "F", "-i", self.genome, "-n", "customBLASTdb"]) # customBLASTdb should be dynamic, name after genome.fasta file
		# Moves back into home directory
		os.chdir(home_directory)

###################
# Splitter Class
####################

class Splitter():
	def __init__(self, sequence, number_splits):
		'''
		(Splitter, fasta file, int) --> None
		'''
		self.sequence = sequence
		self.number_splits = number_splits
	def split_sequence(self):
		'''
		This function will open a fasta file and split it at each '>'. It will save each of these proteins
		in a list called 'data'. Then it will loop through data and save number_splits proteins to new files (in the same directory the script
		is called) the remaining protein splits that don't fit in evenly with the split are saved in the very last file. 

		(Splitter) --> None

		Preconditions: we assume the user feeds in a fasta file (this could be modified though) and there is no option to
		treat the 'left over' proteins, they will simply be saved in the very last file.
		'''
		# Captures the directory the program was called from
		home_directory = os.getcwd()
		subdirChecker("splitter_ouput")
		# Opens the sequence specified by the user 'self.sequence'	
		with open (self.sequence, "r") as input_sequence:
			# Move the progam into our created subdirectory
			os.chdir(os.getcwd() + "/splitter_ouput")
			# Used to name the output files.
			i = 1
			# Splits the sequence file at each instance of '>' and saves it to a list 'data'
			data=input_sequence.read().split('>')
			# Loops through data, saving each item into a file, named sequentially
			for index in range(1,len(data), self.number_splits):
				# Cycles through the number of splits the user requested to append each to a new file
				for number in range(0,self.number_splits):
					# Controls for the situation where we try to move past the length of data
					if index + number > len(data) - 1:
						return None
					# Opens new file, output_spliti (where i is a number)
					output = open("output_split" + str(i) + ".fa", 'a')
					# Saves item at data[index] to a new file. Adds back the ">" at beginning of file.
					output.write(">" + data[index + number])
				# increment to name files that are produced
				i += 1
