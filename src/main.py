# ENEMY SPOTTES!                        :    START
# REPORTING IN                          :    PRINT
# MISSION SUCCESS!                           :    END
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

def cf_run(code):
    line = 0
    # Do some syntac check
    if code[:len('DEFENSE POSITION!')] != 'DEFENSE POSITION!':
        print("Error: No main function found!")
        exit()
    if code[-len('MISSION SUCCESS!'):] != 'MISSION SUCCESS!':
        print("Error: No MainEnd found! Mission Failed!")
        exit()
    # Remove the "DEFENSE POSITION!" and "MISSION SUCCESS!"
    code = code[len('DEFENSE POSITION!') : -len('MISSION SUCCESS!')]

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
    print(tokens)
    cf_parser = Parser(tokens, [])
    cf_parser.parse()
    run(cf_parser.Node)

def cf_token(code):
    code = code.replace("FIRE", "")
    keywords = r'(?P<keywords>(print){1}|(exit){1}|(assign){1}|(endass){1}|' \
               r'(while){1}|(endwhi){1}|(if){1}|(fi){1}|(add){1}|(sub){1})'
    op =  r'(?P<op>\+\+|\+=|\+|--|-=|-|\*=|/=|/|%=|%)'
    num = r'(?P<num>\d+)'
    ID =  r'(?P<ID>[a-zA-Z_][a-zA-Z_0-9]*)'
    string = r'(?P<string>\"([^\\\"]|\\.)*\")'
    cond = r'(?P<cond>[<](.*?)[>])'
    patterns = re.compile('|'.join([keywords, ID, num, op, string, cond]))
    for match in re.finditer(patterns, code):
        yield [match.lastgroup, match.group()]

def node_print_new(Node, arg):
    Node.append(["node_print", arg])

def node_let_new(Node, key, value):
    Node.append(["node_let", key, value])

def node_exit_new(Node):
    Node.append(["node_exit"])

def node_sub_new(Node, value):
    Node.append(["node_sub", value])

def node_add_new(Node, value):
    Node.append(["node_add", value])

def node_if_new(Node, cond, stmt):
    Node.append(["node_if", cond, stmt])

def node_loop_new(Node, cond, stmt):
    Node.append(["node_loop", cond, stmt])

class Parser(object):
    def __init__(self, tokens, Node):
        self.tokens = tokens
        self.pos = 0
        self.Node = Node

    def get(self, offset):
        if self.pos + offset >= len(self.tokens):
            return ["", ""]
        return self.tokens[self.pos + offset]

    def last(self, offset):
        return self.tokens[self.pos - offset]
    
    def skip(self, offset):
        self.pos += offset
    
    def match(self, name):
        if self.get(0)[1] == name:
            self.pos += 1
            return True
        else:
            return False
    
    def parse(self):
        while True:
            if self.match("print"):
                node_print_new(self.Node, self.get(0))
                self.skip(1)
            elif self.match("exit"):
                node_exit_new(self.Node)
            elif self.match("add"):
                node_add_new(self.Node, self.get(0))
                self.skip(1)
            elif self.match("sub"):
                node_sub_new(self.Node, self.get(0))
                self.skip(1)
            elif self.match("assign"):
                node_let_new(self.Node, self.get(0), self.get(1))
                self.skip(3) # Skip the key,value, "endass"
            elif self.match("if"):
                cond = self.get(0)
                self.skip(1)
                stmt = []
                while self.tokens[self.pos][1] != 'fi':
                    stmt.append(self.tokens[self.pos])
                    self.pos += 1
                if_node = []
                Parser(stmt, if_node).parse()
                node_if_new(self.Node, cond, if_node)
                self.skip(1)  # Skip the "endif"
            elif self.match("while"):
                cond = self.get(0)
                print(cond)
                self.skip(1)
                stmt = []
                while self.tokens[self.pos][1] != 'endwhi':
                    stmt.append(self.tokens[self.pos])
                    self.pos += 1
                whi_node = []
                Parser(stmt, whi_node).parse()
                node_loop_new(self.Node, cond, whi_node)
                self.skip(1) # Skip the "endwhi"
            else:
                break

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
        if node[0] == "node_if":
            cond = eval(node[1][1].replace("<","").replace(">", ""))
            if cond:
                run(node[2])
        if node[0] == "node_loop":
            cond = eval(node[1][1].replace("<","").replace(">", ""))
            while cond:
                run(node[2])

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