__author__ = 'johngiorgi'

########################################################################################################################
# IMPORTS
######################################
import sys # for parsing command line arguments
import math
import os
import pandas as pd # for working with dataframes
import argparse # for parsing arguments from command line
##################

########################################################################################################################
# PERQUISITES
#####################################
# Script assumes all pairwise alignment files contain two sequences. The first sequence of each file will
# be considered the reference strain.

########################################################################################################################
# USING THE SCRIPT
######################################
# The script accepts as arguments (during a call to the script) input pairwise alignment files
# (must have extension .fasta), a window size (specified by -w).
# Creates a csv file named output.csv in the same directory that the script was called from

########################################################################################################################
########################################################################################################################
########################################################################################################################

########################################################################################################################
# FUNCTIONS
######################################
def readFile(path):
    '''
    Helper function used to read in contents of a file. Returns as a string stored in memory

    :param path: path to the file to be read into memory
    :return: return a string representing the file.
    '''
    with open(path, "r") as inputSequence:
        data = inputSequence.read()
    return data

def parseAlignments(alignmentFileName):
    '''
    Takes as input the name of an alignment file in fasta format. Returns a list of length two. The first element
    is the first sequence of the alignment file and the second element is the second sequence.

    :param alignmentFile: an alignment file in fasta format
    :return: a tuple containing each sequence from the input alignment file
    '''
    # read in alignment file using readFile
    rawAlignmentData = readFile(alignmentFileName)

    # First split by '>' to separate fasta seqs
    rawAlignmentData = rawAlignmentData.split('>')

    # Second split by newline to separate header from sequences
    rawAlignOne = rawAlignmentData[1].split('\n')
    rawAlignTwo = rawAlignmentData[2].split('\n')

    # Third delete first element, which is the header
    del rawAlignOne[0]
    del rawAlignTwo[0]

    # Fourth join the rest of sequence together
    seqAlignOne = "".join(rawAlignOne)
    seqAlignTwo = "".join(rawAlignTwo)

    return [seqAlignOne, seqAlignTwo]

    ## Test
    # seq1_test = []
    # seq2_test = []
    # for i in range(10):
    #    seq1_test.append(sequenceOneAlign[i])
    #    seq2_test.append(sequenceTwoAlign[i])

    # print("Seq 1 Test:", seq1_test)
    # print("Seq 2 Test:", seq2_test)
    # quit()

def genAlignmentScore(alignmentSequences):
    '''
    Given a list of alignment sequences from a pairwise alignment, this function will compute their "alignment score"
    which is essentially a 1 if the nucleotides at a given position match and 0 if they don't. Returns this alignment
    score as a list.

    :param alignmentSequences: a list of two alignment sequences from a pairwise alignment
    :return: alignmentScores: a list containing the alignment score for these two sequences. (1 is a match and 0 is a
    mismatch)
    '''
    # get each sequence alignment
    sequenceOneAlign = alignmentSequences[0]
    sequenceTwoAlign = alignmentSequences[1]
    # list for storing alignment scores. 0 = nucleotide no match or mismatch. 1 = match
    alignmentScores = []

    for i in range(0, len(sequenceOneAlign)):
        if sequenceOneAlign[i] == sequenceTwoAlign[i]:
            alignmentScores.append(1)
        else:
            alignmentScores.append(0)

    return alignmentScores

def genRollingAvg(windowSize, alignmentScores):
    '''
    This function will generate rolling averages for the alignment scores of two sequences
    each rolling average is mapped to a nucleotide position in the pairwise alignment sequence

    :param windowSize: size of the window for each rolling average
    :param alignmentScores: alignment scores from pairwise alignment file
    :return: tuple containing the rolling averages for each window and the corresponding window map
    '''
    # list to store rolling average
    rollingAlignmentAvg = []
    # list to store positions corresponding to rolling average
    rollingAlignmentPos = []

    for i in range(0, len(alignmentScores) - (windowSize - 1)):
        rollingAlignmentAvg.append((sum(alignmentScores[i:i + windowSize]) / windowSize) * 100)
        rollingAlignmentPos.append(i + math.ceil(windowSize / 2))

    return (rollingAlignmentAvg, rollingAlignmentPos)

########################################################################################################################

########################################################################################################################
# 1) Parsing command line arguments
######################################

