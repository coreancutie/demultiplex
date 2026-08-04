#!/usr/bin/env python

#need this import to use argparse variables
import argparse

#this is to make a fancy wile loop and count the line
import itertools 

#need this for opening zip file
import gzip as gz

#need this for opening making the matrix
import numpy as np


#creating my reverse complment function!
def rev_complement(barcode: str) -> str:
  '''Takes in a sequence that is DNA (string) and returns the complment of it
  as a string'''

  #the dictionary for the reserse complments
  reverse_dict:dict = {'A':'T',
                      'T':'A',
                      'C':'G',
                      'G':'C',
                      'N':'N'}

  #initalizing the reverse barcode
  comp_barcode:str = ''

  #looping though each barcode character
  for i in barcode:
    #getting the complmented string
    comp_barcode += reverse_dict[i]

  #reversing the order
  rev_barcode = comp_barcode[::-1]

  #return the reverse barcode
  return rev_barcode

#creating my arg parse function!
def get_args():
	'''this has 1 arguement: file'''
	parser = argparse.ArgumentParser(description="Getting")
	parser.add_argument("-f1", help="Filename for Read1", type=str, required=True)
	parser.add_argument("-f2", help="Filename for Index1", type=str, required=True)
	parser.add_argument("-f3", help="Filename for Index2", type=str, required=True)
	parser.add_argument("-f4", help="Filename for Read2", type=str, required=True)
	return parser.parse_args()

#calling the function (so in the terminal it runs)
args=get_args()

#reassiging args.f1 as R1
R1:str = args.f1

#reassiging args.f2 as I1
I1:str = args.f2

#reassiging args.f3 as I2
I2:str = args.f3

#reassiging args.f4 as R2
R2:str = args.f4

#creating a set to hold all of the known barcodes
known_bar:set = {'GTAGCGTA','CGATCGAT','GATCAAGG','AACAGCGA','TAGCCATG','CGGTAATC','CTCTGGAT','TACCGGAT',
                 'CTAGCTCA','CACTTCAC','GCTACTCT','ACGATCAG','TATGGCAC','TGTTCCGT','GTCCTAAG','TCGACAAG',
                 'TCTTCGAC','ATCATGCG','ATCGTGGT','TCGAGAGT','TCGGATTC','GATCTTGC','AGAGTCCA','AGGATAGC'}

#creating an empty dictionary to hold all of the variables that corrispond to the known filenames
known_file_name:dict = {}

#looping through the known barcodes
for i in known_bar:
  #populating the dictionary with the key as the barcode and the value a list of filename
  known_file_name[i] = [f"{i}_R1", f"{i}_R2"]

#looping through the dictionary
for key, value in known_file_name.items():
  #for each barcode opening up 2 files one for R1 and one for R2
  value[0] = open(f"{value[0]}.fq", "w")
  value[1] = open(f"{value[1]}.fq", "w")

#opening up hopped files
hopped_R1 = open("hopped_R1.fq", "w")
hopped_R2 = open("hopped_R2.fq", "w")

#opening up unknown files
unknown_R1 = open("unknown_R1.fq", "w")
unknown_R2 = open("unknown_R2.fq", "w")

#initalizing the counts for unknown, hopped, and matched records  
unknown_count:int = 0
hop_count:int =0
match_count:int =0
#initalizing an empty dictionary to count each of the hopped records
hop:dict = {}
#initalizing an empty dictionary to count each of the matched records
match:dict = {}

