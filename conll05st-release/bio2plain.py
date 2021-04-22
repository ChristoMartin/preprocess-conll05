#%%
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
#%%
### getting plain text for dependency parsing
sents_output = [" ".join([token[3] for token in sent]) for sent in sents]
with open("{}.plain".format(section), "w") as f:
	for sent in sents_output:
		f.write(sent)
		f.write('\n')

#%%


