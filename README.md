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


| File  |  Format | Link  | Notes  | 
|---|---|---|---|
| Silver cn2en data  | {'train': `List(matched_recipe)`, 'val': `List(matched_recipe)`, 'test': `List(matched_recipe)`} |   |   |   
| Gold cn2en data  |  `List(matched_recipe)` |   |   |   
| Silver en2cn data  | {'train': `List(matched_recipe)`, 'val': `List(matched_recipe)`, 'test': `List(matched_recipe)`} |   |   |   
| Gold en2cn data  |  `List(matched_recipe)`  |   |   |   
