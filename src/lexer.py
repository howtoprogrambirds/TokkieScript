from typing import List, Tuple
import re

class Lexer_strct_token:    
    def __init__(self, nmbr_line):
        self.nmbr_line = nmbr_line
    def __str__(self):
        return "{}: (line number:{})".format(type(self).__name__, self.nmbr_line)

    def __repr__(self):
        return "<{}>: (line number:{})".format(type(self).__name__, self.nmbr_line)

class Func_token(Lexer_strct_token):
    pass

class If_token(Lexer_strct_token):
    pass

class Else_token(Lexer_strct_token):
    pass

class Beg_scope_token(Lexer_strct_token):
    pass

class End_scope_token(Lexer_strct_token):
    pass

class Endline_token(Lexer_strct_token):
    pass

class Beg_type_token(Lexer_strct_token):
    pass

class End_type_token(Lexer_strct_token):
    pass

class Beg_array_token(Lexer_strct_token):
    pass

class End_array_token(Lexer_strct_token):
    pass

class Parameter_scope_token(Lexer_strct_token):
    pass

class Comma_token(Lexer_strct_token):
    pass

class While_token(Lexer_strct_token):
    pass

class Return_token(Lexer_strct_token):
    pass

class Constructor_token(Lexer_strct_token):
    pass

class Renew_token(Lexer_strct_token):
    pass

class Operator_token(Lexer_strct_token):
    def __init__(self, operator_type, nmbr_line):
        self.operator_type = operator_type
        Lexer_strct_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (operator type:{}, line number:{})".format(type(self).__name__ ,\
                                             self.operator_type, self.nmbr_line)
    def __repr__(self):
        return "<{}>: (operator type:{}, line number:{})".format(type(self).__name__ ,\
                                             self.operator_type, self.nmbr_line)

class Value_token(Lexer_strct_token):
    pass  

class Literal_token(Value_token):
    pass  

class String_token(Literal_token):
    def __init__(self, string_value, nmbr_line):
        self.string_value = string_value
        Lexer_strct_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (string value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.string_value, self.nmbr_line)
    def __repr__(self):
        return "<{}>: (string value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.string_value, self.nmbr_line)

class Number_token(Literal_token):
    def __init__(self, number_string, nmbr_line):
        self.number_string = number_string
        Lexer_strct_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (number value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.number_string, self.nmbr_line)
    def __repr__(self):
        return "<{}>: (number value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.number_string, self.nmbr_line)

class Bool_token(Literal_token):
    def __init__(self, bool_literal, nmbr_line):
        self.bool_literal = bool_literal
        Lexer_strct_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (bool value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.bool_literal, self.nmbr_line)
    def __repr__(self):
        return "<{}>: (bool value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.bool_literal, self.nmbr_line)

class Var_token(Value_token):
    # Var token can be a name of a function and a value.

    def __init__(self, nmbr_line, name = None):
        self.name = name
        Lexer_strct_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (name:{})".format(type(self).__name__, self.name)
    def __repr__(self):
        return "<{}>: (name:{})".format(type(self).__name__ , self.name)

class Class_token(Lexer_strct_token):
    def __init__(self, nmbr_line, name = None):
        self.name = name
        Lexer_strct_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (name:{})".format(type(self).__name__ , self.name)
    def __repr__(self):
        return "<{}>: (name:{})".format(type(self).__name__, self.name)

class Public_token(Lexer_strct_token):
    pass

class Private_token(Lexer_strct_token):
    pass

class Type_token(Lexer_strct_token):
    def __init__(self, nmbr_line, type_name):
        self.type_name = type_name
        Lexer_strct_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (type name:{} line number:{})".format(type(self).__name__ ,\
                                                   self.type_name, self.nmbr_line)
    def __repr__(self):
        return "<{}>: (type name:{} line number:{})".format(type(self).__name__ ,\
                                                            self.type_name, self.nmbr_line)
 
class Run_token(Lexer_strct_token):
    pass

class Foldl_token(Lexer_strct_token):
    pass

class Foldr_token(Lexer_strct_token):
    pass

def give_first_alpha_word(remnants_of_text: str, alpha_word: str = None) -> Tuple[str, str]:
    if alpha_word == None:
        alpha_word = ""
    #print(repr(remnants_of_text[0]), remnants_of_text[0].isalpha())
    if remnants_of_text[0].isalpha():
        return give_first_alpha_word(remnants_of_text[1:], alpha_word + remnants_of_text[0])
    else:
        return alpha_word, remnants_of_text


# can't be a string with "/" literal.
def split_string_from_text(remnants_of_text: str, string_word: str = None) -> Tuple[str, str]:
    if string_word == None:
        string_word = ""
    if remnants_of_text[0] == "\"":
        print(string_word, " || ", (remnants_of_text[1:]))
        return string_word, remnants_of_text[1:]
    else:
        return split_string_from_text(remnants_of_text[1:], string_word + remnants_of_text[0])

def split_number_from_text(remnants_of_text: str, string_number: str = None, first_digit: bool = True, has_decimal_point: bool = False, minus: bool = False) -> Tuple[str, str]:
    if string_number == None:
        string_number = ""
    if remnants_of_text[0].isdigit():
        return split_number_from_text(remnants_of_text[1:], string_number + remnants_of_text[0], False, has_decimal_point, minus)
    elif remnants_of_text[0] == "." and not first_digit and not has_decimal_point and remnants_of_text[1].isdigit():
        return split_number_from_text(remnants_of_text[1:], string_number + remnants_of_text[0], first_digit, True, minus)
    elif remnants_of_text[0] == "-" and not first_digit and not minus: 
        return split_number_from_text(remnants_of_text[1:], string_number + remnants_of_text[0], first_digit, has_decimal_point, True)
    else:
        return string_number, remnants_of_text


