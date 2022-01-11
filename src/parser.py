from lexer import *
from typing import List, Tuple, Type

class Parser_token:
    def __init__(self, nmbr_line):
        self.nmbr_line = nmbr_line
    def __str__(self):
        return "{}: (line number:{})".format(type(self).__name__, self.nmbr_line)

    def __repr__(self):
        return "<{}>: (line number:{})".format(type(self).__name__, self.nmbr_line)

def eat_token(tokens: List[Lexer_token], type_of_token: Type):
    if len(tokens) == 0:
        return None, tokens
    elif isinstance(tokens[0], type_of_token):
        return tokens[0], tokens[1:]
    else:
        return None, tokens

        
def parse_function(tokens: List[Lexer_token]):
    function_var, tokens = eat_token(tokens[1:], lexer.Var_token)
    parameters, tokens = parse_parameters(tokens)
    
        
def parse_tokens(tokens: List[Lexer_token]) -> List[Parser_token]:

    if len(tokens) == 0:
        return []

    elif tokens[0] == Func_token:
        parse_function
        return parse_tokens(tokens_rest)
    return tokens

with open("../examples/hello_world.txt", "r") as f:
    hello_word_tokens = make_tokens(f.read())
    for token in hello_word_tokens:
        print(token)
    parsed_hello_world_tokens = parse_tokens(hello_word_tokens)
 
