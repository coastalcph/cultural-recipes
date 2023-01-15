## Evaluation

1. prepare generation outputs as json file. Formated as :

> {"source": str, "prediction": str, "references": List(str) }    

2. run cmd as:

```shell script
pip install -r requirement.txt
python eval_seq2seq.py --folder outputs/epoch10/

```
