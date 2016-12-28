Bioinformatics tools (Portfolio)
=======

## pairwise.py ##

The script will perform a pairwise analysis for each sequence in two input fasta files.The results will be printed to the console as a matrix. 

### To use ###

* First open the script. Set the variables secondStrainFileName and firstStrainFileName to the paths to the input fasta files.
* When calling the script, provide argument -p to align protein sequences or -n to align nucleotide sequences. 

### Example: ###

```
python3 pairwise.py -p
```

## identityCurve.py ##

This script, written in **Python** will accept as input multiple pairwise alignment files, where the first sequence in each alignment file is expected to be from the same organism - this is considered the reference sequence. 

A a csv file is created containing a matrix that will allow for subsequent plotting of an "identity curve". 

The identity curve is a rolling average of matches/mismatches in the pairwise alignment, where each window of these rolling averages is mapped back to a nucleotide position in the reference sequence.

The plot is saved in the same directory from which the script is called. 

### To use this script ###

During a call to the script, you must provide the following arguments:

* path(s) to one or more pairwise alignment files (in fasta format).
* name of output file 
* window size for rolling averages, in base pairs (bp)

### Example: ###

```
python3 identityCurve.py <alignment1.fasta> <alignment2.fasta> -w <windowSize>
```

## RNAseq_variability.R ##

This script, written in **R**, is designed to compute metrics of variabillity between replicate RNAseq transcriptome normalized gene count data. Currently, it will accept a csv file containing such data and determine the standard deviation and mean of the standard deviation over the mean of each replicates gene count. A final csv file will be created which contains a single standard deviation value and a single mean value for each replicate in the input file.

## RNAseq_workflow.py ##

The script, written in **Python**, will automate the process of downloading high-throughput full transcriptome RNAseq data from NCBI data base (in .sra format), trimming each read (which includes removing adaptor sequences) and then mapping the trimmed reads back to a reference genome. 

### To use ###

* First open the script. Set the variables secondStrainFileName and firstStrainFileName to the paths to the input fasta files.
* When calling the script, provide argument -p to align protein sequences or -n to align nucleotide sequences. 

### Example: ###

```
python3 pairwise.py -p
```

## gffFormater.py ##

This script, written in **Python**, will correct the hierarchical structure of a GFF3 file. The script will produce a new GFF3 file in which
the hierarchical organization of lines follows the conventions laid out by the Sequence Oncology Project. That is, all genes
are followed by their respective mRNA's, then exons, then CDS's.

## gffFormater.go ##

This script, written in **Go**, corrects problems specific to a database of arbuscular mycorrhizal fungus GFF3 files we were working with. The script removes any lines in the GFF3 that do not follow the conventions laid out by the Sequence Oncology Project, and corrects the "attributes" of each line by adding a unique ID (which was missing). Produces a new GFF3 file with the corrections made.

## findDups.py ##

Creates a file, called intersects.txt, which contains gene positions that are present in all files.

### usage ###

```
python3 findDups.py <path to directory containing data ONLY>
```
