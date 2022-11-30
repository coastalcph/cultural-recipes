## File description
* cn_recipes_only_titles.json (all chinese recipes with only id and tile field)
* en_recipes_only_titles.json (all english recipes with only id and tile field)
* matched_recipes.json (matched results of Chinese and English dataset)
> Please use matched_recipes.json to conduct experiment.

## Field Description
* cn_id : chinese recipe id
* cn_title :  chinese recipe title
* cn_title_translated : chinese recipe title in english
* cn_ingredient : chinese recipe ingredients
* cn_steps : chinese recipe cooking steps
* cn_dish : dishes of the chinese recipe belongs to
* en_id : matched english recipe id
* en_title : matched english recipe title
* en_ingredient : matched english recipe ingredients
* en_steps : matched english recipe cooking steps

## Statistics
(Finished processing 40% of chinese dataset)


| Dataset | Number    |
| ------  | ------    |
| Chinese | 1,479,764 |
| English | 2,231,150 |
| Matched | 11,408    |

## Original Dataset
Chinese: [Google Drive](https://drive.google.com/file/d/16_X3I3mt-eIaVx5g1ZxA0uks_fD_IBiy/view)     

English: [Kaggle.com](https://huggingface.co/datasets/recipe_nlg) 

## Data reading interface

```python
import json
def read_data(file_path):
    with open(file_path, "r") as f:
        ret = []
        for i, item in enumerate(f.readlines()):
            record = json.loads(item)
            ret.append(record)
    return ret
    
file_path = "matched_recipes.json"
data = read_data(file_path) # dict list, keys: see Field Description
```
