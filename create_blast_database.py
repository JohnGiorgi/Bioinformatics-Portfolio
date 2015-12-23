from classLibrary import Blast

'''
Creates new Blast() object. Will create a blast database from the name of the genome sequence file intilized with blastObject
and save it as 'customBLASTdb' at /blast_output
'''

# create new instance of Blast class
blastObject = Blast('genome.fa')
# call the create_blast_database() function on our blastObject 
blastObject.create_blast_database()

