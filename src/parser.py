import lexer
from typing import List, Tuple, Type

class Parser_token:
    def __init__(self, nmbr_line):
        self.nmbr_line = nmbr_line
    def __str__(self):
        return "{}: (line number:{})".format(type(self).__name__, self.nmbr_line)

    def __repr__(self):
        return "<{}>: (line number:{})".format(type(self).__name__, self.nmbr_line)

class Parser_Exception(Exception):
    pass

class Func_call_token(Parser_token):
    def __init__(self, identifier: lexer.Var_token, arguments=None):
        self.identifier = identifier
        self.arguements = arguments or []
    
#def parse_structure_token(tokens: List[lexer.Lexer_strct_token]):
#    assert type(tokens[0]) == lexer.Var_token
#
#    variable = tokens[0].name
#    if variable in diff_var_parsers:
#        return diff_var_parsers[variable](tokens)
#    else:
#        raise Parser_Exception(
#            "the variablename {} is missing".format(variable)
#        )

def parse_var_token(tokens: List[lexer.Lexer_strct_token]):
    variable, tokens = get_specific_token(tokens, lexer.Var_token)

    # HINT: the token next to the variable = tokens[0]
    if type(tokens[0]) == lexer.Value_token:
        parameters, tokens = parse_arguments(tokens)
        variable = Func_call_token(variable, parameters)
    
    return variable, tokens
 
diff_token_parser = {
    lexer.Var_token: parse_var_token,
}   

def parse_arguments(tokens: List[lexer.Lexer_strct_token], arguments=None):
    if arguments == None:
        #parameter_scope_indication, tokens = get_specific_token(tokens, lexer.Parameter_scope_token)
        arguments = []

    if type(tokens[0]) == lexer.Endline_token:
        return arguments, tokens[1:]
    else:
        argument, tokens = parse_statement(tokens)
        if type(tokens[1]) != lexer.Endline_token:
            comma, tokens = get_specific_token(tokens, lexer.Comma_token)
        return parse_arguments(tokens, parameters + [argument])

def get_specific_token(tokens: List[lexer.Lexer_strct_token], searched_type: Type, have_to: bool = True):
    if type(tokens[0]) == searched_type:
        return tokens[0], tokens[1:]
    elif have_to:
        raise Parser_Exception(
            "the specific token {} is missing, on line {}, found {}".format(searched_type, tokens[0].nmbr_line, type(tokens[0]))
        )
    else:
        return None, tokens
    
def parse_function(tokens: List[lexer.Lexer_strct_token]):
    function_indication_token, tokens = get_specific_token(tokens, lexer.Func_token)
    function_variable_token, tokens = get_specific_token(tokens, lexer.Var_token)
    beg_type_indication, tokens = get_specific_token(tokens, lexer.Beg_type_token)
    function_type, tokens = get_specific_token(tokens, lexer.Type_token)
    end_type_indication, tokens = get_specific_token(tokens, lexer.End_type_token)
   
    parameter_beg_scope_token, tokens = get_specific_token(tokens, lexer.Parameter_scope_token, False)
    if parameter_beg_scope_token:
        parameters_of_function, tokens = get_func_parameters(tokens)
    
    beg_body_token, tokens = get_specific_token(tokens, lexer.Beg_scope_token)
    statements, tokens = get_statements_body(tokens)
   
def get_statements_body(tokens: List[lexer.Lexer_strct_token], statements = None):
    if statements == None:
        statements = []
    parameter_end_scope_token, tokens = get_specific_token(tokens, lexer.End_scope_token, False)
    if parameter_end_scope_token:
        return Statements_body(statements), tokens
    else:
        statement, tokens = parse_statement(tokens)
        return get_statements_body(tokens, statements + [statement])

def parse_statement(tokens: List[lexer.Lexer_strct_token]):
    type_token = type(tokens[0])
    if type_token in diff_token_parser:
        statement, tokens = diff_token_parser[type_token](tokens)
        return statement, tokens
    else:
        raise Parser_Exception (
            "unexpected token {}".format(type_token)
        )
    
def get_func_parameters(tokens, parameters = None):
    if parameters == None:
        parameters = []
    parameter_variable = get_specific_token(tokens, lexer.Var_token)
    parameter_type = get_specific_token(tokens, lexer.Type_token)
    parameters.append((parameter_variable, parameter_type))
    if type(tokens[0]) == lexer.Comma_token:
        get_func_parameters(tokens, parameters)
    elif type(tokens[0]) == lexer.Parameter_scope_token:
        return tokens, parameters
    else:
        raise Parser_Exception(
            "Error: this is not the correct type token: {} , on line {}".format(type(tokens[0]), tokens[0].nmbr_line)
        )
    
def parse_tokens(tokens: List[lexer.Lexer_strct_token]) -> List[Parser_token]:
    token_type = type(tokens[0])
    if token_type == lexer.Func_token:
        parse_function(tokens)
        print("a")
        parse_tokens(tokens[1:])
    elif token_type == lexer.Var_token:
        print("b")
        parse_tokens(tokens[1:])
    elif token_type == lexer.Beg_scope_token:
        print("c")
        parse_tokens(tokens[1:])
    elif token_type == lexer.Print_token:
        print("d")
        parse_tokens(tokens[1:])
    elif token_type == lexer.String_token:
        print("e")
        parse_tokens(tokens[1:])
    elif token_type == lexer.Endline_token:
        print("f")
        parse_tokens(tokens[1:])
    elif token_type == lexer.End_scope_token:
        print("g")
        parse_tokens(tokens[1:])
    return tokens

with open("../examples/hello_world.txt", "r") as f:
    hello_word_tokens = lexer.make_tokens(f.read())
    for token in hello_word_tokens:
        print(token)
    parsed_hello_world_tokens = parse_tokens(hello_word_tokens)
 
