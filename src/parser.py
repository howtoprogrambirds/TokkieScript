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
    
        
def parse_tokens(tokens: List[lexer.Lexer_token]) -> List[Parser_token]:

    if len(tokens) == 0:
        return []
#<<<<<<< HEAD
#    
#    token_type = type(tokens[0])
#    print(token_type)
#    if token_type == lexer.Func_token:
#        print("a")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.Var_token:
#        print("b")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.Beg_scope_token:
#        print("c")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.Print_token:
#        print("d")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.String_token:
#        print("e")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.Endline_token:
#        print("f")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.End_scope_token:
#        print("g")
#        parse_tokens(tokens[1:])
#=======

    elif tokens[0] == Func_token:
        parse_function
        return parse_tokens(tokens_rest)
    return tokens

with open("../examples/hello_world.txt", "r") as f:
    hello_word_tokens = lexer.make_tokens(f.read())
    for token in hello_word_tokens:
        print(token)
    parsed_hello_world_tokens = parse_tokens(hello_word_tokens)
 
