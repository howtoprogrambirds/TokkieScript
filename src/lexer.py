from typing import List, Tuple
import re

class Lexer_token:    
    def __init__(self, nmbr_line):
        self.nmbr_line = nmbr_line
    def __str__(self):
        return "{}: (line number:{})".format(type(self).__name__, self.nmbr_line)

    def __repr__(self):
        return "<{}>: (line number:{})".format(type(self).__name__, self.nmbr_line)

class Func_token(Lexer_token):
    pass

class Beg_scope_token(Lexer_token):
    pass

class End_scope_token(Lexer_token):
    pass

class Endline_token(Lexer_token):
    pass

class Beg_type_token(Lexer_token):
    pass

class End_type_token(Lexer_token):
    pass

class Parameter_token(Lexer_token):
    pass

class Parameter_split_token(Lexer_token):
    pass

class String_token(Lexer_token):
    def __init__(self, string_value, nmbr_line):
        self.string_value = string_value
        Lexer_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (string value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.string_value, self.nmbr_line)
    def __repr__(self):
        return "<{}>: (string value:{}, line number:{})".format(type(self).__name__ ,\
                                             self.string_value, self.nmbr_line)
class Var_token(Lexer_token):
    def __init__(self, prev_name, nmbr_line, name = None):
        self.name = name
        self.prev_name = prev_name
        Lexer_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (prev name:{} name:{})".format(type(self).__name__ ,\
                                                   self.prev_name, self.name)
    def __repr__(self):
        return "<{}>: (prev name:{} name:{})".format(type(self).__name__ ,\
                                                   self.prev_name, self.name)
class Class_token(Lexer_token):
    def __init__(self, nmbr_line, name = None):
        self.name = name
        Lexer_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (name:{})".format(type(self).__name__ , self.name)
    def __repr__(self):
        return "<{}>: (name:{})".format(type(self).__name__, self.name)
 
class Type_token(Lexer_token):
    def __init__(self, nmbr_line, type_name):
        self.type_name = type_name
        Lexer_token.__init__(self, nmbr_line)

    def __str__(self):
        return "{}: (type name:{} line number:{})".format(type(self).__name__ ,\
                                                   self.type_name, self.nmbr_line)
    def __repr__(self):
        return "<{}>: (type name:{} line number:{})".format(type(self).__name__ ,\
                                                            self.type_name, self.nmbr_line)
 
class Print_token(Lexer_token):
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
def make_string_token(remnants_of_text: str, string_word: str = None) -> Tuple[str, str]:
    if string_word == None:
        string_word = ""
    if remnants_of_text[0] == "\"":
        print(string_word, " || ", (remnants_of_text[1:]))
        return string_word, remnants_of_text[1:]
    else:
        return make_string_token(remnants_of_text[1:], string_word + remnants_of_text[0])

special_vars = ["Rutte", "Wilder", "Corona"]
types = ["zin", "getal", "waarheid", "lijst"] 

def make_tokens(text: str, tokens: List[Lexer_token] = None, nmbr_line: int = None) -> List[Lexer_token]:
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
        string_literal, text = make_string_token(text[1:])
        tokens.append(String_token(string_literal, nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif text[0] == "\'":
        tokens.append(Parameter_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == "(":
        tokens.append(Beg_type_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == ")":
        tokens.append(End_type_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == ".":
        tokens.append(Endline_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)
    elif text[0] == ",":
        tokens.append(Parameter_split_token(nmbr_line))
        return make_tokens(text[1:], tokens, nmbr_line)


    # WORD ---------------------------------------------------------------
    if text != None:
        word, text = give_first_alpha_word(text)
    print(word)
    #if tokens != []:
    #    print(type(tokens[-1]), tokens[-1])
    if word in special_vars:
        tokens.append(Var_token("NONE", nmbr_line, word))
        return make_tokens(text, tokens, nmbr_line)
    if word in types:
        tokens.append(Type_token(nmbr_line, word))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "bekijk":
        tokens.append(Func_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "de" or word == "het" or word == "een":
        tokens.append(Var_token(word, nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Elitaire" or word == "elitaire":
        tokens.append(Class_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    elif word == "Zeg":
        tokens.append(Print_token(nmbr_line))
        return make_tokens(text, tokens, nmbr_line)
    # make a name for the variable
    if tokens != []:
        if type(tokens[-1]) == Var_token or type(tokens[-1]) == Class_token and tokens[-1].name == None:
            tokens[-1].name = word
            return make_tokens(text, tokens, nmbr_line)
            
    elif text == "":
        return tokens
    elif word == "":
        print("can't get a token with this char:", repr(text[0]))
        return make_tokens(text, tokens, nmbr_line)
    else:
        print("can't get a token with this word:", repr(word))
        return make_tokens(text, tokens, nmbr_line)
    return tokens

if __name__ == "__main__":
    #with open("../examples/hello_world.txt", "r") as f:
    #    hello_word_tokens = make_tokens(f.read())
    #    for token in hello_word_tokens:
    #        print(token)
    
    #with open("../examples/tell_me_your_name.txt", "r") as f:
    #    tmyn_tokens = make_tokens(f.read())
    #    for token in tmyn_tokens:
    #        print(token)

    with open("../examples/classes.txt", "r") as f:
        class_tokens = make_tokens(f.read())
        for token in class_tokens:
            print(token)


