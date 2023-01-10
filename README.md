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
| Silver cn2en data - train  | https://drive.google.com/file/d/15eVi_MsW4DGnP2v000EOWIN935q94NAA/view?usp=share_link  |   |    
| Silver cn2en data - val  |  https://drive.google.com/file/d/1Xm5w-ATg1HtJYTKu-ui1UhAtZ5naZqNE/view?usp=share_link |   |    
| Silver cn2en data - test  | https://drive.google.com/file/d/1hiV-XcoknjtHvWXpg3QUzNkD3-XXYqDP/view?usp=share_link  |   |   
| Gold cn2en data  |   |   |   
| Silver en2cn data - train  |  https://drive.google.com/file/d/1cJpNZs_E0O-ur6Yo8sDJrYycBrdXISot/view?usp=share_link |   |    
| Silver en2cn data - val  | https://drive.google.com/file/d/1t6QJcU68IXTUTYtAJ1Ee5gSJw7Vjd1HY/view?usp=share_link  |   |    
| Silver en2cn data - test  | https://drive.google.com/file/d/1ldenL_YaaK23ex-53ynwf-ufJEaR6zei/view?usp=share_link  |   |  
| Gold en2cn data  |   |   |     

