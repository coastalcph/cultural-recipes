import json
import numpy as np
import argparse
from tqdm import tqdm
import evaluate
import re
import jieba 

class Evaluator:
    def __init__(self, lan):
        self.language = lan
        self.bleu = evaluate.load("bleu")
        self.rougeScore = evaluate.load("rouge")
        self.bertScore = evaluate.load("bertscore")
        pass

    def get_corpus_bleu(self, preds, labels, target_lan):
        return self.bleu.compute(predictions=preds, references=labels)['bleu']

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
        for row in tqdm(f):
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
    bleu = evaluator.get_corpus_bleu(recovers_tok, references_tok, target_lan)
    bert_score = evaluator.get_bert_score(recovers, references)
    return bleu, rougel, bert_score, avg_len_recover, avg_len_reference


def extract_componets(content, fields):
    # return content
    components = re.split("标题|Title:|title:|ingredients:|Ingredients:", content)
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
    references_tok = []
    recovers = []
    recovers_tok = []
    rougel = []
    avg_len = []
    with open(path, 'r') as f:
        cnt = 0
        for row in tqdm(f):
            reference = [extract_componets(item.strip(), fields) for item in json.loads(row)['references']]
            reference_tok = [tokenize(r, target_lan) for r in reference]
            recover = extract_componets(json.loads(row)['prediction'].strip(), fields)
            recover = recover.replace(args.eos, '').replace(args.sos, '').replace(args.sep, '').replace(args.pad, '')
            recover_tok = tokenize(recover, target_lan)
            avg_len.append(len(recover_tok.split(' ')))
            # breakpoint()
            try:
                rougel.append(evaluator.get_roughl(recover_tok, reference_tok))
            except:
                rougel.append(0.0)
            recovers.append(recover)
            recovers_tok.append(recover_tok)
            references.append(reference)
            references_tok.append(reference_tok)
            cnt += 1
    breakpoint()
    bleu = evaluator.get_corpus_bleu(recovers_tok, references_tok, target_lan)
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
    parser.add_argument('--strip_heading', type=bool, default=False, help='')

    args = parser.parse_args()
    path = args.file
    print("we are evaluating ", path)
    if args.strip_heading: print('without headings')

    if '2cn' in args.file and args.tgt_lan != 'cn':
        print('!'*100)
        print('You seem to be evaluating a file with Chinese targets but tgt_lan is not set to cn - please fix')
        exit()

    evaluator = Evaluator(args.tgt_lan)
    target_lan = args.tgt_lan
    component = args.component
    if component == None:
        bleu, rougel, F1, avg_len_recover, avg_len_reference = evaluate_all(path, evaluator, args.strip_heading)
    else:
        bleu, rougel, F1, avg_len_recover, avg_len_reference = evaluate_component(path, evaluator, component)

    print('*' * 30)
    print('BLEU score', bleu)
    print('avg ROUGE-L score', np.mean(rougel))
    print('avg berscore', np.mean(F1))
    print('avg len references', np.mean(avg_len_reference))
    print('avg len prediction', np.mean(avg_len_recover))
