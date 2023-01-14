# x-cultural-recipes
Cross-cultural recipe adaptation

Format of a `recipe` 

```
{
'id': str,
'title': str,
'title_translated': Optional[str],
'ingredients': List[str],
'steps': List[str],
'dish': Optional[str],
}
```

Format of a `matched_recipe`

```
{
'source': recipe,
'targets': List[recipe]
}
```

Format of a data file: `jsonl` with one `matched_recipe` per line

| File  |  Link  |cn:en | Notes  | 
|---|---|---|---|
| Silver cn2en data - train  | [Download Link](https://drive.google.com/file/d/15eVi_MsW4DGnP2v000EOWIN935q94NAA/view?usp=share_link)  | 1:n* |    
| Silver cn2en data - val  |  [Download Link](https://drive.google.com/file/d/1Xm5w-ATg1HtJYTKu-ui1UhAtZ5naZqNE/view?usp=share_link) | 1:n  |    
| Silver cn2en data - test  | [Download Link](https://drive.google.com/file/d/1hiV-XcoknjtHvWXpg3QUzNkD3-XXYqDP/view?usp=share_link)  | 1:n  |   
| Gold cn2en data  | [Download Link](https://drive.google.com/file/d/1j3cOR4VGPb8hfGT5jLIZKKs3XuIAClus/view?usp=share_link)  | 1:1  |   
| Silver en2cn data - train  |[Download Link](https://drive.google.com/file/d/1rlMeapVEjXI2ghqcZo9daZU_xK5gV742/view?usp=share_link) | n:1 |    
| Silver en2cn data - val  | [Download Link](https://drive.google.com/file/d/1BLg8gVAMiXmA2hvwR95a9qYzERPZLvWS/view?usp=share_link) | n:1  |    
| Silver en2cn data - test  | [Download Link](https://drive.google.com/file/d/1W2uKg3yQWyYrXKJHbzVFIeuzkDijqdW8/view?usp=share_link) | n:1 |  
| Gold en2cn data  | [Download Link](https://drive.google.com/file/d/1tJjJbEHdILLr__NL4LX7S5ldJDKoueAH/view?usp=share_link)  | 1:1 |  
* n ≤ 10. Raw Chinese (recipe_corpus_finetune_en.json) and English (en_RecipeNLG.csv) datasets can be downloaded [Here](https://drive.google.com/drive/folders/17HG2yeKLSML3mZ-r-kRuRb-qPFNGjrXH?usp=share_link).

Statistics of CulturalDataset

| Direction  |  Source  | Target | Train  | Valid | Test | Golden |
|---|---|---|---|---|---|---|
| cn2en | 44,473 | 144,645 | 35,578 | 4,447 | 4,448 | 189 |
| en2cn | 43,767 | 120,674 | 35,013 | 4,377 | 4,377 | 79  | 
