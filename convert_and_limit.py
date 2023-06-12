"""
This script is used to preprocess a directory of csv files.
It will trim the length in the text, convert and output them to jsonl files in an output directory

Usage:
python convert_and_limit.py \
--input-dir [INPUT_DIRECTORY] \
--output-dir [OUTPUT_DIRECTORY] \
--num-threads [MUTITHREAD_COUNT, default 5] \
--num-processes [MUTIPROCESS_COUNT, default 4]
"""

from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import os
import time
import pandas as pd
import jsonlines
from transformers import AutoTokenizer
from argparse import ArgumentParser

tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
def cut_sentence(sentence):
    new_tokens = tokenizer.encode(sentence)[1:-1][:tokenizer.max_len_single_sentence-2]
    result = tokenizer.decode(new_tokens)
    
    # In some cases, the re-encoded tokens will have longer length, so we will trim it to make sure everything goes right
    while len(tokenizer.encode(result)) > tokenizer.max_len_single_sentence:
        new_tokens = new_tokens[:-1]
        result = tokenizer.decode(new_tokens)
    return result


def csv_to_jsonl(csv_file_path, jsonl_file_path, chunk_size=1000):
    # Load the CSV file using pandas
    df = pd.read_csv(csv_file_path, chunksize=chunk_size)

    # Open the JSON Lines file for writing
    with jsonlines.open(jsonl_file_path, 'w') as writer:
        # Iterate over the rows in the dataframe
        for chunk in df:
            for _, row in chunk.iterrows():
                # Extract the text value from the 'text' column
                text = cut_sentence(str(row['text']))
                other_values = {key: row[key] for key, _ in row.items() if key != 'text'}

                # Write a dictionary containing the input text to the JSON Lines file
                writer.write({
                    'inputs': text,
                    **other_values
                })

def process_files(arguments, num_threads=5):
    thread_pool = ThreadPool(num_threads)
    thread_pool.starmap(csv_to_jsonl, arguments)

def main(args):
    t0 = time.time()
    os.makedirs(args.output_dir, exist_ok=True)

    process_pool = Pool(args.num_processes)

    arguments = []
    for input_file in os.listdir(args.input_dir):
        print(input_file)
        input_path = os.path.join(args.input_dir, input_file)
        output_path = os.path.join(args.output_dir, f'{os.path.splitext(input_file)[0]}.jsonl')
        arguments.append((input_path, output_path))
    arguments.append(args.chunk_size)

    splited_arguments = list(map(list, zip(*zip(*[iter(arguments)] * args.num_processes)))) if len(arguments) >= args.num_processes else [arguments]
    print("splited_arguments", splited_arguments)
    process_pool.starmap(process_files, [(argument, args.num_threads) for argument in splited_arguments])
    print("Time taken", time.time() - t0)
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input-dir', type=str, help="Input directory that contains the csv files")
    parser.add_argument('--output-dir', type=str, help="Input directory that would contain the resulting jsonl files")
    parser.add_argument('--num-threads', type=int, default=5, help="Number of thread")
    parser.add_argument('--num-processes', type=int, default=4, help="Number of process")
    parser.add_argument('--chunk-size', type=int, default=1000, help="Number of row to lazy load per chunk")
    args = parser.parse_args()
    main(args)