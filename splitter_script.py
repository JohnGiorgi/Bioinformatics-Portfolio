from classLibrary import Splitter

''' 
Creating a new instance of Splitter() with initilization parameter number_splits

This will split the sequences in protein.fasta in n number of sequences per file, saved into new files

'''
# create new instance of Splitter class
splitterObject = Splitter("protein.fa", 4)
# call the split_sequence() function on our splitterObject 
splitterObject.split_sequence()

