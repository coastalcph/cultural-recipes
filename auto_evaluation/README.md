## Evaluation

1. prepare generation outputs as json file. Formated as :

> {"source": str, "prediction": str, "references": List(str) }    

2. run cmd as:

Evaluate single file:
```shell script
pip install -r requirement.txt
python eval_seq2seq.py --folder ../data/generation_results/human_cn2en/ --file sampled_human_mt_zeroshot_cn2en.jsonl --tgt_lan en
```

Evaluate multiple files of a folder:

```shell script
pip install -r requirement.txt
python eval_seq2seq.py --folder ../data/generation_results/human_cn2en/ --tgt_lan en
```
