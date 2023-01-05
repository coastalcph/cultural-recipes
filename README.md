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

| File  |  Link  | Notes  | 
|---|---|---|
| Silver cn2en data - train  |   |   |    
| Silver cn2en data - val  |   |   |    
| Silver cn2en data - test  |   |   |   
| Gold cn2en data  |   |   |   
| Silver en2cn data - train  |   |   |    
| Silver en2cn data - val  |   |   |    
| Silver en2cn data - test  |   |   |   | Gold en2cn data  |   |   |     
| Gold en2cn data  |   |   |   

