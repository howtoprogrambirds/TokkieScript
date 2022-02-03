import lexer
from typing import List, Tuple, Type

class P_token:
    def __init__(self, nmbr_line):
        self.nmbr_line = nmbr_line
    def __str__(self):
        return "{}: (line number:{})".format(type(self).__name__, self.nmbr_line)

    def __repr__(self):
        return "<{}> || at linenumber {}".format(type(self).__name__, self.nmbr_line)


class P_exception(Exception):
    pass


class P_function(P_token):
    def __init__(self, identifier: lexer.Var_token, type_func, parameters, body, nmbr_line):
        self.identifier = identifier
        self.type = type_func
        self.parameters = parameters
        self.body = body
        P_token.__init__(self, nmbr_line)

    def __len__(self):
        return len(self.body)
 
    def __str__(self):
        return "{}: [\n-ID of function: \'{}\'\n-{}\n-Parameters: {}\n-{}\n]".format(type(self).__name__, self.identifier.name, self.type, self.parameters, self.body)

    def __repr__(self):
        return "{}: (amount of statements:{})".format(type(self).__name__, len(self))


class P_func_call(P_token):
    def __init__(self, identifier: lexer.Var_token, nmbr_line, arguments=None):
        self.identifier = identifier
        self.arguments = arguments or []
        P_token.__init__(self, nmbr_line)
    
    def __str__(self):
        return_str = "{}:\n\tCalled for function:\'{}\'\n\tWith arguments:\n\t\t".format(type(self).__name__, self.identifier.name)
        if self.arguments:
            for argument in self.arguments[:-1]:
                return_str += "[{}],\n\t\t".format(argument)
            return_str += "[{}]".format(self.arguments[-1])
        return_str += "\n\t---------------------\n\tAt linenumber: {}".format(self.nmbr_line)

        return return_str
    

class P_literal(P_token):
    def __init__(self, value: lexer.Literal_token, nmbr_line):
        self.value = value
        P_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: -| {} |-".format(type(self).__name__, self.value, self.nmbr_line)


class P_body(P_token):
    def __init__(self, statements: List[lexer.Lexer_strct_token], nmbr_line):
        self.statements = statements
        P_token.__init__(self, nmbr_line)

    def __len__(self):
        return len(self.statements)
    
    def __str__(self):
        return_str = "{}:\n - ".format(type(self).__name__)
        if self.statements:
            for statement in self.statements[:-1]:
                return_str += "{}\n - ".format(statement)
            return_str += "{}".format(self.statements[-1])
        return return_str

    def __repr__(self):
        return_str = ""
        if self.statements:
            for statement in self.statements[:-1]:
                return_str += "{}\n".format(statement)
            return_str += "{}".format(self.statements[-1])
        return return_str

def parse_tokenlist(tokens: List[lexer.Lexer_strct_token]):
    assert not len(tokens) == 0, "Can't find any tokens in this tokenlist"

    parsed_tokens, tokens = parse_token(tokens)

    if len(tokens) == 0:
        return [parsed_tokens]
    else:
        return [parsed_tokens] + parse_tokenlist(tokens)
    
def parse_token(tokens: List[lexer.Lexer_strct_token]):
    type_token = type(tokens[0])
    # if it's a literal
    if issubclass(type_token, lexer.Literal_token):
        return P_literal(tokens[0], tokens[0].nmbr_line), tokens[1:]
    # if it's a variable
    elif type_token == lexer.Var_token:
        parsed_var_token, tokens = parse_variable(tokens)
        return parsed_var_token, tokens
    # if it's a function
    elif type_token  == lexer.Func_token:
        parsed_func_token, tokens = parse_function(tokens)
        return parsed_func_token, tokens
    else:
        raise P_exception (
            "unexpected token {}".format(type_token)
        )

