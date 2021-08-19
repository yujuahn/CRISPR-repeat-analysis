# Python script to generate a table containing MFE free energy values
import pandas as pd
import os

# file containing the results of RNA fold for all classes and subtypes
file = os.path.join('All_results.txt')

# initiate a dictionary for repests
repeat_dict = dict()

# read data from a result file
with open(file) as f:
    read_data = f.readlines()
    read_data_formatted = [chunk.rstrip('\n') for chunk in read_data]

# iterate through the formatted read data and extract the id of repeats and MFE values from a list
for count in range(2, len(read_data_formatted), 6):
    repeat_name = read_data_formatted[count-2][1:].split('_')[0]
    MFE_value = read_data_formatted[count][-7:-2]
    
    # add a new repeat key having an empty list as a value
    if repeat_name not in repeat_dict.keys():
        repeat_dict[repeat_name] = list()
    # if a repeat exists in the key, append MFE value to the list
    repeat_dict[repeat_name].append(float(MFE_value))

# obtain a repeat counter, the number of repeats
repeat_counter = set(len(val) for val in repeat_dict.values())
# initiate a nested dictionary with keys containing each number of CRISPR repeats
repeat_collection = {'dict_' + str(k) :{} for k in repeat_counter}

# iterate over key and value in repeat dict previously built to construct a nested dictionary containing different number of repeats
for key, val in repeat_dict.items():
    repeat_count = str(len(val))
    repeat_collection['dict_{}'.format(repeat_count)][key] = val

# data frame is constructed from each number of repeat and is converted into an excel file
for key in repeat_collection.keys():
    dict = repeat_collection[key]
    repeat_num = int(key.split('_')[1])
    df = pd.DataFrame.from_dict(dict, orient = 'index', columns = ['MFE_{}'.format(i+1) for i in range(repeat_num)])
    df.to_excel('Results_{}_repeats.xlsx'.format(repeat_num)) 