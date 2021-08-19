from Bio import SeqIO
import os

# a list containing different classes and subtypes of CRISPR repeats (large number of repeats)
type_name = ['Class1_IB', 'Class1_IC', 'Class1_IE', 'Class1_IF', 'Class1_IIIA', 'Class2_IIA', 'Class2_IIC', 'IU', 'orphan']

# iterate over each type and perform RNA fold using the sourcecode
for type in type_name:

    file = os.path.join('{}_labelled.fa'.format(type))
    open_file = list(SeqIO.parse(open(file), 'fasta'))

    # lists containing sequence id and sequence from an input fasta file
    labels = list(str(label.id) for label in open_file)

    # automatise generating RNA fold results 
    os.system('mkdir {}_result'.format(type))
    os.system('./RNAfold -p < {}_labelled.fa'.format(type, type))
    os.system('./RNAfold -p < {}_labelled.fa > {}_results.txt'.format(type, type))

    # select labels from total labels by calculating divider using the number of repeats
    total_labels = len(labels)
    selected_labels = [labels[0]]
    counter = 0
    divider = total_labels // 100

    for label in labels[1:]:
        if label[-2:] == '_1' :
            counter += 1
        if counter % divider == 0 and label[-1] != 1:
            selected_labels.append(label)

    # for selected labels, generate PostScript files for visualisation
    for label in selected_labels:
        os.system('.././Utils/relplot.pl {}_ss.ps {}_dp.ps > {}_rss.ps'.format(label, label, label))
        os.system('mv {}_rss.ps {}_result'.format(label, type))

