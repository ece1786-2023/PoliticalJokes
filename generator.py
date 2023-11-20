import argparse
import csv
from openai import OpenAI


def extract_data(path):
    # Helper function for data extraction.
    data_lst = []
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for line in spamreader:
            data_lst.append(line[0])
    return data_lst

def main(args):
    # Create instruction for the language model
    instruction = "Generate a USSR political joke with the keywords given. Pretend its twentieth century and USSR still exists. Use dark humour. Base on the history and don't play on words. Generate outputs in one line.\n\n"
    # Extract keywords from csv file
    keywords = extract_data(args.keywords_path)
    # Extract examples from csv file
    examples = extract_data(args.train_path)
    # Create prompt
    prompt = instruction
    for i in range(1, len(keywords)):
        prompt += "Keywords: " + keywords[i] + "\n" + examples[i] + "\n\n"
    # Generate outputs
    client = OpenAI()
    outputs = []
    for i in range(args.output_count):
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "user", "content": "Keywords: " + args.keywords}
                ]
            )
        outputs.append(completion.choices[0].message.content)
    # Save the outputs or print to stdout.
    if args.save:
        with open(args.save_path, 'w', newline='') as csvfile:
            spamWriter = csv.writer(csvfile)
            for output in outputs:
                spamWriter.writerow([output])
    else:
        for output in outputs:
            print(output)

if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_count", help="the number of generated jokes", type=int, default=5)
    parser.add_argument("--train_path", help="the path to the generator csv", type=str, default="data/generator_filtered.csv")
    parser.add_argument("--keywords_path", help="the path to the generator keywords csv", type=str, default="data/generator_filtered_keywords.csv")
    parser.add_argument("--keywords", help="the keywords for joke generation", type=str, default="USSR")
    parser.add_argument('--save', help='Default is False. When activated, save the output as csv file.', action='store_true')
    parser.add_argument("--save_path", help="the path for the output csv", type=str, default="generator_output/output.csv")
    arguments = parser.parse_args()
    network = main(arguments)