special_vars = ["Rutte", "Wilders", "Corona"]
types = ["zin", "nummer", "waarheid", "onwaarheid", "lijst", "niks"] 
operators = ["plus", "minus", "gedeelt", "maal", "hetzelvde", "niet", 
             "klijner", "minder", "meer", "groter", "is", "maak"]
char_operators = ["+", "-", "/", "*"]

def make_tokens(text: str, tokens: List[Lexer_strct_token] = None, nmbr_line: int = None) -> List[Lexer_strct_token]:
    if tokens == None:
        tokens = []
    if nmbr_line == None:
        nmbr_line = 0

    #CHAR----------------------------------------------------------------
    word = None
    #print(repr(text))
    if text == "":
        return tokens
    elif text[0] == " " or text[0] == "\t":
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == "\n":
        return make_tokens(text[1:], tokens, nmbr_line+1)
    elif text[0] == ":":
        tokens.append(Beg_scope_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == "!":
        tokens.append(End_scope_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == "\"":
        string_literal, text = split_string_from_text(text[1:])
        tokens.append(String_token(string_literal, nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif text[0] == "\'":
        tokens.append(Parameter_scope_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == "(":
        tokens.append(Beg_type_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == ")":
        tokens.append(End_type_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == "[":
        tokens.append(Beg_array_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == "]":
        tokens.append(End_array_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == ".":
        tokens.append(Endline_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == ",":
        tokens.append(Comma_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] in char_operators:
        tokens.append(Operator_token(text[0], nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0].isdigit() or text[0] == "-" and text[1].isdigit():
        number_literal, text = split_number_from_text(text)
        tokens.append(Number_token(number_literal, nmbr_line))
        return make_tokens(text, tokens, nmbr_line)

    # WORD ---------------------------------------------------------------
    if text != None:
        word, text = give_first_alpha_word(text)
    print(word)
    #if tokens != []:
    #    print(type(tokens[-1]), tokens[-1])
    if word in special_vars:
        tokens.append(Var_token(nmbr_line, word))
        return make_tokens(text, tokens, nmbr_line)
    elif word in types:
        tokens.append(Type_token(nmbr_line, word))
        return make_tokens(text, tokens, nmbr_line)
    elif word in operators:
        tokens.append(Operator_token(nmbr_line, word))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "prive":
        tokens.append(Private_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "publiek":
        tokens.append(Public_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Hierbij":
        tokens.append(Constructor_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Bekijk":
        tokens.append(Func_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Als":
        tokens.append(If_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Anders":
        tokens.append(Else_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Totdat":
        tokens.append(While_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Geef":
        tokens.append(Return_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "LekkerLinks":
        tokens.append(Foldl_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "LekkerRechts":
        tokens.append(Foldr_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "en":
        tokens.append(Renew_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "de" or word == "het" or word == "een" \
        or word == "De" or word == "Het" or word == "Een":
        tokens.append(Var_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Elitaire" or word == "elitaire":
        tokens.append(Class_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Zeg":
        tokens.append(Var_token(nmbr_line, word))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Roep":
        tokens.append(Run_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif text == "":
        return tokens
    elif word == "":
        print("can't get a token with this char:", repr(text[0]))
        return make_tokens(text, tokens, nmbr_line)

    # make a name for the variable
    if tokens != []:
        if (type(tokens[-1]) == Var_token and tokens[-1].name == None) or \
                (type(tokens[-1]) == Class_token and tokens[-1].name == None):
            print("CLASS ", tokens[-1].name == None)
            tokens[-1].name = word
            return make_tokens(text, tokens, nmbr_line)

    print("can't get a token with this word:", repr(word))
    return make_tokens(text, tokens, nmbr_line)

if __name__ == "__main__":
    with open("../examples/hello_world.txt", "r") as f:
        hello_word_tokens = make_tokens(f.read())
        for token in hello_word_tokens:
            print(token)
    
    #with open("../examples/tell_me_your_name.txt", "r") as f:
    #    tmyn_tokens = make_tokens(f.read())
    #    for token in tmyn_tokens:
    #        print(token)

    #with open("../examples/classes.txt", "r") as f:
    #    class_tokens = make_tokens(f.read())
    #    for token in class_tokens:
    #        print(token)
    #        if type(token) == Endline_token or type(token) == Beg_scope_token:
    #            print()

    #with open("../examples/go_to_statements.txt", "r") as f:
    #    class_tokens = make_tokens(f.read())
    #    for token in class_tokens:
    #        print(token)
    #        if type(token) == Endline_token or type(token) == Beg_scope_token:
    #            print()

    #with open("../examples/loops.txt", "r") as f:
    #    class_tokens = make_tokens(f.read())
    #    for token in class_tokens:
    #        print(token)
    #        if type(token) == Endline_token or type(token) == Beg_scope_token:
    #            print()
    
    #with open("../examples/double_recursive.txt", "r") as f:
    #    class_tokens = make_tokens(f.read())
    #    for token in class_tokens:
    #        print(token)
    #        if type(token) == Endline_token or type(token) == Beg_scope_token:
    #            print()   

