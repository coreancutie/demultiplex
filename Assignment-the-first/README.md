# Demultiplexing and Index Swapping – Part 1

**Goals**: Look through a lane of sequencing generated from the 2017 BGMP cohort’s library preps and determine the level of index swapping and undetermined index-pairs, before and after quality filtering of index reads. In order to do this, we must first demultiplex the data. In Assignment the First, we will develop a strategy to de-multiplex samples to create **48 FASTQ files** that contain acceptable index pairs (read1 and read2 for 24 different index pairs), **two FASTQ files** with index-hopped reads-pairs, and **two FASTQ files** undetermined (non-matching or low quality) index-pairs. **Total of 52 fastq files!**

De-multiplexing is necessary for downstream analyses.

We submitted 24 indexed (dual matched) libraries for sequencing. The indexes are:

```
B1	GTAGCGTA    A5	CGATCGAT    C1	GATCAAGG
B9	AACAGCGA    C9	TAGCCATG    C3	CGGTAATC
B3	CTCTGGAT    C4	TACCGGAT    A11	CTAGCTCA
C7	CACTTCAC    B2	GCTACTCT    A1	ACGATCAG
B7	TATGGCAC    A3	TGTTCCGT    B4	GTCCTAAG
A12	TCGACAAG    C10	TCTTCGAC    A2	ATCATGCG
C2	ATCGTGGT    A10	TCGAGAGT    B8	TCGGATTC
A7	GATCTTGC    B10	AGAGTCCA    A8	AGGATAGC
```

4 FASTQ files are: 
```bash
1294_S1_L008_R1_001.fastq.gz
1294_S1_L008_R2_001.fastq.gz
1294_S1_L008_R3_001.fastq.gz
1294_S1_L008_R4_001.fastq.gz
```

Answers are on [Answers.md](Answers.md)

## Quality Score Distribution per-nucleotide
1.	Perform some initial data exploration!
    1. Determine which files contain the indexes, and which contain the paired end reads containing the biological data of interest. Create a table and label each file with either read1, read2, index1, or index2.
    2. Determine the length of the reads in each file.
    3. Determine the phred encoding for these data (either +33 or +64).
2.	Generate a per base distribution of quality scores for read1, read2, index1, and index2. Average the quality scores at each position for all reads and generate a per nucleotide mean distribution.
    1.	Turn in the four histograms.
    2.	What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively? 
    3.	How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)

## Develop an algorithm to de-multiplex the samples
Write up a strategy for developing an algorithm to de-multiplex files and reporting index-hopping given four input FASTQ files (two with biological reads, two with index reads) and the 24 known indexes above, demultiplex reads by index-pair, outputting:

- one R1 FASTQ file and one R2 FASTQ file **per** matching index-pair, 
- another two FASTQ files for non-matching index-pairs (index-hopping), and 
- two additional FASTQ files when one or both index reads are unknown or low quality (do not match the 24 known indexes [this includes indexes with 'N's in them] or do not meet a quality score cutoff)
    
Add the sequence of the index-pair to the header of BOTH reads in all of your FASTQ files for all categories (e.g. add “AAAAAAAA-CCCCCCCC” to the end of headers of every read pair that had an index1 of AAAAAAAA and an index2 of CCCCCCCC; this pair of reads would be in the unknown category as one or both of these indexes do not match the 24 known indexes).

Additionally, your algorithm should report: 
- the number of read-pairs with properly matched indexes (per index-pair)
- the number of read pairs with index-hopping observed
- the number of read-pairs with unknown index(es)

You should strive to report values for each possible pair of indexes (both swapped and dual matched).

### Be sure to:
- Define the problem
- Determine/describe what output would be informative
- Write examples (unit tests!):
    - INPUT FILES: R1 (biological read 1) R2 (index 1 -> i1) R3 (index 2 -> i2) R4 (biological R2)
    - Include four properly formatted input FASTQ files with read pairs that cover all three categories (dual matched, index-hopped, unknown index) (the bare MINIMUM is 6 files, Read 1 and Read 2 for dual, hopped, and unknown)
    - Include the appropriate number of properly formatted output FASTQ files given your input files
- Develop your algorithm using pseudocode
- Determine high level functions
