Dependencies: torch, transformers, datasets, evaluate

Train  a model with

python train.py --data_path mRecipe_dataset/recipe_match_en2cn/ $DATA_DIR --src_lang en --tgt_lang cn --model_name Helsinki-NLP/opus-mt-en-zh --experiment_name en_cn --lr 1e-4 --do_train

Evaluate a model with

python train.py --data_path mRecipe_dataset/recipe_match_en2cn/ --model_name Helsinki-NLP/opus-mt-en-zh --experiment_name en_cn --lr 1e-4 --do_predict --src_lang en --tgt_lang cn

Use --do_predict_zero_shot to run zero-shot evaluation. With --do_predict, the model finds the best checkpoint based on validation BLEU and uses that for the predictions. 
