# CulturalRecipes
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

[//]: # (| File  |  Link  |cn:en | Notes  | )

[//]: # (|---|---|---|---|)

[//]: # (| Silver cn2en data - train  | [Download Link]&#40;https://drive.google.com/file/d/15eVi_MsW4DGnP2v000EOWIN935q94NAA/view?usp=share_link&#41;  | 1:n |    )

[//]: # (| Silver cn2en data - val  |  [Download Link]&#40;https://drive.google.com/file/d/1Xm5w-ATg1HtJYTKu-ui1UhAtZ5naZqNE/view?usp=share_link&#41; | 1:n  |    )

[//]: # (| Silver cn2en data - test  | [Download Link]&#40;https://drive.google.com/file/d/1hiV-XcoknjtHvWXpg3QUzNkD3-XXYqDP/view?usp=share_link&#41;  | 1:n  |   )

[//]: # (| Gold cn2en data  | [Download Link]&#40;https://drive.google.com/file/d/1epyn9TIrBRNAn5OpQdckH7fBsUzac9Wi/view?usp=share_link&#41;  | n:n  |   )

[//]: # (| Silver en2cn data - train  |[Download Link]&#40;https://drive.google.com/file/d/1rlMeapVEjXI2ghqcZo9daZU_xK5gV742/view?usp=share_link&#41; | n:1 |    )

[//]: # (| Silver en2cn data - val  | [Download Link]&#40;https://drive.google.com/file/d/1BLg8gVAMiXmA2hvwR95a9qYzERPZLvWS/view?usp=share_link&#41; | n:1  |    )

[//]: # (| Silver en2cn data - test  | [Download Link]&#40;https://drive.google.com/file/d/1W2uKg3yQWyYrXKJHbzVFIeuzkDijqdW8/view?usp=share_link&#41; | n:1 |  )

[//]: # (| Gold en2cn data  | [Download Link]&#40;https://drive.google.com/file/d/1mVk9Elz9WPGZDt45g6rQOPHtf9CaK1Xo/view?usp=share_link&#41;  | n:n |  )

[//]: # ()
[//]: # (n ≤ 10. )

| Set    | direction | Scale | Link |  Notes  |
|--------|-----------|-------|---| ---|
| Silver | cn2en     | 82    | [Download](https://drive.google.com/drive/folders/1W1wf29Xe0J-sqvesJuH70lhajAmxzBVV?usp=sharing) | 1:1 |
| Human  | cn2en     | 25    | [Download](https://drive.google.com/drive/folders/1WUrOuXG8mrz9Mio5oponjiuEc6JCgplH?usp=sharing) | 1:1 |
| Silver | en2cn     | 52    | [Download](https://drive.google.com/drive/folders/1s14s8bEFtuHsEu5VcCnoUYsxIR1k6jRj?usp=sharing) | 1:1 |
| Human  | en2cn     | 41    | [Download](https://drive.google.com/drive/folders/1GWNdVwMtWTuTWiaoT3CXuYtxRlLhS1he?usp=sharing) | 1:1 |

[Chinese monolingual dataset](https://drive.google.com/file/d/1U9qpLk5VzQM4lY2NujGTsnz1TkIy-EO2/view?usp=share_link) (cleaned) and [English monolingual dataset](https://drive.google.com/file/d/1WhKebcqzBTC_8T679ROmuUPy0sHi_4OL/view?usp=share_link) (raw) 

Statistics of CulturalDataset

| Direction  |  Source  | Target | Train  | Valid | Test | Silver | Human |
|---|---|---|---|---|---|--------|-------|
| cn2en | 44,473 | 144,645 | 35,578 | 4,447 | 4,448 | 82     | 25 | 
| en2cn | 43,767 | 120,674 | 35,013 | 4,377 | 4,377 | 52     | 41 | 
