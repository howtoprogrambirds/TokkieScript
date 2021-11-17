from typing import List, Tuple
import re

class Lexer_token:    
    def __str__(self):
        return "{}".format(type(self).__name__)

    def __repr__(self):
        return "<{}>".format(type(self).__name__)

class Func_token(Lexer_token):
    pass

class Var_token(Lexer_token):
    def __init__(self, prev_name, name = None):
        self.name = name
        self.prev_name = prev_name

    def __str__(self):
        return "{}: (prev name:{} name:{})".format(type(self).__name__ ,\
                                                   self.prev_name, self.name)
    def __repr__(self):
        return "<{}>: (prev name:{} name:{})".format(type(self).__name__ ,\
                                                   self.prev_name, self.name)


def give_first_word(text: str) -> Tuple[str, str]:
   splitted_text = text.split(" ", 1)
   first_word = splitted_text[0]
   rest_string = None
   if (len(splitted_text) == 2):
       rest_string = splitted_text[1]
   
   return first_word, rest_string

#def erase_one_whitespace(text: str) -> str:
#    if len(text) > 0 and text[0].isspace():
#        return erase_one_whitespace(text[1:])
#    return text

def make_tokens(text: str, tokens: List[Lexer_token] = None) -> List[Lexer_token]:
    if tokens == None:
        tokens = []
#    text = erase_one_whitespace(text)
    word = None
    if text != None:
        word, text = give_first_word(text)

    #if tokens != []:
    #    print(type(tokens[-1]), tokens[-1])
    if word == "bekijk":
        tokens.append(Func_token);
        make_tokens(text, tokens)
    elif word == "de" or word == "het" or word == "een":
        tokens.append(Var_token(word))
        make_tokens(text, tokens)
    # make a name for the variable
    elif type(tokens[-1]) == Var_token and tokens[-1].name == None:
        tokens[-1].name = word
        make_tokens(text, tokens)
    elif text == None:
        return tokens
    else:
        print("can't get a token with this word:", word)
        make_tokens(text, tokens)
    return tokens

if __name__ == "__main__":
    with open("../examples/hello_world.txt", "r") as f:
        tokens = make_tokens(f.read())
        print(tokens)
