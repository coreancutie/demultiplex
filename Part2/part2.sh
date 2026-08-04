#!/bin/bash

#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=bgmp                  #REQUIRED: which partition to use
#SBATCH --cpus-per-task=4                 #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4GB per cpu
#SBATCH --mail-user=catcar@uoregon.edu     #optional: if you'd like email
#SBATCH --mail-type=ALL                   #optional: must set email first, what type of email you want
#SBATCH --job-name=demultiplex_3rd            #optional: job name
#SBATCH --output=demultiplex_3rd_%j.out       #optional: file to store stdout from job, %j adds the assigned jobID
#SBATCH --error=demultiplex_3rd_%j.err        #optional: file to store stderr from job, %j adds the assigned jobID

mamba activate bgmp_demultiplex

/usr/bin/time -v ./part2.py -f1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
-f2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
-f3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
-f4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz
