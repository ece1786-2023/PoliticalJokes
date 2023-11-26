import argparse
import csv
from openai import OpenAI


class Generator:
    def __init__(self, example_path="data/generator_filtered.csv", example_keyword_path="data/generator_filtered_keywords.csv", 
                 keywords="USSR", output_count=1) -> None:
        # Initialize attributes.
        self.example_path = example_path
        self.example_keyword_path = example_keyword_path
        self.keywords = keywords
        self.output_count = output_count
    
    def __extract_data(self, path) -> list:
        # Helper function for data extraction.
        data_lst = []
        with open(path, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for line in spamreader:
                data_lst.append(line[0])
        return data_lst

    def generate(self) -> list:
        # Create instruction for the language model
        instruction = "### instruction ###\nGenerate a USSR political joke with the keywords given. Pretend its twentieth century and USSR still exists. Use dark humour. Base on the history and don't play on words. Generate the output in one line.\n\n"
        # Extract examples from csv file
        examples = self.__extract_data(self.example_path)
        # Extract keywords from csv file
        keywords = self.__extract_data(self.example_keyword_path)
        # Create prompt
        prompt = instruction + "### examples ###\n"
        for i in range(1, len(keywords)):
            prompt += "Keywords: " + keywords[i] + "\n" + examples[i] + "\n\n"
        # Generate outputs
        client = OpenAI()
        outputs = []
        for i in range(self.output_count):
            completion = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": "Keywords: " + self.keywords}
                    ]
                )
            outputs.append(completion.choices[0].message.content)
        return outputs


def main(args):
    generator = Generator(args.example_path, args.example_keyword_path, args.keywords, args.output_count)
    outputs = generator.generate()
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
    parser.add_argument("--output_count", help="the number of generated jokes", type=int, default=1)
    parser.add_argument("--example_path", help="the path to the generator csv", type=str, default="data/generator_filtered.csv")
    parser.add_argument("--example_keyword_path", help="the path to the generator keywords csv", type=str, default="data/generator_filtered_keywords.csv")
    parser.add_argument("--keywords", help="the keywords for joke generation", type=str, default="USSR")
    parser.add_argument('--save', help='Default is False. When activated, save the output as csv file.', action='store_true')
    parser.add_argument("--save_path", help="the path for the output csv", type=str, default="generator_output/output.csv")
    arguments = parser.parse_args()
    main(arguments)