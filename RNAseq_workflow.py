# TODO(John): Correct styling according to Google's Style Guide
# TODO(John): Make this script importable (add a main method)

############################# IMPORTS ###################################
from subprocess import call # for executing commands in terminal
import os # for changing directory, etc
import time # for printing current time to console
#######################################################################
Y = True
N = False
#################### CHANGE VARIABLES HERE ############################
# first SRA accension number of the study
first_SRA = 3202807
# number of samples in the study
num_samples = 5
# study directory
study = "study_1"
# parent directory
parent_directory = "/Volumes/Storage/RNASeq_data/fusarium_graminearum/"
# reference genome directory
reference_genome = "/Volumes/Storage/RNASeq_data/reference_genomes/Fusarim_Graminearum_index/"

# set of booleans to chose which part of workflow is ran
downloadSRA = Y
trimSRA = Y
mapSRA = N
#######################################################################

# context manager for changing directory
class cd:
	"""
	Context manager for safely changing the current working directory
	"""
	def __init__(self, newPath):
		self.newPath = os.path.expanduser(newPath)

	def __enter__(self):
		self.savedPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.savedPath)
###

for SRA in range(first_SRA, first_SRA + num_samples):
	# Create string variable SRA, points to SRA accension number
	SRA = "SRR" + str(SRA)
	# 1) download SRA file
	if downloadSRA:
		with cd(parent_directory+study+"/fastq/"):
			# print conformation that moved occured sucsesfully
			print(time.strftime("[%a, %I:%M]"), "Moving to: ", os.getcwd())
			print(time.strftime("[%a, %I:%M]"), "Downloading SRA file: " + SRA + " to current directory")
			# call fast-q dump using the SRA accension
			call(["fastq-dump", SRA, "-gzip"])
			# print DONE message along with current time
			print(time.strftime("[%a, %I:%M]"), "DONE. " + SRA + ".fastq.gz saved to: ", os.getcwd())

	# 2) trim file
	if trimSRA:
		with cd(parent_directory+study+"/trimmed_fastq/"):
			# print conformation that moved occured sucsesfully
			print(time.strftime("[%a, %I:%M]"), "Moving to: ", os.getcwd())
			print(time.strftime("[%a, %I:%M]"), "Trimming " + SRA + ".fastq.gz ...")
			# call tim_galore  using the SRA accension
			call(["trim_galore", "../fastq/" + SRA + ".fastq.gz"])

			print(time.strftime("[%a, %I:%M]"), "DONE.", SRA + ".fastq.gz", "trimmed")

	# 3) map back to reference genome
	if mapSRA:
		with cd("/Users/johngiorgi/Documents/Google Drive/honours/workflows/RNASeq/"):
			# print conformation that moved occured sucsesfully
			print(time.strftime("[%a, %I:%M]"), "Moving to: ", os.getcwd())
			print(time.strftime("[%a, %I:%M]"), "Begin mapping " + SRA + 
				"_trimmed.fq.gz to reference genome...") 
			# map trimmed fast-q back to reference genome
			# IF there is a buffer size error, add: 
			# "--limitOutSJcollapsed", "5000000", to this call
			call(["STAR", "--quantMode", "GeneCounts", "--runThreadN", "2", "--genomeDir", 
				reference_genome, "--readFilesIn", parent_directory + study + "/trimmed_fastq/" + 
				SRA + "_trimmed.fq.gz", "--readFilesCommand", "gunzip", "-c", "--runMode", "alignReads", 
				"--limitOutSJcollapsed", "5500000"])
			# rename and move file to correct directory
			call(["mv", "ReadsPerGene.out.tab", "ReadsPerGene_" + SRA + "_trimmed.out.tab"])
			print(time.strftime("[%a, %I:%M]"), 
				"Renamed output file 'ReadsPerGene.out.tab' to 'ReadsPerGene_" + 
				 SRA + "_trimmed.out.tab'")
			call(["mv", "ReadsPerGene_" + SRA + "_trimmed.out.tab", "/Volumes/Storage/RNASeq_data/" + study + "/RNA_raw_counts/"])
			print(time.strftime("[%a, %I:%M]"), "Moved 'ReadsPerGene_" + SRA + 
				"_trimmed.out.tab' to /Volumes/Storage/RNASeq_data/" + study + "/RNA_raw_counts")
		# empty this directory (just to be sure)
		call(["rm", "-r", "/Users/johngiorgi/Documents/Google Drive/honours/workflows/RNASeq/"])	
		call(["mkdir", "/Users/johngiorgi/Documents/Google Drive/honours/workflows/RNASeq/"])

# empty ncbi > public > sra directory
call(["rm", "-r", "/Users/johngiorgi/ncbi/public/sra"])	
