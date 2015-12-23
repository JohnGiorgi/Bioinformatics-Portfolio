from multiprocessing import Pool
from subprocess import call
import os

'''
This script will look for a blast database at /blast_output directory (from directory it is called from) and protein fasta files at /splitter_output/output_splitn where n is a positive integer. Then, will call tblastn in parallel.

Preconditions:

database is named customBLASTdb and saved at /blast_output

protein splits are named output_split (and a number) with extension .fa, saved at /splitter_output
'''

start_dir = os.getcwd()

protein_path = start_dir + '/splitter_ouput'
number_splitter_files = (len([name for name in os.listdir(protein_path) if os.path.isfile(os.path.join(protein_path, name))]))
	
def protein_against_genome(file_number):
	call(['tblastn', '-db', start_dir + '/blast_output/customBLASTdb', '-query', start_dir + '/splitter_ouput/output_split' + str(file_number) + '.fa', '-out', start_dir + '/blast_output/blast_results' + str(file_number)])
	
			
if __name__ == '__main__':
	pool = Pool(processes=4)
	pool.map(protein_against_genome, range(1,number_splitter_files+1))


