# Python script to generate a table containing MFE free energy values
import pandas as pd
import os


type_name = ['Class1_IA', 'Class1_IB', 'Class1_IC', 'Class1_ID', 'Class1_IE', 'Class1_IF', 'Class1_IIIA', 'Class1_IIIB', 'Class1_IIIC', 'Class1_IIID', 'Class2_IIA', 'Class2_IIB', 'Class2_IIC', 'Class2_VA', 'Class2_VIB1', 'IU', 'orphan']

# initiate a dictionary for repests
repeat_dict = {}

for type in type_name:
    # file containing the results of R NA fold for all classes and subtypes
    file = os.path.join('{}_results.txt'.format(type))

    # read data from a result file
    with open(file) as f:
        read_data = f.readlines()
        read_data_formatted = [chunk.rstrip('\n') for chunk in read_data]

    # iterate through the formatted read data and extract the id of repeats and MFE values from a list
    for count in range(2, len(read_data_formatted), 6):
        repeat_name = read_data_formatted[count-2][1:].split('_')[0] + '@{}'.format(type)
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
    
    type_info = []
    for id in df.index:
        type = id.split('@')[1]
        type_info.append(type)

    df['Type'] = type_info

    # when the number of repeats is greater than 1, iterate over the repeatas and create a new column for a statistical indicator
    if len(df.columns) != 1: 
        statistics_list = []
            
        # iterate over each ID
        for i in range(len(df)):
            statistical_indicator = 0

            # iterate over each repeat in ID to calculate a statistical indicator
            for j in range(len(df.columns) - 2):
                prev_MFE_value = df.iloc[i][j]
                MFE_value = df.iloc[i][j+1]
                statistical_indicator += abs(MFE_value - prev_MFE_value)

            statistics_list.append("%.2f" % (statistical_indicator/len(df.columns)))
        
        # assign a new column in a dataframe
        df['Statistics'] = statistics_list
        df.to_excel('All_{}_repeats.xlsx'.format(len(df.columns)-2)) 