#%%
import numpy as np
import sys
section = sys.argv[1]
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
sents_output = [[token[3] for token in sent] for sent in sents]
print(sents_output)
#%%
### getting plain text for dependency parsing
# sents_output = [" ".join([token[3] for token in sent]) for sent in sents]
# with open("{}.plain".format(section), "w") as f:
# 	for sent in sents_output:
# 		f.write(sent)
# 		f.write('\n')

from supar import Parser
parser_biaffine = Parser.load('crf-dep-en')
parser_biaffine = Parser.load('crf-dep-en')
parser_biaffine = Parser.load('crf-dep-en')
dataset_biaffine = parser_biaffine.predict(sents_output, prob=True, verbose=False)

for sent, arc in zip(output, dataset_biaffine.arcs):
	if np.random.rand()>0.5:
		for line, head in zip(sent, arc):
			line[6] = str(head)

print(output[0])
lines = []
for sent in output:
	for line in sent:
		lines += ['\t'.join(line)]
	lines.append('')
# sents_output = [[] ]
# print(lines[:20])


with open("{}.gz.parse.biaffine-gold.combined.bio".format(section), "w") as f:
	for line in lines:
		f.write(line)
		f.write('\n')
#%%


