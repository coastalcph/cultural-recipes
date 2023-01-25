from torch.utils.data import Dataset
import evaluate
from datasets import load_metric
import numpy as np
import torch
import json

def extract_txt(data_path, split='train'):
    def format_recipe(recipe):
        template = 'Title: {}, Ingredients: {}, Steps: {}'
        ingredients = ' '.join(recipe['ingredients'])
        steps = ' '.join(recipe['steps'])
        return template.format(recipe['title'], ingredients, steps)
    data = [json.loads(l) for l in open(data_path+'/{}.jsonl'.format(split))]
    data = [(format_recipe(item['source']), format_recipe(target)) for item in data for target in item['targets']]
    with open(data_path+'/{}.txt'.format(split), 'w') as f:
        f.write('\n'.join(data))

class TrainDataset(Dataset):
    def __init__(self, data_path, src_lang, tgt_lang, split, tokenizer, max_input_length, max_target_length):
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length 
        
        data = [json.loads(l) for l in open(data_path+'/{}.jsonl'.format(split))]
        self.data = [(item['source'], target) for item in data for target in item['targets']]
        
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang

    def format_recipe(self, title, ingredients, steps):
        template = 'Title: {}, Ingredients: {}, Steps: {}'
        ingredients = ' '.join(ingredients)
        steps = ' '.join(steps)
        return template.format(title, ingredients, steps)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        inputs = self.format_recipe(self.data[idx][0]['title'],
                                    self.data[idx][0]['ingredients'],
                                    self.data[idx][0]['steps'])
        targets = self.format_recipe(self.data[idx][1]['title'],
                                    self.data[idx][1]['ingredients'],
                                    self.data[idx][1]['steps'])

        model_inputs = self.tokenizer(inputs, max_length=self.max_input_length, truncation=True)
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(targets, max_length=self.max_target_length, truncation=True)
        model_inputs["labels"] = labels["input_ids"]

        return model_inputs

class TestDataset(Dataset):
    def __init__(self, data_path, src_lang, tgt_lang, split, tokenizer, max_input_length, max_target_length):
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length

        self.data = [json.loads(l) for l in open(data_path+'/{}.jsonl'.format(split))]

        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.inputs = []
        self.targets = []

    def format_recipe(self, title, ingredients, steps):
        template = 'Title: {}, Ingredients: {}, Steps: {}'
        ingredients = ' '.join(ingredients)
        steps = ' '.join(steps)
        return template.format(title, ingredients, steps)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        inputs = self.format_recipe(self.data[idx]['source']['title'],
                                    self.data[idx]['source']['ingredients'],
                                    self.data[idx]['source']['steps'])
        targets = [self.format_recipe(target['title'],
                                      target['ingredients'],
                                      target['steps']) for target in self.data[idx]['targets']]

        model_inputs = self.tokenizer(inputs, max_length=self.max_input_length, truncation=True)
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(targets[0], max_length=self.max_target_length, truncation=True)
        model_inputs["labels"] = labels["input_ids"]

        self.inputs.append(inputs)
        self.targets.append(targets)

        return model_inputs

def postprocess_text(preds, labels, tokenizer):
    if isinstance(preds, tuple):
        preds = preds[0]
    preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    # Some simple post-processing
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]
    return preds, labels

def postprocess_test_data(inputs, preds, labels, tokenizer):
    if isinstance(preds, tuple):
        preds = preds[0]
    preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    inputs = [inp.strip() for inp in inputs]
    labels = [[l.strip() for l in label] for label in labels]
    return inputs, preds, labels

def compute_test_metrics(preds, labels):
    bleu = evaluate.load("bleu")
    return bleu.compute(predictions=preds, references=labels)

class ComputeMetrics():
    def __init__(self, tokenizer):
        self.metric = load_metric("sacrebleu")
        self.tokenizer = tokenizer

    def __call__(self, eval_preds):
        preds, labels = eval_preds
        decoded_preds, decoded_labels = postprocess_text(preds, labels, self.tokenizer)
        result = self.metric.compute(predictions=decoded_preds, references=decoded_labels)
        result = {"bleu": result["score"]}
        prediction_lens = [np.count_nonzero(pred != self.tokenizer.pad_token_id) for pred in preds]
        result["gen_len"] = np.mean(prediction_lens)
        result = {k: round(v, 4) for k, v in result.items()}
        return result
