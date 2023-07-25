#!/bin/bash -x
#SBATCH --job-name=parse
#SBATCH -p gpu --gres=gpu:1
#SBATCH --ntasks=4 --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=16GB
#SBATCH --output=parse.out
#SBATCH --time=08:00:00

echo $SLURMD_NODENAME $CUDA_VISIBLE_DEVICES
. /etc/profile.d/modules.sh
eval "$(conda shell.bash hook)"
conda activate ~/anaconda3/envs/xamr
pip3 install torch==1.10.2+cu113 torchvision torchaudio  -f https://download.pytorch.org/whl/torch_stable.html
checkpoint=XAMR/ckpt/best.pt # this points to the pretrained model you have downloaded
indir=/ceph/hpc/data/d2023d06-049-users/xamr/input
outdir=/ceph/hpc/data/d2023d06-049-users/xamr/pred
mkdir -p $outdir

for dataset in $indir/*.txt; do
	PYTHONPATH=XAMR python3 XAMR/bin/predict_amrs.py \
	   --model facebook/mbart-large-50-many-to-many-mmt \
	   --checkpoint ${checkpoint} \
	   --dataset ${dataset} \
	   --nproc-per-node 4 \
	   --gold-path $outdir/$(basename $dataset txt)gold.txt \
	   --pred-path $outdir/$(basename $dataset txt)pred.txt \
	   --beam-size 4 \
	   --batch-size 5000 \
	   --penman-linearization \
	   --use-pointer-tokens
done
