import os
import sys
import subprocess

########## VARIABLES ##########
dataDirectory = sys.argv[1]
##############################

########### INSTRUCTIONS ###########
# call script example:
# python3 findDups.py <path to data>
##############################

def readFile(path):
    '''
    Helper function used to read in contents of a file. Returns as a string stored in memory

    :param path: path to the file to be read into memory
    :return: return a string representing the file.
    '''
    with open(path, "r") as inputSequence:
        data = inputSequence.read()
    return data

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

files = [] # store file contents
fileNames = [] # store file names
tmpFiles = [] # store tmpFileNames
dupFiles = [] # store dupFileNames, so this can be the input to sorting program

# read content all files in the specified directory into a list
with cd(dataDirectory):
	for file in os.listdir():
		if not file.startswith("."):
			files.append(readFile(file))
			fileNames.append(file)

# remove the third column from all files
i = 0
for file in files:
	cleanedLines = []
	cleanedFile = ""
	lines = file.split("\n")
	
	for line in lines: 
		thirdCol = line.split("\t")
		if line: 
			del thirdCol[2]
			#print("\t".join(thirdCol))
			cleanedLines.append("\t".join(thirdCol))
	cleanedFile = "\n".join(cleanedLines)	
	
	# create tmp file
	#with open(fileNames[i] + ".tmp", 'a') as f:
	#	f.write(cleanedFile)
	tmpFiles.append(fileNames[i] + ".tmp")
	with open(fileNames[i] + ".dup", 'a') as j:
		j.write(cleanedFile)
		dupFiles.append(fileNames[i] + ".dup")
	i+=1

# loop over files again to sort them
i = 0
for file in files:
	k = open(tmpFiles[i], "w")
	subprocess.call(["sort", "-d", dupFiles[i]], stdout = k)
	k.close()
	subprocess.call(["rm", dupFiles[i]])
	i+=1
print("Finished sort")
# perform the first comm test
f = open("intersect.txt", 'w')
subprocess.call(["comm", "-12", tmpFiles[0], tmpFiles[1]], stdout = f)
f.close()
print("Finished first comm")

# delete the first two tmp files
subprocess.call(["rm", tmpFiles[0]])
subprocess.call(["rm", tmpFiles[1]])


# loop over all tmp files, continuosly update intersect.txt
for i in range(2,len(tmpFiles)):
	f = open("intersect_tmp.txt", 'w')
	subprocess.call(["comm", "-12", "intersect.txt", tmpFiles[i]], stdout = f)
	subprocess.call(["rm", "intersect.txt"])
	subprocess.call(["cp", "intersect_tmp.txt", "intersect.txt"])
	subprocess.call(["rm", "intersect_tmp.txt"])
	f.close()
	subprocess.call(["rm", tmpFiles[i]])

# Get rid of duplicates in intersect.txt
# This step shouldn't be needed; have to be fixed later!!
print("run 'sort intersect.txt | uniq -c > intersect.u.txt'")
