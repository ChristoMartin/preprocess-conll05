#%%
from copy import deepcopy

import numpy as np
import sys
section = sys.argv[1]
parsers = sys.argv[2:]
with open("{}.gz.parse.synt.combined.bio".format(section)) as f:
	lines = f.readlines()
#%%
container = []
sents = []
for line in lines:
	if line != '\n':
		container += [line.strip().split('\t')]
	else:
		sents += [container]
		container = []

output = sents


for sent in output:
	root_node = deepcopy(sent[0])
	root_node[2] = -1
	root_node[5] = 'ROOT'
	root_node[6] = 'ROOT'
	root_node[3] = 'ROOT'
	root_node[19] = 'root'
	# root_node[20] = 'ROOT'
	root_node[4] = -1
	for idx in range(7, 19):
		root_node[idx]=0
	root_node[24] = 'O'
	root_node[21] = '-'
	root_node[22] = '-'
	root_node[31:] = ['O']*len(root_node[31:])
	sent.insert(0,root_node)
	for token_idx in range(len(sent)):
		sent[token_idx][2] = int(sent[token_idx][2])+1


# root_node = ["conll05", -1, 0, "ROOT", -1, ]

# def yield_heads_of_parsers(input):
# 	with open(input) as f:
# 		lines = f.readlines()
# 		lines = [line.strip().split(' ') for line in lines]
# 	return lines
# print(len(parsers))
# heads = [yield_heads_of_parsers("{}.sdeps.{}".format(section, ind)) for ind in parsers]
# print(len(heads))
# # print(len(heads))
# combined_head = [[ [] for tok in sent] for sent in heads[0]]
# for head in heads:
# 	assert (len(combined_head)==len(head))
# 	for comb_sent, sent in zip(combined_head, head):
# 		assert  len(comb_sent) == len(sent)
# 		for comb_tok, tok in zip(comb_sent, sent):
# 			# print(tok)
# 			comb_tok.append(tok)
# print("finished")
# print(heads[0][0])
# print(heads[1][0])
# print(combined_head)


# for sent, arc in zip(output, combined_head):
# 	for line, head in zip(sent, arc):
# 		line[7:] = head + line[7:]
# print(output[0])


#
# print(output[0])
# lines = []
# for sent in output:
# 	for line in sent:
# 		lines += ['\t'.join(line)]
# 	lines.append('')
# # sents_output = [[] ]
# # print(lines[:20])
#
# #
with open("{}.gz.parse.synt-root.combined.bio".format(section), "w") as f:
	for sent in output:
		# print(line)
		for line in sent:
			line = [str(i) for i in line]
			f.write('\t'.join(line))
			f.write('\n')
		f.write('\n')
#%%


