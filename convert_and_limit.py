import pandas as pd
import jsonlines
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
def cut_sentence(sentence):
   return tokenizer.decode(tokenizer.encode(sentence)[1:-1][:tokenizer.max_len_single_sentence-2])


def csv_to_jsonl(csv_file_path, jsonl_file_path):
    # Load the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Open the JSON Lines file for writing
    with jsonlines.open(jsonl_file_path, 'w') as writer:
        # Iterate over the rows in the dataframe
        for _, row in df.iterrows():
            # Extract the text value from the 'text' column
            text = cut_sentence(str(row['text']))

            # Write a dictionary containing the input text to the JSON Lines file
            writer.write({'inputs': text})

# Example usage
csv_file_path = 'category_test.csv'
jsonl_file_path = 'category_test_limited.jsonl'
csv_to_jsonl(csv_file_path, jsonl_file_path)
