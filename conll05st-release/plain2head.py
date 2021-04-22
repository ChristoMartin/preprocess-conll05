import os
import sys
section = sys.argv[1]
parser_ind = sys.argv[2]
model_ind = sys.argv[3]
dep_type = sys.argv[4]
if dep_type == "sd":
	dep_type_ind = "sdeps"
else:
	dep_type_ind = "udeps"
with open("{}.plain".format(section)) as f:
	lines = f.readlines()
	


if parser_ind == 'supar':
	sents = [line.replace('(', '-LRB-').replace(')', '-RRB-').split(' ') for line in lines]

	from supar import Parser
	parser = Parser.load(model_ind)
	dataset = parser.predict(sents, prob=True, verbose=False)

	with open("{}.parsed.{}.{}".format(section, dep_type_ind, model_ind), "w") as f:
		for arc in dataset.arcs:
			f.write(' '.join(map(str, arc)))
			f.write('\n')
		print("finished {} {}".format(parser_ind, "heads"))
	with open("{}.parsed.{}.{}.labels".format(section, dep_type_ind, model_ind), "w") as f:
		for rel in dataset.rels:
			f.write(' '.join(map(str, rel)))
			f.write('\n')
		print("finished {} {}".format(parser_ind, "labels"))

if parser_ind == 'benepar':
	sents = [line.split(' ') for line in lines]

	import benepar, nltk
	parser = benepar.Parser("benepar_en3")
	# nlp = spacy.load('en_core_web_md')
	# if spacy.__version__.startswith('2'):
	# 	nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
	# else:
	# 	nlp.add_pipe("benepar", config={"model": "benepar_en3"})
	sents = [benepar.InputSentence(words=sent) for sent in sents]
	print(sents[0])
	dts = parser.parse_sents(sents)
	results = [' '.join(str(item).split()) for item in dts]
	print(len(results))
	# input = "{}.cdeps.{}".format(section, parser_ind)

	with open("{}.cdeps.{}".format(section, parser_ind), "w") as f:
		for item in results:

			# parse_str = ' '.join(str(item).split())
			# print(parse_str)
			f.write(item)
			f.write('\n')

	# command_normalization = "zcat {} | awk '{gsub(/\(/, \"-LRB-\", $1); gsub(/\)/, \"-RRB-\", $1); gsub(/\(/, \"-LRB-\", $2); gsub(/\)/, \"-RRB-\", $2); print $2\" \"$1\"\t\"$3}' | sed 's/\(.*\)\t\(.*\)\*\(.*\)/\2(\1)\3/' > \"{}.parse\"".format(input, input)
	# exit()
	STANFORD_CP = "{}/*:{}/*:".format("/home/u00222/opt/stanford-parsers/stanford-parser-full-2017-06-09", "/home/u00222/opt/stanford-parsers/stanford-postagger-full-2017-06-09")
	if dep_type == "sd":
		command = " java -Xmx8g -cp {} edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile \"{}.cdeps.{}\" -basic -conllx -keepPunct -makeCopulaHead > \"{}.{}.{}\"".format(STANFORD_CP, section, parser_ind, section, dep_type_ind, parser_ind)
	else:
		command = " java -Xmx8g -cp {} edu.stanford.nlp.trees.ud.UniversalDependenciesConverter -treeFile \"{}.cdeps.{}\" -basic > \"{}.udeps.{}\"".format(
			STANFORD_CP, section, parser_ind, section, parser_ind)
	print(command)
	os.system(command)
	if dep_type == "sd":
		with open("{}.{}.{}".format(section, dep_type_ind, parser_ind)) as f:
			lines = f.readlines()
	else:
		with open("{}.{}.{}".format(section, dep_type_ind, parser_ind)) as f:
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
	sents_output = [" ".join([token[6] for token in sent]) for sent in sents]
	labels_output = [" ".join([token[7] for token in sent]) for sent in sents]

	with open("{}.parsed.{}.{}".format(section, dep_type_ind,parser_ind), "w") as f:
		for sent in sents_output:
			f.write(sent)
			f.write('\n')
	with open("{}.parsed.{}.{}.labels".format(section, dep_type_ind, parser_ind), "w") as f:
		for sent in labels_output:
			f.write(sent)
			f.write('\n')
if parser_ind == 'stanford-sr':
	import re
	# STANFORD_CP = "{}/*:{}/*:".format("/home/u00222/opt/stanford-parsers/stanford-parser-full-2017-06-09", "/home/u00222/opt/stanford-parsers/stanford-postagger-full-2017-06-09")
	STANFORD_CP = "/home/u00222/opt/stanford-parsers/stanford-corenlp-4.2.0/*:"
	# command = "java -Xmx8g -cp {}  edu.stanford.nlp.parser.nndep.DependencyParser -model edu/stanford/nlp/models/parser/nndep/english_SD.gz -textFile {}.plain -outFile {}.sdeps.stansr".format(STANFORD_CP, section, section)
	command = " java -cp {} -Xmx8g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,depparse -depparse.model edu/stanford/nlp/models/parser/nndep/english_SD.gz  -ssplit.eolonly -tokenize.whitespace -file {}.plain -outputFormat conll".format(STANFORD_CP, section)
	print(command)
	os.system(command)

	head_pattern = re.compile("[a-z]+\(.+-(\d+), .*\)")

	with open("{}.plain.conll".format(section)) as f:
		lines = f.readlines()
	#%%
	container = []
	container_label = []
	sents = []
	labels = []
	for line in lines:
		if line != '\n':
			line_content = line.split()
			container += [line_content[5]]
			container_label += [line_content[6]]
		else:
			sents += [container]
			labels += [container_label]
			container = []
			container_label = []
	#%%
	sents_output = [" ".join([token for token in sent]) for sent in sents]
	labels_output = [" ".join([token for token in sent]) for sent in labels]

	with open("{}.parsed.{}.stansr".format(section, dep_type_ind), "w") as f:
		for sent in sents_output:
			f.write(sent)
			f.write('\n')
	with open("{}.parsed.{}.stansr.labels".format(section, dep_type_ind), "w") as f:
		for sent in labels_output:
			f.write(sent)
			f.write('\n')
