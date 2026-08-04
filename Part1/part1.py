#!/usr/bin/env python

#need this import to use argparse variables
import argparse

#need this is make empy list of 0
import numpy as np

#need this for opening zip file
import gzip as gz

def get_args():
	'''this has 1 arguement: file'''
	parser = argparse.ArgumentParser(description="Getting")
	parser.add_argument("-f", help="Filename", type=str, required=True)
	parser.add_argument("-l", help="length of sequence", type=int, required=True)
	return parser.parse_args()

#calling the function (so in the terminal it runs)
args=get_args()

#reassiging args.filename as f
f:str = args.f

#reassiging args.filename as f
l:int = args.l


def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    
    #uses ord to get the phred value
    #subtract 33 to get actual phred score
    return ord(letter) - 33
 
#making an empy list
my_list: list = np.zeros(l)

#opening the file
# with open(f, "r") as fh: US THIS FOR TEST FILES

#"rt" is so it reads the file as text and not as binary jiberish
with gz.open(f, "rt") as fh:
    
    #initalizing line count to get qual score lines
    line_count = 0

    #for each line in f (file)
    for line in fh:
        #add the line count
        line_count += 1
        
        #getting rid of newline
        line = line.strip('\n')
        
        #getting the quality score line (line no. 4)
        if line_count%4 == 0:
            #getting the score and it's poisiton in the line
            for j, score in enumerate(line):
                my_list[j] += convert_phred(score)


# print("Done with populating the list!")

score_lines = line_count / 4

#looping through the
for i, score in enumerate(my_list):
    #calculating the mean and storing it back into my_list
    my_list[i] = score / score_lines

# print("Done getting the averages!")

#plotting the scores!
import matplotlib.pyplot as plt

#making figure size
plt.figure(figsize=(12, 5))

#adding gridlines
plt.grid()

#plotting the mean quality scores as dots in pink
plt.plot(my_list, 'o', color="pink")

#adding lables
plt.xlabel("Base Position")
plt.ylabel("Mean Quality Score")
plt.title(f"Plot of Mean Quality Score of {f[-15:-13]} FASTQ file for Each Base Position in a Sequence")

#saving the figure
#for the test use f[:-3]
plt.savefig(f"{f[38:-9]}.png")