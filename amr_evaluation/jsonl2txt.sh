#!/bin/bash
#SBATCH --job-name=parse
#SBATCH --partition=cpu
#SBATCH --ntasks=4
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=16GB
#SBATCH --output=parse.out
#SBATCH --time=00:01:00

outdir=/ceph/hpc/data/d2023d06-049-users/xamr/input
mkdir -p $outdir
python source2txt.py ../data/generation_results/human_cn2en/sampled_human_gpt4_cn2en.jsonl $outdir/cn2en_source.txt zh
python reference2txt.py ../data/generation_results/human_cn2en/sampled_human_gpt4_cn2en.jsonl $outdir/cn2en_reference.txt en
for jsonl in ../data/generation_results/human_cn2en/*.jsonl; do
	python prediction2txt.py $jsonl $outdir/$(basename $jsonl jsonl)txt en
done
python source2txt.py ../data/generation_results/human_en2cn/sampled_human_gpt4_en2cn.jsonl $outdir/en2cn_source.txt en
python reference2txt.py ../data/generation_results/human_en2cn/sampled_human_gpt4_en2cn.jsonl $outdir/en2cn_reference.txt zh
for jsonl in ../data/generation_results/human_en2cn/*.jsonl; do
	python prediction2txt.py $jsonl $outdir/$(basename $jsonl jsonl)txt zh
done
