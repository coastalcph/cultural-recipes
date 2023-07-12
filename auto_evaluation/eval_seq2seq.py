import json
import os

import numpy as np
import argparse
from tqdm import tqdm
import evaluate
import re
import jieba
import sacrebleu
from prettytable import PrettyTable

class Evaluator:
    def __init__(self, lan):
        self.language = lan
        self.sacrebleu = sacrebleu.corpus_bleu
        self.chrf = sacrebleu.corpus_chrf
        self.rougeScore = evaluate.load("rouge")
        self.bertScore = evaluate.load("bertscore")
        pass

    def get_sacrebleu(self, preds, labels):
        return self.sacrebleu(preds, labels).score

    def get_chrf(self, preds, labels):
        return self.chrf(preds, labels).score

    def get_roughl(self, preds, labels):
        if self.language == "en":
            return self.rougeScore.compute(predictions=[preds], references=[labels])['rougeLsum']
        elif self.language == "cn":
            return self.rougeScore.compute(predictions=[' '.join(list(preds))],
                                           references=[[' '.join(list(item)) for item in labels]],
                                           tokenizer=lambda x: x.split(" "))['rougeLsum']

    def get_bert_score(self, preds, labels):
        if self.language == "en":
            return self.bertScore.compute(predictions=preds, references=labels,
                                          model_type='bert-base-uncased', lang='en', verbose=True)['f1']
        elif self.language == "cn":
            return self.bertScore.compute(predictions=preds, references=labels,
                                          model_type='bert-base-chinese', lang='cn', verbose=True)['f1']

def stripping_headings(r):
    r = r.replace('Title:', '').replace('Ingredients:', '').replace('Steps:', '')
    r = r.replace('title:', '').replace('ingredients:', '').replace('steps:', '')
    r = r.replace('標題:', '').replace('原料:', '').replace('腳步:', '')
    return r

def tokenize(r, tgt_lan):
    if tgt_lan == 'cn':
        r = list(jieba.cut(r, cut_all=False))
    else:
        r = r.split()
    return ' '.join(r)

def evaluate_all(path, evaluator, strip_headings):
    references = []
    references_tok = []
    recovers = []
    recovers_tok = []
    rougel = []
    avg_len_recover = []
    avg_len_reference = []
    with open(path, 'r') as f:
        cnt = 0
        for row in f:
            row = json.loads(row)
            reference = [item.strip() for item in row['references']]
            recover = row['prediction'].strip()
            if strip_headings:
                reference = [stripping_headings(r) for r in reference]
                recover = stripping_headings(recover)
            recover = recover.replace(args.eos, '').replace(args.sos, '').replace(args.sep, '').replace(args.pad, '')
            recover_tok = tokenize(recover, target_lan)
            reference_tok = [tokenize(r, target_lan) for r in reference]
            avg_len_recover.append(len(recover_tok.split()))
            avg_len_reference+=[len(r.split()) for r in reference_tok]
            rougel.append(evaluator.get_roughl(recover_tok, reference_tok))
            recovers.append(recover)
            recovers_tok.append(recover_tok)
            references.append(reference)
            references_tok.append(reference_tok)
            cnt += 1
    sacrebleu_score = evaluator.get_sacrebleu(recovers_tok, references_tok)
    chrf_score = evaluator.get_chrf(recovers_tok, references_tok)
    bert_score = evaluator.get_bert_score(recovers, references)
    return sacrebleu_score, chrf_score, rougel, bert_score, avg_len_recover, avg_len_reference


if __name__ == '__main__':
    print("-"*30, " Begin Evaluation ", "-"*30)
    parser = argparse.ArgumentParser(description='decoding args.')
    parser.add_argument('--folder', type=str, default='', help='path to the jsonl file of decoded texts')
    parser.add_argument('--file', type=str, default=None, help='path to the jsonl file of decoded texts')
    parser.add_argument('--sos', type=str, default='[CLS]', help='start token of the sentence')
    parser.add_argument('--eos', type=str, default='[SEP]', help='end token of the sentence')
    parser.add_argument('--sep', type=str, default='[SEP]', help='sep token of the sentence')
    parser.add_argument('--pad', type=str, default='[PAD]', help='pad token of the sentence')
    parser.add_argument('--tgt_lan', type=str, default='en', help='target adaptation language')
    parser.add_argument('--component', type=str, default=None, help='target adaptation language')
    parser.add_argument('--strip_heading', type=bool, default=False, help='')

    args = parser.parse_args()
    if args.file:
        paths = [os.path.join(args.folder, args.file)]
    else:
        filename = os.listdir(args.folder)
        paths = [os.path.join(args.folder, f) for f in filename]

    for path in paths:
        print("we are evaluating ", path)
        if args.strip_heading: print('without headings')

        if '2cn' in path and args.tgt_lan != 'cn':
            print('!'*100)
            print('You seem to be evaluating a file with Chinese targets but tgt_lan is not set to cn - please fix')
            exit()

        evaluator = Evaluator(args.tgt_lan)
        target_lan = args.tgt_lan
        component = args.component
        sacrebleu_score, chrf_score, rougel, F1, avg_len_recover, avg_len_reference = evaluate_all(path, evaluator, args.strip_heading)
        ret_table = PrettyTable()
        ret_table.field_names = ["sacreBLEU", "ChrF", "ROUGE-L", "BERTScore", "avg_len_recover"]
        ret_table.add_row([sacrebleu_score, chrf_score, np.mean(rougel)*100, np.mean(F1)*100, np.mean(avg_len_recover)])
        ret_table.float_format = ".2"
        print(ret_table)