#opening all 4 files at the same time
with gz.open(R1, "rt") as r1, gz.open(I1, "rt") as i1, gz.open(I2, "rt") as i2, gz.open(R2, "rt") as r2:

  #initalizing empty lists to hold each record
  r1_record:list = []
  i1_record:list = []
  i2_record:list = []
  r2_record:list = []

  #this itertools will keep the line count for me 
  #count is initalized with 1 being the first line (not 0)
  for i in itertools.count(1):

    #read all 4 lines for each file
    r1_line = r1.readline().strip("\n")
    i1_line = i1.readline().strip("\n")
    i2_line = i2.readline().strip("\n")
    r2_line = r2.readline().strip("\n")

    #if the lines are empty (reached the end of the file), break!
    if r1_line == "" and i1_line == "" and i2_line == "" and r2_line == "":
      break

    #adding the lines to their respective lists
    r1_record.append(r1_line)
    i1_record.append(i1_line)
    i2_record.append(i2_line)
    r2_record.append(r2_line)

    #if I have reached the 4th line (final line in the record)
    if i % 4 == 0:
      #taking the reverse complment of the second index and replacing it in the list
      i2_record[1] = rev_complement(i2_record[1])
      
      #creating the combined barcode
      combinded_barcode = i1_record[1] + '-' + i2_record[1]

      #appending the combined barcode to the end of the header in both reads
      r1_record[0] = r1_record[0] + ' ' + combinded_barcode
      r2_record[0] = r2_record[0] + ' ' + combinded_barcode
      
      #if the barcodes ARE THE SAME and they are both in the known barcodes (matched)
      if i1_record[1] == i2_record[1] and i1_record[1] in known_bar and i2_record[1] in known_bar:
        #writiting the records to the files
        known_file_name[i1_record[1]][0].write(f"{r1_record[0]}\n{r1_record[1]}\n{r1_record[2]}\n{r1_record[3]}\n")
        known_file_name[i1_record[1]][1].write(f"{r2_record[0]}\n{r2_record[1]}\n{r2_record[2]}\n{r2_record[3]}\n")
        #increment the match counter
        match_count += 1

        #if the barcode is not a key in matched dictionary
        if combinded_barcode not in match:
          #make the barcode a key and initalize it as 1
          match[combinded_barcode] = 1

        #if the barcode is a keyin matched dictionary
        elif combinded_barcode in match:
          #increment it by 1
          match[combinded_barcode] += 1

      #if the barcodes are NOT THE SAME as each other and both known (hopped)
      elif i1_record[1] != i2_record[1] and i1_record[1] in known_bar and i2_record[1] in known_bar:
        #writiting the records to the files
        hopped_R1.write(f"{r1_record[0]}\n{r1_record[1]}\n{r1_record[2]}\n{r1_record[3]}\n")
        hopped_R2.write(f"{r2_record[0]}\n{r2_record[1]}\n{r2_record[2]}\n{r2_record[3]}\n")
        #increment the hop counter
        hop_count += 1

        #if the barcode is not a key in hopped dictionary
        if combinded_barcode not in hop:
          #make the barcode a key and initalize it as 1
          hop[combinded_barcode] = 1

        #if the barcode is a key in hopped dictionary
        elif combinded_barcode in hop:
          #increment it by 1
          hop[combinded_barcode] += 1
      
      #if the barcodes are not in the known barcodes (unkowned)
      else:
        #writiting the records to the files
        unknown_R1.write(f"{r1_record[0]}\n{r1_record[1]}\n{r1_record[2]}\n{r1_record[3]}\n")
        unknown_R2.write(f"{r2_record[0]}\n{r2_record[1]}\n{r2_record[2]}\n{r2_record[3]}\n")
        #incrementing the unknown count
        unknown_count += 1
    
      #empty the lists to get the next record
      r1_record:list = []
      i1_record:list = []
      i2_record:list = []
      r2_record:list = []
        

#looping through the dictionary
for key, value in known_file_name.items():
  #for each barcode closing up 2 files one for R1 and one for R2
  value[0].close()
  value[1].close()

#closing hopped files
hopped_R1.close()
hopped_R2.close()

#closing unknown files
unknown_R1.close()
unknown_R2.close()

#plotting the scores!
import matplotlib.pyplot as plt

#making figure size
plt.figure(figsize=(12, 8))

#plotting the bargraphs of how many matched barcodes there are
plt.bar(list(match.keys()), list(match.values()), color="green", label="matched index")
# plt.bar(list(hop.keys()), list(hop.values()), color="red", label="hopped index")
plt.bar_label

#adding lables
plt.xlabel("Matched barcodes")
plt.ylabel("Amount of Pairs")
plt.title(f"Plot of index pairs from FASTQ file")

#makes the x axis vertical
plt.xticks(rotation=45, fontsize=7)

#makes sure the labels don't get cut off 
plt.tight_layout()

#printing the legend on the plot
plt.legend()

#saving the figure
plt.savefig("demiluiplex_bar_chart.svg")

#make an empty array 
matrix = np.zeros((24,24))

#looping through the known barcode set, but sorted alphabetically
for i, row in enumerate(sorted(known_bar)):
  #looping through the known barcodes again
  for j, col in enumerate(sorted(known_bar)):
    
    #if the records are the same, look in matched dictionary
    if row == col:
      #checking if the unmatched index is in the hopped
      if f'{row}-{col}' in match:
        #replacing that number in the matrix with the number in the dictionary
        matrix[i,j] = match[f'{row}-{col}']

    #if the records are not the same, look in the hopped dictionary
    elif row != col:
      #checking if the unmatched index is in the hopped
      if f'{row}-{col}' in hop:
        #replacing that number in the matrix with the number in the dictionary
        matrix[i,j] = hop[f'{row}-{col}']

#this is the total counts of records, so I can report percentage
total:int = match_count + hop_count + unknown_count 

#print statements written to an output file
with open("demultiplex_output.md", "w") as file:
  #reporting the total records
  file.write(f"The total matched: {match_count}\n\nThe total hopped: {hop_count}\n\nThe total unknown: {unknown_count}\n\n")
  #reporting the percentage of each record
  file.write(f"\nThe percent matched: {(match_count/total):.3%}\n\nThe percent hopped: {(hop_count/total):.3%}\n\nThe percent unknown: {(unknown_count/total):.3%}\n\n")
  
  #writing a table for the matrix
  #writing the the header
  #"| |": is the empty box in the cornner
  # " | ".join(sorted(known_bar)): joins each of the barcodes with "|" as a seperater
  file.write("| |" + " | ".join(sorted(known_bar)) + " |\n")
  #writing the seperator line
  file.write("|-|" + "-|-".join("-" * len(known_bar)) + "-|\n")

  #making the data rows
  for i, bar in enumerate(sorted(known_bar)):
    #wiritng the bar then joiing the matrix line, making it a list, and each index a string
    file.write("| " + bar + " |" + " | ".join(list(matrix[i,:].astype(str))) + " |\n")
