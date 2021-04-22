#%%
import sys
section = sys.argv[1]
with open("{}.plain".format(section)) as f:
	lines = f.readlines()
	sents = [line.strip().split(' ') for line in lines]

#%%

import sys
from supar import Parser

#%%

### getting plain text for dependency parsing
# sents_output = [" ".j???oin([token[3] for token in sent]) for sent in sents]
# with open("{}.plain".format(section), "w") as f:
# 	for sent in sents_output:
# 		f.write(sent)
# 		f.write('\n')

#%%
parser_biaffine = Parser.load('biaffine-dep-en')
# parser_biaffine_bert = Parser.load('biaffine-dep-bert-en')
parser_crf_dep_en = Parser.load('crf-dep-en')
parser_crf2o_dep_en = Parser.load('crf2o-dep-en')

#%%
# sents = sents

#%%
dataset_biaffine = parser_biaffine.predict(sents, prob=True, verbose=False)
# dataset_biaffine_bert = parser_biaffine_bert.predict(sents, prob=True, verbose=False)
dataset_crf2o_dep_en = parser_crf2o_dep_en.predict(sents, prob=True, verbose=False)
dataset_crf_dep_en = parser_crf_dep_en.predict(sents, prob=True, verbose=False)

#%%
with open("{}.parsed.biaffine".format(section), "w") as f:
	for result in dataset_biaffine.arcs:
		f.write(" ".join(map(str, result)))
		f.write('\n')
#%%
with open("{}.parsed.crf".format(section), "w") as f:
	for result in dataset_crf_dep_en.arcs:
		f.write(" ".join(map(str, result)))
		f.write('\n')
#%%
with open("{}.parsed.crf2o".format(section), "w") as f:
	for result in dataset_crf2o_dep_en.arcs:
		f.write(" ".join(map(str, result)))
		f.write('\n')

#%%


