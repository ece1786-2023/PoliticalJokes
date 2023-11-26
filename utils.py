import tiktoken
def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def log(string, file):
    print(string)
    with open(file, "a") as log_file:
        log_file.write(string + "\n")