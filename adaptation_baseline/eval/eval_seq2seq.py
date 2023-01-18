import json
import numpy as np
import argparse
from tqdm import tqdm
import evaluate
import re


class Evaluator:
    def __init__(self, lan):
        self.language = lan
        self.bleu = evaluate.load("bleu")
        self.rougeScore = evaluate.load("rouge")
        self.bertScore = evaluate.load("bertscore")
        pass

    def get_corpus_bleu(self, preds, labels, target_lan):
        if target_lan == "en":
            return self.bleu.compute(predictions=preds, references=labels)['bleu']
        elif target_lan == "cn":
            return self.bleu.compute(predictions=[' '.join(list(p)) for p in preds], 
                                     references=[[' '.join(list(l)) for l in label] for label in labels])['bleu']

    def get_roughl(self, preds, labels):
        if self.language == "en":
            return self.rougeScore.compute(predictions=[preds], references=[labels])['rougeLsum']
        elif self.language == "cn":
            return self.rougeScore.compute(predictions=' '.join(list(preds)),
                                           references=[[' '.join(list(item)) for item in labels]])['rougeLsum']

    def get_bert_score(self, preds, labels):
        if self.language == "en":
            return self.bertScore.compute(predictions=preds, references=labels, 
                                               model_type='bert-base-uncased', lang='en', verbose=True)['f1']
        elif self.language == "cn":
            return self.bertScore.compute(predictions=preds, references=labels, 
                                               model_type='bert-base-chinese', lang='cn', verbose=True)['f1']


def evaluate_all(path, evaluator):
    references = []
    recovers = []
    rougel = []
    avg_len = []
    with open(path, 'r') as f:
        cnt = 0
        for row in tqdm(f):
            reference = [item.strip() for item in json.loads(row)['references']]
            recover = json.loads(row)['prediction'].strip()
            recover = recover.replace(args.eos, '').replace(args.sos, '').replace(args.sep, '').replace(args.pad, '')
            avg_len.append(len(recover.split(' ')))
            rougel.append(evaluator.get_roughl(recover, reference))
            recovers.append(recover)
            references.append(reference)
            cnt += 1
    bleu = evaluator.get_corpus_bleu(recovers, references, target_lan)
    bert_score = evaluator.get_bert_score(recovers, references)
    return bleu, rougel, bert_score, avg_len


def extract_componets(content, fields):
    # return content
    components = re.split("Title:|title:|ingredients:|Ingredients:", content)
    # breakpoint()
    # title + ingre + step
    if len(components) > 2:
        title = components[1].strip()
        components_2 = re.split("Steps:|steps:", components[2])
        if len(components_2) > 1:
            ingredient = components_2[0].strip()
            step = components_2[1].strip()
        else:
            ingredient = components_2[0].strip()
            step = ""
    # title + step
    elif len(components) == 2:
        ingredient = ""
        components_2 = re.split("Steps:|steps:|step:|Step:", components[1])
        if len(components_2) > 1:
            title = components_2[0].strip()
            step = components_2[1].strip()
        else:
            title = components[0]
            step = ""
    # title
    else:
        title = ""
        ingredient = ""
        step = ""
    if fields == "title":
        return title
    if fields == "ingredient":
        return ingredient
    if fields == "step":
        return step


def evaluate_component(path, evaluator, fields):
    references = []
    recovers = []
    rougel = []
    avg_len = []
    with open(path, 'r') as f:
        cnt = 0
        for row in tqdm(f):
            reference = [extract_componets(item.strip(), fields) for item in json.loads(row)['references']]
            recover = extract_componets(json.loads(row)['prediction'].strip(), fields)
            recover = recover.replace(args.eos, '').replace(args.sos, '').replace(args.sep, '').replace(args.pad, '')
            avg_len.append(len(recover.split(' ')))
            try:
                rougel.append(evaluator.get_roughl(recover, reference))
            except:
                rougel.append(0.0)
            recovers.append(recover)
            references.append(reference)
            cnt += 1
    bleu = evaluator.get_corpus_bleu(recovers, references, target_lan)
    bert_score = evaluator.get_bert_score(recovers, references)

    return bleu, rougel, bert_score, avg_len


if __name__ == '__main__':
    print("begin")
    parser = argparse.ArgumentParser(description='decoding args.')
    parser.add_argument('--file', type=str, default='', help='path to the folder of decoded texts')
    parser.add_argument('--sos', type=str, default='[CLS]', help='start token of the sentence')
    parser.add_argument('--eos', type=str, default='[SEP]', help='end token of the sentence')
    parser.add_argument('--sep', type=str, default='[SEP]', help='sep token of the sentence')
    parser.add_argument('--pad', type=str, default='[PAD]', help='pad token of the sentence')
    parser.add_argument('--tgt_lan', type=str, default='en', help='target adaptation language')
    parser.add_argument('--component', type=str, default=None, help='target adaptation language')

    args = parser.parse_args()
    path = args.file
    evaluator = Evaluator(args.tgt_lan)
    target_lan = args.tgt_lan
    component = args.component
    if component == None:
        bleu, rougel, F1, avg_len = evaluate_all(path, evaluator)
    else:
        bleu, rougel, F1, avg_len = evaluate_component(path, evaluator, component)
    
    print('*'*30)
    print('BLEU score', bleu)
    print('avg ROUGE-L score', np.mean(rougel))
    print('avg berscore', np.mean(F1))
    print('avg len', np.mean(avg_len))
