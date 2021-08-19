from Bio import SeqIO
import os

# a list containing different classes and subtypes of CRISPR repeats (small number of repeats)
type_name = ['Class1_IA', 'Class1_ID', 'Class1_IIIB', 'Class1_IIIC', 'Class1_IIID', 'Class1_IV', 'Class2_IIB', 'Class2_VA', 'Class2_VIB1']

# iterate over each type and perform RNA fold using the sourcecode
for type in type_name:

    file = os.path.join('{}_labelled.fa'.format(type))
    open_file = list(SeqIO.parse(open(file), 'fasta'))

    # lists containing sequence id and sequence from an input fasta file
    labels = list(str(label.id) for label in open_file)

    # automatise generating RNA fold results and visualised PostScript file using os library
    os.system('mkdir {}_result'.format(type))
    os.system('./RNAfold -p < {}_labelled.fa'.format(type, type))
    os.system('./RNAfold -p < {}_labelled.fa > {}_results.txt'.format(type, type))
 
    for label in labels:
        os.system('.././Utils/relplot.pl {}_ss.ps {}_dp.ps > {}_rss.ps'.format(label, label, label))
        os.system('mv {}_rss.ps {}_result'.format(label, type))