def parse_variable(tokens: List[lexer.Lexer_strct_token]):
    temp_var_token = tokens[0]

    #if it's a function call
    if isinstance(tokens[1], lexer.Value_token):
        arguments, tokens = parse_arguments(tokens[1:])
        return P_func_call(temp_var_token, temp_var_token.nmbr_line, arguments), tokens

def parse_arguments(tokens: List[lexer.Lexer_strct_token], arguments=None):
    if arguments == None:
        #parameter_scope_indication, tokens = get_specific_token(tokens, lexer.Parameter_scope_token)
        arguments = []

    if isinstance(tokens[0], lexer.Endline_token):
        return arguments, tokens[1:]
    else:
        argument, tokens = parse_token(tokens)
        if not isinstance(tokens[0], lexer.Endline_token): 
            comma, tokens = get_specific_token(tokens, lexer.Comma_token)
        return parse_arguments(tokens, arguments + [argument])

def parse_function(tokens: List[lexer.Lexer_strct_token]):
    func_id, tokens = get_specific_token(tokens[1:], lexer.Var_token)
    func_type, tokens = parse_function_type(tokens)
    func_para, tokens = parse_function_para(tokens)
    func_body, tokens = parse_body(tokens)

    return P_function(func_id, func_type, func_para, func_body, func_id.nmbr_line), tokens

def parse_function_type(tokens: List[lexer.Lexer_strct_token]):
    _, tokens = get_specific_token(tokens, lexer.Beg_type_token)
    function_type, tokens = get_specific_token(tokens, lexer.Type_token)
    _, tokens = get_specific_token(tokens, lexer.End_type_token)

    return function_type, tokens

def parse_function_para(tokens: List[lexer.Lexer_strct_token]):
    parameter_beg_scope_flag, tokens = get_specific_token(tokens, lexer.Parameter_scope_token, False)
    if parameter_beg_scope_flag:
        parsed_parameters, tokens = get_func_parameters(tokens)
    else:
        parsed_parameters = None

    return parsed_parameters, tokens

def parse_body(tokens: List[lexer.Lexer_strct_token], statements = None):
    if statements == None:
        _, tokens = get_specific_token(tokens, lexer.Beg_scope_token)
        statements = []

    body_end_scope_flag, tokens = get_specific_token(tokens, lexer.End_scope_token, False)
    if body_end_scope_flag:
        return P_body(statements, statements[0].nmbr_line), tokens
    else:
        statement, tokens = parse_token(tokens)
        return parse_body(tokens, statements + [statement])

# STILL IN CONSTRUCTION
#def get_func_parameters(tokens, parameters = None):
#    if parameters == None:
#        parameters = []
#    parameter_variable = get_specific_token(tokens, lexer.Var_token)
#    parameter_type = get_specific_token(tokens, lexer.Type_token)
#    parameters.append((parameter_variable, parameter_type))
#    if type(tokens[0]) == lexer.Comma_token:
#        get_func_parameters(tokens, parameters)
#    elif type(tokens[0]) == lexer.Parameter_scope_token:
#        return tokens, parameters
#    else:
#        raise P_exception(
#            "Error: this is not the correct type token: {} , on line {}".format(type(tokens[0]), tokens[0].nmbr_line)
#        )
    
def get_specific_token(tokens: List[lexer.Lexer_strct_token], searched_type: Type, have_to: bool = True):
    if isinstance(tokens[0], searched_type):
        return tokens[0], tokens[1:]
    elif have_to:
        raise P_exception(
            "the specific token {} is missing, on line {}, found {}".format(searched_type, tokens[0].nmbr_line, type(tokens[0]))
        )
    else:
        return None, tokens
    

with open("../examples/hello_world.txt", "r") as f:
    print("Lexer:")
    hello_word_tokens = lexer.make_tokens(f.read())
    for token in hello_word_tokens:
        print(" -"+str(token))

    print("\nParser:")
    parsed_hello_world_tokens = parse_tokenlist(hello_word_tokens)
    for token in parsed_hello_world_tokens:
        print(token)
