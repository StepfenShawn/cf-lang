#===============================================
# FILENAME: main.py
# created at 2020/8/18 15:46:04
#===============================================

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

# Examples:

# /* PRINT "Hello World" on the screen */
# ENEMY SPOTTED!
#   REPORTING IN ["Hello World"]!
#   FIRE IN THE HOLE!
# ENEMY DOWN!

# /* A +oo Loop! */
# ENEMY SPOTTED!
#   I AM IN POSITION [A : 1]!
#   FOLLOW ME!
#   REPORTING IN [A]!
#   KEEP YOUR FIRE [A]!
#       REPORTING IN ["Go to hell!"]!
#   HOLD YOUR FIRE!
#   FIRE IN THE HOLE!
# ENEMY DOWN!

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
    code = code.replace("[", "(")
    code = code.replace("]", ")")

    if keyword["PRINT"] in code:
        code = code.replace(keyword["PRINT"] , "print")
    if keyword["EXIT"] in code:
        code = code.replace(keyword["EXIT"], "exit()")
    if keyword["ASSIGN"] in code:
        code = code.replace(keyword["ASSIGN"], "assign")
    if keyword["ENDASSIGN"] in code:
        code = code.replace(keyword["ENDASSIGN"], "endassign")
    if keyword["WHILE"] in code:
        code = code.replace(keyword["WHILE"], "while")
    if keyword["ENDWHILE"] in code:
        code = code.replace(keyword["ENDWHILE"], "endwhi")
    if keyword["IF"] in code:
        code = code.replace(keyword["IF"], "if")
    if keyword["ENDIF"] in code:
        code = code.replace(keyword["ENDIF"], "endif")
    if keyword["ADD"] in code:
        code = code.replace(keyword["ADD"], "add")
    if keyword["SUB"] in code:
        code = code.replace(keyword["SUB"], "sub")
    cf_parse(code)

key = []
value = []

def cf_parse(code):
    # nop
    if 'FIRE' in code:
        code = code.replace("FIRE", "")
    code = code.split("\n")
    for i in range(len(code)):
        cf_eval(code[i], i)

key = []
value = []

def cf_let(var_name, val):
    key.append(var_name)
    value.append(val)

def cf_eval(code, line):
    # Init some var
    while_cond = True
    while_stmt = ""
    end_while = False
    while_start = 0

    end_assign = False
    assign_start = 0

    if 'assign' in code:
        end_assign = True
        assign_start = line
        try:
            cf_let(code[code.index('(') + 1 : code.index(':')], code[code.index(':') + 1 : code.index(')')])
        except Exception:
            pass

    if end_assign and line == assign_start + 1:
        print("Line " + str(line) + ": You need soldiers to follow you when you're in position(No endassign found)")

    if 'while' in code:
        end_while = True
        while_start = line
        try:
            while_cond = bool(int(code[code.index('(') + 1 : code.index(')')]))
        except Exception:
            pass

    if 'print' in code:
        # identifier
        if code[code.index('(') + 1 : code.index(')')].isalpha():
            print(value[key.index(code[code.index('(') + 1 : code.index(')')])])
        # String Or Number
        else:
            eval(code[code.index('print') : code.index(')') + 1])
    if 'exit()' in code:
        eval(code[code.index('exit') : code.index('exit') + len('exit()')])

import sys

# If a filename has been specified, we try to run it.
def main():
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                code = f.read()
            # Skip the comment
            import re
            m = re.compile(r'/\*.*?\*/', re.S)
            code = re.sub(m, ' ', code)
            cf_run(code)
        except FileNotFoundError:
            print("File not found!")

if __name__ == '__main__':
    main()