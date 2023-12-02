from openai import OpenAI
import os
import pandas as pd
import utils

class Evaluator:
    def __init__(self, model="gpt-4-1106-preview", temperature=1, top_p=1, verbose=False, log_path="evaluator_output/evaluator_log.txt", example_ids=[2, 10, 38, 42]):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.log_path = log_path
        instruction = "### instruction ###\nAct as a Russian political joke evaluator. Evaluate the funniness with a reason and give an integer rating from 0 to 3, in a format of reason -> rating.\n"
        examples = "### examples ###\n"
        score_to_explanation = {
            3: "This joke is very funny because it is easy to understand and plays on the absurdities and contradictions of the Soviet regime and its leadership -> 3",
            2: "This joke can be rated between 3 and 1 -> 2",
            1: "This joke is too opaque for immediate comedic impact or is just a simple wordplay without meaningful satire against the absurdities under Soviet regime -> 1",
            0: "This is a fact, not a joke -> 0"
        }
        df = pd.read_csv('data/evaluator_filtered.csv')
        for i, id in enumerate(example_ids):
            examples += "Example #" + str(i+1) + "\n<user>: '''" + df.iloc[id,0] + "'''\n<assistant>: '''"
            examples += score_to_explanation[df.iloc[id,2]] + "'''"
            if i != len(example_ids) - 1:
                examples += "\n"
        self.prompt = instruction + examples
        if verbose:
            utils.log("model: " + self.model + ", temperature: " + str(self.temperature) + ", top_p: " + str(self.top_p), self.log_path)
            utils.log("example data ids:" + str(example_ids), self.log_path)
            utils.log("system prompt:\n" + self.prompt, self.log_path)
            utils.log("system prompt tokens:" + str(utils.num_tokens_from_string(self.prompt)), self.log_path)

    def evaluate(self, input, verbose=False):
        client = OpenAI()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": input
                }
            ],
            temperature=self.temperature,
            max_tokens=512,
            top_p=self.top_p,
            frequency_penalty=0,
            presence_penalty=0
        )
        content = response.choices[0].message.content
        rating = int(content[content.find(" -> ") + 4])
        explanation = content[:content.find(" -> ")]
        if verbose:
            print("Rating: " + str(rating))
            print("Explanation: " + explanation)
        return rating, explanation