import pandas as pd
import os
import argparse

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, HfArgumentParser
from transformers.trainer_utils import get_last_checkpoint
from transformers import EarlyStoppingCallback

import wandb
from utils import *

#PAD_TOKEN = '!'
#EOS_TOKEN = '.'
MAX_LENGTH = 512

def get_model_and_auxiliaries(args):

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_name)
    model.config.max_length = MAX_LENGTH

    return model, tokenizer

def get_data(tokenizer, max_length, args):

    train_dataset = TrainDataset(
                           data_path=args.data_path,
                           src_lang=args.src_lang,
                           tgt_lang=args.tgt_lang,
                           split='train',
                           tokenizer=tokenizer,
                           max_input_length=max_length,
                           max_target_length=max_length)
    val_dataset = TrainDataset(
                           data_path=args.data_path,
                           src_lang=args.src_lang,
                           tgt_lang=args.tgt_lang,
                           split='test',
                           tokenizer=tokenizer,
                           max_input_length=max_length,
                           max_target_length=max_length)
    test_dataset = TestDataset(
                           data_path=args.data_path,
                           src_lang=args.src_lang,
                           tgt_lang=args.tgt_lang,
                           split='test',
                           tokenizer=tokenizer,
                           max_input_length=max_length,
                           max_target_length=max_length)

    return train_dataset, val_dataset, test_dataset

def get_best_checkpoint(output_dir):
    last_checkpoint = get_last_checkpoint(output_dir)
    return json.load(open(os.path.join(last_checkpoint, 'trainer_state.json')))['best_model_checkpoint']

def store_results(inputs, predictions, labels, metrics, output_dir, prefix):
    json.dump(metrics, open(os.path.join(output_dir, prefix + 'metrics.json'), 'w'))
    with open(os.path.join(output_dir, prefix + 'preds.jsonl'), 'w') as preds_out:
        for inp, pred, lab in zip(inputs, predictions, labels):
            preds_out.write('{}\n'.format(json.dumps({'source': inp, 'references': lab, 'prediction': pred})))
     
def main(args):

    if args.experiment_name is None:
        args.experiment_name = '{}_{}'.format(args.src_lang, args.tgt_lang, args.lr)
    output_dir = os.path.join(args.experiments_dir, args.experiment_name)
    
    # for prediction
    if os.path.exists(output_dir) and (args.do_predict or args.do_eval):
        args.model_name = get_best_checkpoint(output_dir)
        output_dir = args.model_name

    model, tokenizer = get_model_and_auxiliaries(args)

    # config generation
    model.config.num_beams = 3
    model.config.repetition_penalty = 1.2
    model.config.no_repeat_ngram_size = 5

    train_dataset, val_dataset, test_dataset = get_data(tokenizer, model.config.max_length, args)
   
    report_to = "wandb" if args.do_train else None

    training_args = Seq2SeqTrainingArguments(
        num_train_epochs=args.n_epochs, 
        per_device_train_batch_size=args.batch_size, 
        gradient_accumulation_steps=args.gradient_steps,
        learning_rate =args.lr,
        fp16=True,
        save_strategy="epoch",
        save_total_limit=args.n_epochs, 
        logging_strategy="epoch", 
        evaluation_strategy="epoch",
        predict_with_generate=True,
        metric_for_best_model='eval_bleu',
        greater_is_better=True,
        output_dir=output_dir, 
        overwrite_output_dir=True,
        report_to="wandb",
        load_best_model_at_end = True
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        data_collator=data_collator, 
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        callbacks = [EarlyStoppingCallback(early_stopping_patience=5)],
        compute_metrics=ComputeMetrics(tokenizer)
    )

    if args.do_train:
        wandb.init(project="recipes", entity="yovakem")
        wandb.run.name = args.experiment_name
        trainer.train()
    elif args.do_eval:
        metrics  = trainer.evaluate(val_dataset)
        store_results(None, None, metrics, output_dir, 'val_')
    elif args.do_predict:
        predictions, _, _  = trainer.predict(test_dataset)
        predictions, labels = postprocess_test_data(predictions, test_dataset.targets, tokenizer)
        metrics = compute_test_metrics(predictions, labels)
        store_results(predictions, labels, metrics, output_dir, 'test_')
    elif args.do_predict_zero_shot:
        predictions, _, _  = trainer.predict(test_dataset)
        inputs, predictions, labels = postprocess_test_data(test_dataset.inputs, predictions, test_dataset.targets, tokenizer)
        metrics = compute_test_metrics(predictions, labels)
        store_results(inputs, predictions, labels, metrics, output_dir, 'zero_shot_test_')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Model Training')
    parser.add_argument("--data_path", type=str, help="Path to data")
    parser.add_argument("--src_lang", type=str, help="en or cn")
    parser.add_argument("--tgt_lang", type=str, help="en or cn")

    parser.add_argument("--experiments_dir", type=str, default="experiments/", help="Directory where trained models will be saved")
    parser.add_argument("--experiment_name", type=str, default=None, help="Sub directory where trained models will be saved")

    parser.add_argument("--model_name", type=str, help="Model name")

    parser.add_argument("--do_train", action="store_true", default=False, help="Whether to train model")
    parser.add_argument("--n_epochs", type=int, default=30, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--gradient_steps", type=int, default=4, help="Number of gradient accumulation steps")
    parser.add_argument("--do_eval", action="store_true", default=False, help="Whether to run prediction on val")
    parser.add_argument("--do_predict", action="store_true", default=False, help="Whether to run prediction on test")
    parser.add_argument("--do_predict_zero_shot", action="store_true", default=False, help="Whether to run zero-shot prediction on test")


    args = parser.parse_args()

    main(args)
