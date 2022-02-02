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
        return "\n{}: [\n-ID of function: \'{}\'\n-{}\n-Parameters: {}\n-{}\n]".format(type(self).__name__, self.identifier.name, self.type, self.parameters, self.body)

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

#def parse_structure_token(tokens: List[lexer.Lexer_strct_token]):
#    assert type(tokens[0]) == lexer.Var_token
#
#    variable = tokens[0].name
#    if variable in diff_var_parsers:
#        return diff_var_parsers[variable](tokens)
#    else:
#        raise P_exception(
#            "the variablename {} is missing".format(variable)
#        )

def parse_var_token(tokens: List[lexer.Lexer_strct_token]):
    variable, tokens = get_specific_token(tokens, lexer.Value_token)
    #print(type(tokens[0]))
    # HINT: the token next to the variable = tokens[0]
    if isinstance(tokens[0], lexer.Value_token):
        parameters, tokens = parse_arguments(tokens)
        variable = P_func_call(variable, variable.nmbr_line, parameters)
    elif isinstance(variable, lexer.Literal_token):
        return P_literal(variable, variable.nmbr_line), tokens

    #print("hoihoi")
    #print(type(variable))
    return variable, tokens
 
diff_token_parser = {
    lexer.Value_token: parse_var_token,
    
}   

def parse_arguments(tokens: List[lexer.Lexer_strct_token], arguments=None):
    if arguments == None:
        #parameter_scope_indication, tokens = get_specific_token(tokens, lexer.Parameter_scope_token)
        arguments = []

    if isinstance(tokens[0], lexer.Endline_token):
        return arguments, tokens[1:]
    else:
        argument, tokens = parse_tokens(tokens)
        if not isinstance(tokens[0], lexer.Endline_token): 
            comma, tokens = get_specific_token(tokens, lexer.Comma_token)
        return parse_arguments(tokens, arguments + [argument])

def get_specific_token(tokens: List[lexer.Lexer_strct_token], searched_type: Type, have_to: bool = True):
    if isinstance(tokens[0], searched_type):
        return tokens[0], tokens[1:]
    elif have_to:
        raise P_exception(
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
    else:
        parameters_of_function = None

    beg_body_token, tokens = get_specific_token(tokens, lexer.Beg_scope_token)
    statements, tokens = get_statements_body(tokens)
    print(function_type)
    return P_function(function_variable_token, function_type, parameters_of_function, statements, function_variable_token.nmbr_line), tokens

def get_statements_body(tokens: List[lexer.Lexer_strct_token], statements = None):
    if statements == None:
        statements = []
    parameter_end_scope_token, tokens = get_specific_token(tokens, lexer.End_scope_token, False)
    if parameter_end_scope_token:
        return P_body(statements, statements[0].nmbr_line), tokens
    else:
        statement, tokens = parse_tokens(tokens)
        return get_statements_body(tokens, statements + [statement])

def parse_tokens(tokens: List[lexer.Lexer_strct_token]):
    type_token = type(tokens[0])
    if issubclass(type_token, lexer.Value_token):
        statement, tokens = parse_var_token(tokens)
        return statement, tokens
    elif type_token  == lexer.Func_token:
        function, tokens = parse_function(tokens)
        return function, tokens
    else:
        raise P_exception (
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
        raise P_exception(
            "Error: this is not the correct type token: {} , on line {}".format(type(tokens[0]), tokens[0].nmbr_line)
        )
    
#def parse_tokens(tokens: List[lexer.Lexer_strct_token]) -> List[P_token]:
#    token_type = type(tokens[0])
#    if token_type == lexer.Func_token:
#        parse_function(tokens)
#        print("a")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.Var_token:
#        print("b")
#        parse_tokens(tokens[1:])
#    elif token_type == lexer.Beg_scope_token:
#        print("c")
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
#    return tokens

with open("../examples/hello_world.txt", "r") as f:
    hello_word_tokens = lexer.make_tokens(f.read())
    for token in hello_word_tokens:
        print(token)
    parsed_hello_world_tokens = parse_tokens(hello_word_tokens)
    for token in parsed_hello_world_tokens:
        print(token)
    print(parsed_hello_world_tokens)
