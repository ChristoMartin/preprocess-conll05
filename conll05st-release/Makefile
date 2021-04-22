
ifeq ($(sec), train)
    section=train-set
else ifeq ($(sec), dev)
    section=dev-set
else ifeq ($(sec), wsj)
    section=test.wsj
else
    section=test.brown
endif

ifeq ($(par), biaffine)
    parser=biaffine-dep-en
else ifeq ($(par), crf)
    parser=crf-dep-en
else ifeq ($(par), crf2o)
    parser=crf2o-dep-en
else ifeq ($(par), biaffine-bert)
    parser=biaffine-dep-bert-en
else
    parser=crfnp-dep-en
endif

all_parse:
	( \
       srun -p p singularity exec --nv ~/singularity/images/supar.simg python bio2plain.py $(section); \
       srun -p p singularity exec --nv ~/singularity/images/supar.simg python bio2goldheads.py $(section); \
       srun -p p  --gres gpu:1 singularity exec --nv ~/singularity/images/supar.simg python plain2head.py $(section) supar biaffine-dep-en sd & \
       srun -p v  --gres gpu:1 singularity exec --nv ~/singularity/images/supar.simg python plain2head.py $(section) supar biaffine-dep-bert-en sd & \
       srun -p p  --gres gpu:1  singularity exec --nv ~/singularity/images/supar.simg python plain2head.py $(section) supar crf-dep-en sd &\
       srun -p p  --gres gpu:1 singularity exec --nv ~/singularity/images/supar.simg python plain2head.py $(section) supar crf2o-dep-en sd & \
       srun -p p  --gres gpu:1 singularity exec --nv ~/singularity/images/supar.simg python plain2head.py $(section) supar crfnp-dep-en sd & \
#       srun -p p singularity exec --nv ~/singularity/images/supar.simg python plain2head.py $(section) supar biaffine-dep-en & \
       srun -p v  --gres gpu:1 singularity exec --nv ~/singularity/images/benepar.simg python plain2head.py $(section) benepar placeholder sd & \
       srun -p p singularity exec ~/singularity/images/benepar.simg python plain2head.py $(section) stanford-sr placeholder sd & \
    )
collect_sdeps:
	srun -p p singularity exec ~/singularity/images/benepar.simg python grouping_dep_parsings.py $(section) sd biaffine-dep-en biaffine-dep-bert-en crf-dep-en crf2o-dep-en crfnp-dep-en benepar stansr
gather_all_info:
	srun -p p singularity exec ~/singularity/images/benepar.simg python construct_bio_file.py train-set dev-set test.wsj test.brown
construct_enhance_file: 
	python bio_parsing_enhance.py $(section) biaffine-dep-en crf-dep-en crf2o-dep-en crfnp-dep-en
construct_ind_file:
	python bio_parsing_ind.py $(section) $(parser)

all_parse_ud:
	( \
       srun -p p singularity exec --nv ~/singularity/images/supar.simg python bio2plain.py $(section); \
       srun -p p singularity exec --nv ~/singularity/images/supar.simg python bio2goldheads.py $(section); \
       srun -p v  --gres gpu:1 singularity exec --nv ~/singularity/images/benepar.simg python plain2head.py $(section) benepar placeholder ud & \
    )
collect_udeps:
	srun -p p singularity exec ~/singularity/images/benepar.simg python grouping_dep_parsings.py $(section) ud benepar
gather_all_info_ud:
	srun -p p singularity exec ~/singularity/images/benepar.simg python construct_bio_file.py ud train-set dev-set test.wsj test.brown