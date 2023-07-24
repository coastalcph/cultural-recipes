import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process jsonl file to txt format.')
    parser.add_argument('jsonl_file', type=str, help='Input jsonl file path.')
    parser.add_argument('output_file', type=str, help='Output txt file path.')
    parser.add_argument('lang', type=str, help='Language of the input sentences.')
    args = parser.parse_args()

    with open(args.jsonl_file, 'r') as jsonl_file, open(args.output_file, 'w') as txt_file:
        for idx, line in enumerate(jsonl_file):
            data = json.loads(line)
            source = data.get('source', '')
            txt_file.write(f'# ::id {idx}\n')
            txt_file.write(f'# ::snt {source}\n')
            txt_file.write(f'# ::snt_lang {args.lang}\n')
            txt_file.write('(z0 / and)\n\n')  # placeholder

if __name__ == '__main__':
    main()

