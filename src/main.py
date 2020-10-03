# ENEMY SPOTTES!                        :    START
# REPORTING IN                          :    PRINT
# ENEMY DOWN!                           :    END
# FIRE IN THE HOLE                      :    exit function
# KEEP YOUR WHILE                       :    while
# HOLD YOUR FIRE                        :    end while
# WAIT FOR MY GO                        :    IF
# GO!GO!GO!                             :    ENDIF
# I AM IN POSITION [varname]:[value]    :    assign
# FOLLOW ME                             :    end assign
# MOVE ON                               :    ++
# MOVE BACK                             :    --

import re
import sys

keyword = {
    "PRINT"     : "REPORTINGIN",      # REPORTING IN
    "EXIT"      : "FIREINTHEHOLE",    # FIRE YOU GO HOLE
    "ASSIGN"    : "IAMINPOSITION",    # I AM IN POSITION
    "ENDASSIGN" : "FOLLOWME",         # FOLLOW ME
    "WHILE"     : "KEEPYOURFIRE",     # KEEP YOUR FIRE
    "ENDWHILE"  : "HOLDYOURFIRE",     # HOLD YOUR FIRE
    "IF"        : "WAITFORMYGO",      # WAIT FOR MY GO
    "ENDIF"     : "GOGOGO",           # GO! GO! GO!
    "ADD"       : "MOVEON",           # MOVE ON
    "SUB"       : "MOVEBACK"          # MOVE BACK
}
Node = []
def cf_run(code):
    line = 0
    # Do some syntac check
    if code[:len('ENEMY SPOTTED!')] != 'ENEMY SPOTTED!':
        print("Error: Don't panic! No ememy spotted!")
        exit()
    if code[-len('ENEMY DOWN!'):] != 'ENEMY DOWN!':
        print("Error: The enemy was not annihilated! Mission Failed!")
        exit()
    # Remove the "ENEMY SPOTTED!" and "ENEMY DOWN!"
    code = code[len('ENEMY SPOTTED!') : -len('ENEMY DOWN!')]

    # Remove the whitespace
    code = code.replace(" ", "")
    code = code.replace("-", " ")
    code = code.replace("!", "")
    code = code.replace("isnot", "!=")
    code = code.replace("is", "==")
    code = code.replace("[", "(")
    code = code.replace("]", ")")

    if keyword["PRINT"] in code:
        code = code.replace(keyword["PRINT"] , "print")
    if keyword["EXIT"] in code:
        code = code.replace(keyword["EXIT"], "exit")
    if keyword["ASSIGN"] in code:
        code = code.replace(keyword["ASSIGN"], "assign")
    if keyword["ENDASSIGN"] in code:
        code = code.replace(keyword["ENDASSIGN"], "endass")
    if keyword["WHILE"] in code:
        code = code.replace(keyword["WHILE"], "while")
    if keyword["ENDWHILE"] in code:
        code = code.replace(keyword["ENDWHILE"], "endwhi")
    if keyword["IF"] in code:
        code = code.replace(keyword["IF"], "if")
    if keyword["ENDIF"] in code:
        code = code.replace(keyword["ENDIF"], "fi")
    if keyword["ADD"] in code:
        code = code.replace(keyword["ADD"], "add")
    if keyword["SUB"] in code:
        code = code.replace(keyword["SUB"], "sub")
    tokens = []
    for token in cf_token(code):
        tokens.append(token)
    cf_parser(tokens)
    run(Node)

def cf_token(code):
    code = code.replace("FIRE", "")
    keywords = r'(?P<keywords>(print){1}|(exit){1}|(assign){1}|(endass){1}|' \
               r'(while){1}|(endwhi){1}|(if){1}|(fi){1}|(add){1}|(sub){1})'
    op =  r'(?P<op>\+\+|\+=|\+|--|-=|-|\*=|/=|/|%=|%)'
    num = r'(?P<num>\d+[.]?\d+)'
    ID =  r'(?P<ID>[a-zA-Z_][a-zA-Z_0-9]*)'
    string = r'(?P<string>\"([^\\\"]|\\.)*\")'
    cond = r'(?P<cond>[<](.*?)[>])'
    patterns = re.compile('|'.join([keywords, ID, num, op, string, cond]))
    for match in re.finditer(patterns, code):
        yield [match.lastgroup, match.group()]

def node_print_new(arg):
    Node.append(["node_print", arg])

def node_let_new(key, value):
    Node.append(["node_let", key, value])

def node_exit_new():
    Node.append(["node_exit"])

def node_sub_new(value):
    Node.append(["node_sub", value])

def node_add_new(value):
    Node.append(["node_add", value])

def node_if_new(cond, stmt):
    Node.append(["node_if", cond, stmt])

def cf_parser(tokens):
   global Node
   print(tokens)
   for t in tokens:
       if t[0] == 'keywords':
           if t[1] == 'print':
                if tokens[tokens.index(t) + 1][0] == "string" or tokens[tokens.index(t) + 1][0] == "num" or \
                tokens[tokens.index(t) + 1][0] == "ID":
                    node_print_new(tokens[tokens.index(t) + 1])
           if t[1] == 'exit':
               node_exit_new()
           if t[1] == 'assign':
               if tokens[tokens.index(t) + 1][0] == "ID" and (tokens[tokens.index(t) + 2][0] == "num" or \
               tokens[tokens.index(t) + 2][0] == "string"):
                    node_let_new(tokens[tokens.index(t) + 1], tokens[tokens.index(t) + 2])
           if t[1] == 'if':
               stmt = []
           if t[1] == "else":
               pass
           if t[1] == "sub":
               if tokens[tokens.index(t) + 1][0] == "ID":
                    node_sub_new(tokens[tokens.index(t) + 1])
           if t[1] == "add":
               if tokens[tokens.index(t) + 1][0] == "ID":
                    node_add_new(tokens[tokens.index(t) + 1])

def run(Nodes):
    if Nodes == None:
        return None
    for node in Nodes:
        if node[0] == "node_print":
            exec("print(" + node[1][1] + ")")
        if node[0] == "node_let":
            exec(node[1][1] + "=" + node[2][1])
        if node[0] == "node_exit":
            exec("exit(0)")
        if node[0] == "node_sub":
            exec(node[1][1] + "-= 1")
        if node[0] == "node_add":
            exec(node[1][1] + "+= 1")


# If a filename has been specified, we try to run it.
def main():
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                code = f.read()
            # Skip the comment
            code = re.sub(re.compile(r'/\*.*?\*/', re.S), ' ', code)
            cf_run(code)
        except FileNotFoundError:
            print("File not found!")
    else:
        print("Please input your filename!")

if __name__ == '__main__':
    main()