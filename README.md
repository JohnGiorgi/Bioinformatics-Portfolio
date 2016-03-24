# Bioinformatics tools (Portfolio)

## Standalone Scripts

#### gffFormater.py

This script will correct the hierarchical structure of a GFF3 file. The script will produce a new GFF3 file in which
the hierarchical organization of lines follows the conventions laid out by the Sequence Oncology Project. That is, all genes
are followed by their respective mRNA's, then exons, then CDS's.

### gffFormater.go

This script, written in Go, corrects problems specific to a database of arbuscular mycorrhizal fungus GFF3 files we were working with. The script removes any lines in the GFF3 that do not follow the conventions laid out by the Sequence Oncology Project, and corrects the "attributes" of each line by adding a unique ID (which was missing). Produces a new GFF3 file with the corrections made. 

## Scripts which rely on Class Library

### Class Library

House all the classes called upon by the scripts. 

### exonerate_script

Uses the command line exonerate tools to call exonerate from the command line with a protein sequence FASTA file query on a genomic sequence FASTA database.

### create_blast_database

Uses the command line BLAST tools from NCBI to convert a genomic sequence FASTA file into a blast database.

### splitter_script

Splits a FASTA file containing multiple protein sequences into multiple FASTA files containing n number of protein sequences. The multiple FASTA files are then used in parallize_tblastn as queries. 

### parallize_tblastn

A stand-alone script which uses pythons multiprocessing library to make TBLASTN calls from the command line, in parallel, between multiple protein sequence FASTA files and a genomic sequence FASTA database.




