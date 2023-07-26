#!/bin/bash -x
#SBATCH --job-name=smatchpp
#SBATCH -p gpu --gres=gpu:1
#SBATCH --ntasks=4 --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=16GB
#SBATCH --output=smatchpp.out
#SBATCH --time=08:00:00

eval "$(conda shell.bash hook)"
conda activate ~/anaconda3/envs/smatchpp
indir=/ceph/hpc/data/d2023d06-049-users/xamr/pred
outdir=/ceph/hpc/data/d2023d06-049-users/xamr/smatchpp
mkdir -p $outdir

for direction in cn2en en2cn; do
	for pred in $indir/sampled_human_*_$direction.txt; do
		python -m smatchpp      -a $pred \
			-b $indir/${direction}_reference.txt \
			-solver ilp \
			-edges dereify \
			-score_dimension main \
			-score_type micromacro \
			-log_level 20 \
			-output_format json \
			--bootstrap \
			--remove_duplicates > $outdir/$(basename $pred)
	done
done
