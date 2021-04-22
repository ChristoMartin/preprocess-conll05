#%%
import numpy as np
import sys
section = sys.argv[1]
parsers = sys.argv[2:]
with open("{}.gz.parse.sdeps.combined.bio".format(section)) as f:
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
def yield_heads_of_parsers(input):
	with open(input) as f:
		lines = f.readlines()
		lines = [line.strip().split(' ') for line in lines]
	return lines
print(len(parsers))
heads = [yield_heads_of_parsers("{}.sdeps.{}".format(section, ind)) for ind in parsers]
labels = [yield_heads_of_parsers("{}.sdeps.{}.labels".format(section, ind)) for ind in parsers]
print(len(heads))
# print(len(heads))
combined_head = [[ [] for tok in sent] for sent in heads[0]]
for head, label in zip(heads, labels):
	assert (len(combined_head)==len(head))
	for comb_sent, sent, sent_label in zip(combined_head, head, label):
		assert  len(comb_sent) == len(sent)
		for comb_tok, tok, tok_label in zip(comb_sent, sent, sent_label):
			# print(tok)
			comb_tok.append(tok)
			comb_tok.append(tok_label)
# print("finished")
# print(heads[0][0])
# print(heads[1][0])
# print(combined_head)


for sent, arc in zip(output, combined_head):
	for line, head in zip(sent, arc):
		line[7:] = head + line[7:]
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
#
with open("{}.gz.parse.enhanced-sdeps-labels.combined.bio".format(section), "w") as f:
	for sent in output:
		# print(line)
		for line in sent:
			f.write('\t'.join(line))
			f.write('\n')
		f.write('\n')
#%%


