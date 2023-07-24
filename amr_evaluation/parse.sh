#!/bin/bash
#SBATCH --job-name=parse
#SBATCH --partition=cpu
#SBATCH --ntasks=4
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=16GB
#SBATCH --output=parse.out
#SBATCH --time=00:01:00

checkpoint=ckpt/best.pt # this points to the pretrained model you have downloaded

dataset=tmp.txt # this points to the data you want to parse (see detailed explanation below)
python prediction2txt.py sampled_human_gpt4_cn2en.jsonl $dataset en

for jsonl in ../../data/generation_results/human_cn2en/*.jsonl; do
	python prediction2txt.py $jsonl $dataset en
	PYTHONPATH=. python3 bin/predict_amrs.py \
	   --model facebook/mbart-large-50-many-to-many-mmt \
	   --checkpoint ${checkpoint} \
	   --dataset ${dataset} \
	   --nproc-per-node 4 \
	   --gold-path tmp-gold.txt \
	   --pred-path tmp-pred.txt \
	   --beam-size 4 \
	   --batch-size 5000 \
	   --penman-linearization \
	   --use-pointer-tokens
done
