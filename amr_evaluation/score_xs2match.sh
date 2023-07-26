#!/bin/bash -x
#SBATCH --job-name=xs2match
#SBATCH -p gpu --gres=gpu:1
#SBATCH --ntasks=4 --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=16GB
#SBATCH --output=xs2match.out
#SBATCH --time=08:00:00

eval "$(conda shell.bash hook)"
conda activate ~/anaconda3/envs/xs2match
indir=/ceph/hpc/data/d2023d06-049-users/xamr/pred
outdir=/ceph/hpc/data/d2023d06-049-users/xamr/xs2match
mkdir -p $outdir

cd Crossling-AMR-Eval/s2match/
for direction in cn2en en2cn; do
	for pred in $indir/sampled_human_*_$direction.txt; do
		bash x_evaluation-fixed-s2match.sh $pred \
			$indir/${direction}_reference.txt \
			> $outdir/$(basename $pred)
	done
done
