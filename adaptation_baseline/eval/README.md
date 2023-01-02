## Evaluation

1. prepare generation outputs as json file. Formated as :

> {"recover": generation outputs, "reference": English recipes, "source":Chinese recipes}    
> see output/outputs/epoch10/sample_1.json for example.

2. run cmd as:

```shell script
pip install -r requirement.txt
python eval_seq2seq.py --folder outputs/epoch10/

# Note: folder contains multiple json files to calculate self-BLEU score, i.e. one chinese recipes adapt to multiple English recipes.
```