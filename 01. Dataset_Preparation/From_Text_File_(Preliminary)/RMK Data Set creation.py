
import pandas as pd
import numpy as np
import re
import csv

'''
Replacing some words.
Ex: Both @ , 'at' and 'after' are used for same purpose like @6:30 / at 6:30 / after 6:30. 
So I will replace the 'at' and 'after' by '@'
'''

# Read the whole file 
with open('rmk_broadcast.txt', 'r') as f:
    filedata = f.read()
    
# Replace some words in the text file

filedata = filedata.replace(' at', ' @')
filedata = filedata.replace('after', ' @')
filedata = filedata.replace('pm,','PM,')
filedata = filedata.replace('pm', 'PM,')
filedata = filedata.replace('nusrat:', 'nusrat - ')
filedata = filedata.replace('nusrat :','nusrat - ')

filedata = filedata.replace('nusrat - ','nusrat ~ ')  

# Creating a new text file which reflects the changes 

with open('rmk_broadcast_edited.txt', 'w') as file:
    file.write(filedata)

'''
Count frequency of some symbols 
Ex: This symbols are needed for spliting a line. So we need to ensure that every lines has the necessary symbols.
'''

tilde_count = 0
at_count = 0
comma_count = 0

with open('rmk_broadcast_edited.txt','r') as f:
    
    lines = f.readlines()   
    for line in lines:
        words = line.split()
        for word in words:
            if word == '~':
                tilde_count += 1
            # If a word starts with '@', ex: @ or @6pm
            if word[0] == '@':
                at_count += 1
            if word[-1] == ',':
                comma_count += 1
                
        # Check which line (if any) breaks the format
        if tilde_count != at_count:
            print(tilde_count)
            print(at_count)
            print(line)

print("Tilde counts are "+ str(tilde_count) )
print("@ counts are "+ str(at_count))
print("comma counts are "+ str(comma_count))

'''
Declaration of lists
'''
day  = []
date = []
year = []
bc_time = []
broadcaster = []

micro_time = []
is_sharp = []

# Loading the text file

list_of_lines = np.genfromtxt('rmk_broadcast_edited.txt', delimiter='\n', dtype='str')
print("Length is " + str(len(list_of_lines))) # If not an even number then wrong format

# Loading the necessary data into seperate lists

line_no = 0  
for line in list_of_lines:    
    if line_no%2 == 0:        
        # Monday, January 2, 2017 [Line format]
        # Split the line into 3 parts and returns the as a list
        words = line.split(sep=',')
        day.append(words[0].strip())
        date.append(words[1].strip())
        year.append(words[2].strip())
        
    else:
        # (16:59:39) nusrat - Broadcast: RMT @6:30pm, In Sha Allah. [Line format]

        lines = line.split(sep='~', maxsplit = 1)  
        # split into 2 parts [ ex:"(16:59:39) nusrat"  & "Broadcast: RMT @6:30pm, In Sha Allah." ]
        
        # 1st part manipulation [ex: (16:59:39) nusrat]
        words = lines[0].split(sep=' ')
        
        time = words[0].strip()
        bc_time.append(time[1:-4]) # avoid the opening and ending bracket
        broadcaster.append(words[1].strip())
        
        l = re.findall("\d+", lines[1])

        if len(l)== 1:   # Ex: 6pm
            l[0] = str(str(l[0]) + ":00")
            micro_time.append(l[0])
        elif len(l) == 0:
            micro_time.append(-1)  # after magrib
        else:
            m_time = str( str(l[0]) + ":" + str(l[1]) ) # Ex: 5:30pm
            micro_time.append(m_time)
        
        if 'sharp' in lines[1].lower():
            is_sharp.append(1)
        else:
            is_sharp.append(0)
            
    line_no = line_no + 1

# All lengths must be equal
print(len(day))
print(len(date))
print(len(year))
print(len(bc_time))
print(len(broadcaster))
print(len(micro_time))
print(len(is_sharp))

# Printing
for i in range(0,len(day)):
    print("Day: "+ str(day[i]) + "  ||  " 
          + "Date: "+ str(date[i]) + "  ||  " 
          + "Year: "+ str(year[i]) + "  ||  " 
          + "Broadcast Time: "+ str(bc_time[i]) + "  ||  " 
          + "Broadcaster : "+ str(broadcaster[i]) + "  ||  " 
          + "Micro Time : " + str(micro_time[i]) + "  ||  "
          + "Is Sharp ? : " + str(is_sharp[i]) )
    print()


# Creating a CSV file from these lists

with open('rmk_dataset.csv', 'w', newline='') as file:
    
    columns = ['Day', 'Date', 'Year', 'Broadcast_time', 'Broadcaster', 'Micro_time', 'Is_sharp_time?']
    the_writer = csv.DictWriter(file, fieldnames = columns)
    the_writer.writeheader()
    
    for i in range(0,len(day)):      
        the_writer.writerow({ 'Day': day[i], 
                              'Date': date[i], 
                              'Year':year[i], 
                              'Broadcast_time':bc_time[i], 
                              'Broadcaster': broadcaster[i],
                              'Micro_time': micro_time[i], 
                              'Is_sharp_time?': is_sharp[i] })
        
