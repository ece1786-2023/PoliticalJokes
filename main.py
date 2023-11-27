from evaluator import Evaluator
from generator import Generator
import gradio as gr

def generate_and_evaluate(keywords):
    # Generate a a Russian political joke.
    generator = Generator(keywords=keywords)
    joke = generator.generate()[0]
    # Evaluate the funniness of the generated joke.
    evaluator = Evaluator()
    rating, explanation = evaluator.evaluate(joke)
    # Build output.
    return "Generated joke:\n{}\n\nRating: {} / 3\n\nExplanation: {}".format(joke, rating, explanation)

if __name__ == "__main__":
    demo = gr.Interface(
        fn=generate_and_evaluate,
        inputs=gr.Textbox(lines=2, placeholder="Input keyword(s) here to generate a Russian political joke!"),
        outputs="text",
        allow_flagging="never"
    )
    demo.launch()