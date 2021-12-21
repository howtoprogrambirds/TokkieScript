from lexer import make_tokens, Lexer_token
from typing import List, Tuple

class Parser_token:
    def __init__(self, nmbr_line):
        self.nmbr_line = nmbr_line
    def __str__(self):
        return "{}: (line number:{})".format(type(self).__name__, self.nmbr_line)

    def __repr__(self):
        return "<{}>: (line number:{})".format(type(self).__name__, self.nmbr_line)

        
def parse_tokens(tokens: List[Lexer_token]) -> List[Parser_token]:

    if len(tokens) == 0:
        return []

    return tokens

with open("../examples/hello_world.txt", "r") as f:
    hello_word_tokens = make_tokens(f.read())
    for token in hello_word_tokens:
        print(token)
    parsed_hello_world_tokens = parse_tokens(hello_word_tokens)
 
