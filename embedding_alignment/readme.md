This folder will store information about token-level translation / dictionary induction including:

- Code on how to train static embeddings (fasttext) on the two full monolingual corpora (Chinese- English)
- Induce mapping between the embeddings
- Mapping evaluation


# Fasttext Embeddings

To produce the fasttext embeddings you simply need to upoload your data in google drive, load the .ipynb file in Jupyter Notebook/Google Colab and mount your google drive to the notebook. Run all the cells and at the end the output will be two .txt files with the fasttext embeddings. (Comment: now that I have access to the cluster, I will probably adapt this code to a command-line interface.

# Mapping between embeddings

To produce a mapping between the embeddings we used [VecMap](https://github.com/artetxem/vecmap), an open source implementation that learns cross-lingual word embedding mappings. For this experiment you simply need to clone their [repository](https://github.com/artetxem/vecmap) and run:


```
python3 map_embeddings.py --unsupervised SRC.EMB TRG.EMB SRC_MAPPED.EMB TRG_MAPPED.EMB
```

`SRC.EMB` and `TRG.EMB` refer to the input monolingual embeddings, which should be in the word2vec text format, whereas `SRC_MAPPED.EMB` and `TRG_MAPPED.EMB` refer to the output cross-lingual embeddings. 

If you have a NVIDIA GPU, append the --cuda flag to the above commands to make things faster.

# Evaluation
You can evaluate the mapped embeddings in bilingual lexicon extraction (aka dictionary induction or word translation) as follows:

```
python3 eval_translation.py SRC_MAPPED.EMB TRG_MAPPED.EMB -d TEST.DICT
The above command uses standard nearest neighbor retrieval by default. For best results, it is recommended that you use CSLS retrieval instead:
```
```
python3 eval_translation.py SRC_MAPPED.EMB TRG_MAPPED.EMB -d TEST.DICT --retrieval csls
While better, CSLS is also significantly slower than nearest neighbor, so do not forget to append the --cuda flag to the above command if you have a NVIDIA GPU.
```

In addition to bilingual lexicon extraction, you can also evaluate your mapped embeddings in cross-lingual word similarity as follows:

```
python3 eval_similarity.py -l --backoff 0 SRC_MAPPED.EMB TRG_MAPPED.EMB -i TEST_SIMILARITY.TXT
```

Finally, the [VecMap repository](https://github.com/artetxem/vecmap#readme) also offers an evaluation tool for monolingual word analogies, which mimics the one included with word2vec but should run significantly faster:

```
python3 eval_analogy.py -l SRC_MAPPED.EMB -i TEST_ANALOGIES.TXT -t 30000
```

The training dictionary `TRAIN.DICT`, if any, should be given as a text file with one entry per line (source word + whitespace + target word). I guess the same applies to the `TEST.DICT` ? 
