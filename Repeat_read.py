from Bio import SeqIO

# read fasta file with SeqIO module for convenience
file = 'Class1_1A.fa'
open_file = list(SeqIO.parse(open(file), 'fasta'))

# lists containing sequence id and sequence from an input fasta file
labels = list(str(label.id) for label in open_file)
seqs = list(str(seq.seq) for seq in open_file)

# write a new file containing each repeat and its counter
labelled_file = open('{}'.format(file.removesuffix('.fa')) + '_labelled.fa', 'w')

# pre-set starting id, repeat counter for counting the number of repeats appearing in the dataset,
# and position for identifying the sequence positions in fasta file
prev_id = labels[0]
repeat_counter = 1
pos = 0

# write first sequence id and its sequence
read = '>' + labels[0] + '_1' + '\n'
read += seqs[0] + '\n'

# for loop with zip - to write a fasta file contatining each repeat with its counter
for id, sequence in zip(labels[1:], seqs[1:]):

    # when id is the same with the previous id, then add 1 to the repeat counter
    # then write sequence id and its sequence
    if id == prev_id:
        repeat_counter += 1
        read += '>' + id + '_{}'.format(repeat_counter) +'\n'
        read += sequence + '\n'
        pos += 1

    # when id is not the same with the previous id, start new repeat counter from 1
    else:
        repeat_counter = 1
        read += '>' + id + '_{}'.format(repeat_counter) + '\n'
        read += sequence + '\n'
        pos += 1
        prev_id = labels[pos]

# write the string generated into a file and close a newly written fasta file
labelled_file.write(read)
labelled_file.close()