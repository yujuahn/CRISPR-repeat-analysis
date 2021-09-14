# Python script to generate a plot of MFE changes for each number of repeats
import pandas as pd
import seaborn as sns

# define total number of repeats that appear in CRISPR repeat dataset
num_of_repeats = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '19', '21', '24']

# to optimise parameters in seaborn plotting, define each parameter - trial and error approach
top_value = [0.95, 0.95, 0.95, 0.95, 0.9, 0.9, 0.9, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
col_wrap = [4, 4, 4, 4, 4, 3, 4, 3, 3, 3, 3, 3, 2, 2, 2, 1, 2, 2, 1]

# plotting 
for idx, num in enumerate(num_of_repeats):
    # open the excel file containing the table with MFE value for each number of repeats
    df = pd.read_excel('All_{}_repeats.xlsx'.format(num), index_col=None)

    # store type information for later use
    type_info = df['Type'].to_list()

    # slice transposed dataframe for a time-serial plotting
    df = df.transpose()[1:int(num)+1]

    # add a new column 'Time' to melt a dataframe correctly
    df['Time'] = [str(i+1) for i in range(int(num))]

    # modify a dataframe for a time-serial plot
    df = df.melt('Time', var_name='cols',  value_name='vals')
    
    # initialise type_list from type_info, with a repeat having the same value with the number of repeats
    type_list = []
    for type in type_info:    
        type_list += [type] * int(num)

    # add a new column to a modified dataframe to restore type information
    df['Type'] = type_list

    # predefine palette to make hue of different repeats the same
    palette = sns.color_palette(['midnightblue'], len(df)//int(num))

    # use a seaborn relplot to initialise facet grid and define parameters
    plot = sns.relplot(kind='line', data=df, x="Time", y="vals", col="Type", hue='cols', col_wrap=col_wrap[idx], legend=False, palette=palette, facet_kws={'sharex': 'False'})
    
    # format a generated plot and save it
    plot.fig.suptitle("Change in MFE values for CRISPR repeat" ,
               fontsize = 'x-large', 
               fontweight = 'bold' )
    
    plot.fig.subplots_adjust(top = top_value[idx])
    plot.set_axis_labels( "Time point" , "Minimum Free Energy (kcal/mol)" )
    plot.savefig("{}_repeats_summary.png".format(num))
    