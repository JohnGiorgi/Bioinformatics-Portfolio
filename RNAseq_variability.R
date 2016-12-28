# This script is designed to compute metrics of variabillity between replicate
# RNAseq transcriptome normalized gene count data. Currently, it will accept
# a csv file containing such data and determine the standard deviation and mean
# of the standard deviation over the mean of each replicates gene count.

# A final csv file will be created which contains a single standard deviation 
# value and a single mean value for each replicate in the input file.

# the information that must be set on each run is as follows: (START)
# set the path to the input file
input.file = paste("/Volumes/Storage/RNASeq_data/yeast/",
                   "study_1/RNA_normalized_counts_study_1.csv", sep = "")
# for example, if each transcriptome is analyzed in duplicate, set this to 2
num.replicates = 3
# for example, if the first cohort is to be named cohort 1, set this to 1
cohort.start = 1
# (END)

# read in the normalized gene counts
normalized.counts <- read.csv(input.file, sep=",", header=TRUE, row.names = 1)
# set the number of samples
num.samples = ncol(normalized.counts)
# get the row names from normalized.counts
gene.names <- rownames(normalized.counts)
# get the column names from normalized.counts
sample.names <- colnames(normalized.counts)

# loop over each value from 1 to num.samples, with a step of num.replicates
for (i in seq(1,num.samples, by = num.replicates)) {
  # create temporory data frame, with first replicate from the current sample
  tmp.dframe <- data.frame(normalized.counts[,i])
  # add the correct colname
  colnames(tmp.dframe) <- sample.names[i]
  # then loop over the remaining replicates, add these to the data frame
  for (j in seq(i+1, i+num.replicates-1)) {
    tmp.dframe[[sample.names[j]]] <- normalized.counts[,j]
  }
  
  rownames(tmp.dframe) <- gene.names  # add rownames to tmp data frame
  tmp.dframe[tmp.dframe == 0] <- NA  # replace all 0's with NA
  tmp.dframe <- na.omit(tmp.dframe)  # remove all rows containing NA
  
  # next, compute the stdev, mean, and stdev/mean for each row
  row.stdev <- apply(tmp.dframe,1, sd, na.rm = TRUE)  # calculate row stdev
  row.means <- rowMeans(tmp.dframe, na.rm = TRUE)  # calculate row means
  row.varience <- row.stdev/row.means  # calculate the 'varience'
  
  # print the varience values
  print(paste("Cohort ", cohort.start, " SD:", sd(row.varience)))
  print(paste("Cohort ", cohort.start, " Mean:", mean(row.varience)))
  
  cohort.start = cohort.start + 1  # increment the cohort counter

}