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

import peglet
import re

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
    cf_parse(code)

def cf_parse(code):
    # nop
    if 'FIRE' in code:
        code = code.replace("FIRE", "")
    interpreter = Interpreter()
    interpreter.interpreter(code)

class CFParser(object):
    grammar = r"""
    lines       = _ line _ lines
                | _ line
    line        = num _ stmt                        hug
                | stmt                              hug
    stmt        = print_stmt
                | let_stmt
                | exit_stmt
    exit_stmt   = (exit)
    print_stmt  = (print) _ expr_list
    let_stmt    = (assign) _ var _ (\:) _ expr
                | (assign) _ var _ (\:) _ str
    expr_list   = expr _ , _ expr_list 
                | expr 
                | str _ , _ expr_list
                | str
    expr        = term _ binop _ expr               join
                | term _ relop _ expr               join
                | term
    term        = var
                | num
                | l_paren _ expr _ r_paren          join
    var_list    = var _ , _ var_list
                | var
    var         = ([A-Z])
    str         = " chars " _                       join quote
                | ' sqchars ' _                     join
    chars       = char chars 
                |
    char        = ([^\x00-\x1f"\\]) 
                | esc_char
    sqchars     = sqchar sqchars 
                |
    sqchar      = ([^\x00-\x1f'\\]) 
                | esc_char
    esc_char    = \\(['"/\\])
                | \\([bfnrt])                       escape
    num         = (\-) num
                | (\d+)
    relop       = (<>|><|<=|<|>=|>|=)
    binop       = (\+|\-|\*|\/)
    l_paren     = (\()
    r_paren     = (\))
    _           = \s*
        """
    
    def __init__(self):
        kwargs = {
            "hug"     : peglet.hug,
            "join"    : peglet.join,
            "escape"  : re.escape,
            "quote"   : self.quote,
        }
        self.parser = peglet.Parser(self.grammar, **kwargs)

    def __call__(self, program):
        return self.parser(program)

    def quote(self, toekn):
        return '"%s"' %  toekn

class Interpreter(object):
    def __init__(self):
        self.curr = 0
        self.mem = {}
        self.sysmbols = {}
        self.parser_tree = None
        self.Parser = CFParser()

    def interpreter(self, program):
        self.parser_tree = self.Parser(program)
        for line in self.parser_tree:
           if len(line) > 1:
                head, tail = line[0], line[1:]
                self.mem[head] = tail
        for line in self.parser_tree:
            self.stmt(line)
        self.curr = 0
    
    def stmt(self, stmt):
        head, tail = stmt[0], stmt[1 : ]
        if head == "print":
            self.print_stmt(tail)
        elif head == "exit":
            self.exit_stmt()
        elif head == "assign":
            self.assign_stmt(tail)
    
    def expr_list(self, xs):
        return [self.expr(x) for x in xs]

    def expr(self, x):
        if re.match("^\".*\"$", x):
            return x.replace("\"", "")
        else:
            try:
                return str(eval(x))
            except:
                return x.replace("\"", "")


    def print_stmt(self, content):
        print(" ".join(self.expr_list(content)))
    
    def exit_stmt(self):
        exit()

    def assign_stmt(self, args):
        key, value = args[0], args[2]
        self.sysmbols[key] = self.expr(value)

    def cf_get_var(self, var_name):
        return self.sysmbols[var_name]

# If a filename has been specified, we try to run it.
def main():
    import sys
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