# create the parser object.
parser = argparse.ArgumentParser(description = "Create identity curve matrix as a csv file. Example of usage: python3 identityCurve.py <alignment1.fasta> <alignment2.fasta> -w <windowSize>")
# add an argument for paths to filenames
parser.add_argument('filenames', metavar = '<filepath>', type=str, nargs = 2, help = 'the path to the input alignment files (MUST be in .fasta format)')
# add an argument for window size
parser.add_argument('-w','--window', metavar = '<window size>', type=int, nargs = 1, required = True, help = 'the window size of the rolling averages to be computed')
# parse the arguments, store as namespace object arguments. 
arguments = parser.parse_args()

# finally, store the parsed arugment values
windowSize = arguments.window[0] # set window size
rawAlignmentFiles = arguments.filenames # set alignment file names

########################################################################################################################
# 2) Generate the data frames
######################################

# this is bad style, fix this if you get a chance ... 
firstLoop = True
# list to store header strings for pandas data frame
header = ["Reference"]

# for each pairwise alignment, we do ...
for fileName in rawAlignmentFiles:
    # 1: parse the input pairwise alignment file
    pairwiseSequences = parseAlignments(fileName)
    # store reference strain in variable
    referenceStrainSeq = pairwiseSequences[0]
    # 2: generate the alignment score for the two sequences in this file
    alignmentScore = genAlignmentScore(pairwiseSequences)
    #print(alignmentScore)
    # 3: generate the rolling average for the alignment scores
    tmp = genRollingAvg(windowSize, alignmentScore)
    windowMapping = tmp[1]
    rollingAvg = tmp[0]

    # 4. loop over the mapped values of each window to nt position in the pairwise align sequence
    # if, at the mapped nt position, there is a gap in the pairwise alignment sequence,
    # change this map value to NA
    #print(fileName)
    #print(referenceStrainSeq)
    for i in range(0, len(windowMapping)):
        if referenceStrainSeq[windowMapping[i]] == '-':
            windowMapping[i] = 'NA'
            rollingAvg[i] = 'NA'


    # use list comprehension to remove rolling average windows mapped to
    # a gap in the pairwise alignment sequence of the reference strain.
    windowMapping = [window for window in windowMapping if window != 'NA']
    rollingAvg = [avg for avg in rollingAvg if avg != 'NA']

    #print(windowMapping)
    # map the windows back onto the reference strain nt's

    gapCount = 0
    #print("Window mapping", windowMapping[0])
    for nt in range(0, windowMapping[0]):
        if referenceStrainSeq[nt] == "-":
            gapCount+= 1

    #print("Gap count: ", gapCount)
    windowMapping[0] = windowMapping[0] - gapCount

    for window in range(1, len(windowMapping)):
        windowMapping[window] = windowMapping[window-1] + 1

    # Splice the window mapping and rolling averages at the maximum possible mapped 
    # nucleotide positon onward
    maxFirstWinPos = windowMapping.index(math.ceil(windowSize / 2))
    windowMapping = windowMapping[maxFirstWinPos:]
    rollingAvg = rollingAvg[maxFirstWinPos:]
    # splice the window mapping and rolling averages from first nucleotide position
    # to the minumum possible last mapped nucleotide position
    minLastWinPos = windowMapping.index(len(referenceStrainSeq.replace("-", "")) - math.ceil(windowSize / 2))
    windowMapping = windowMapping[:minLastWinPos]
    rollingAvg = rollingAvg[:minLastWinPos]

    #print("Length of windowMapping:", len(windowMapping))
    #print("Length of rollingAvg:", len(rollingAvg))

    # 5. append the rolling average for the pairwise alignment to the data frame
    if firstLoop: # if this is the first loop, create a pandas data frame
        finalDataRaw = pd.DataFrame({'mapped_nucleotides':windowMapping})
        finalDataRaw[fileName] = rollingAvg
    else: # otherwise append the rolling averages
        finalDataRaw[fileName] = rollingAvg

    # appeand file name of current fasta 
    header.append(fileName)

    # BAD PRACTICE, fix this
    firstLoop = False

########################################################################################################################
# 3) Write to file
######################################

# write data to csv in currently working directory
finalDataRaw.to_csv(r'output.csv', header=header, index=None, sep=' ', mode='a')