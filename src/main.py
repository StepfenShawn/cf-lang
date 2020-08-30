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
        code = code.replace(keyword["EXIT"], "exit()")
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
    code = code.split("\n")
    codeobj = dict()
    for i in range(len(code)):
        codeobj[str(i)] = code[i]
        cf_eval(codeobj[str(i)], i)

khash = dict()

def cf_let(var_name, val):
    khash[var_name] = val

def cf_var_get(var_name) -> str:
    return khash[var_name]
    

while_run = False
while_start = 0
end_while = False
while_cond = True
while_stmt = []
assign_start = 0
end_assign = False
if_start = 0
end_if = False
if_cond = True
if_run = False
if_stmt = []

def cf_eval(code, line):
    global while_run
    global while_cond
    global while_stmt
    global end_while
    global while_start
    global end_assign
    global assign_start
    global if_start
    global end_if
    global if_cond
    global if_run
    global if_stmt

    # Update var
    if khash != {}:
        for k,v in khash.items():
            exec(k + '=' + str(v))
            
    if 'assign' in code:
        end_assign = True
        assign_start = line
        try:
            cf_let(code[code.index('(') + 1 : code.index(':')], code[code.index(':') + 1 : code.index(')')])
        except Exception:
            pass

    if 'if' in code:
        if_start = line
        if_cond = code[code.index('(') + 1 : code.index(')')]
        if_cond = eval(if_cond)
        end_if = True

    if end_if and line != 0 and not if_run and "fi" not in code:
        if_stmt.append(code)

    if "fi" in code:
        end_if = False
        if if_stmt != []:
            if_run = True
            if if_cond:
                for i in range(1,len(if_stmt)):
                    cf_eval(code[i], i)

    if 'while' in code:
        while_start = line
        while_cond = code[code.index('(') + 1 : code.index(')')]
        while_cond = eval(while_cond)
        end_while = True
    
    if end_while and line != 0 and not while_run and "endwhi" not in code:
        while_stmt.append(code)

    if "endwhi" in code:
        end_while = False
        if while_stmt == []:
            pass
        else:
            while_run = True
            while while_cond:
                for i in range(len(while_stmt)):
                    cf_eval(while_stmt[i], i)

    if 'add' in code:
        val = cf_var_get(code[code.index('(') + 1 : code.index(')')])
        cf_let(code[code.index('(') + 1 : code.index(')')], int(val) + 1)
    if 'sub' in code:
        val = cf_var_get(code[code.index('(') + 1 : code.index(')')])
        cf_let(code[code.index('(') + 1 : code.index(')')], int(val) - 1)
    if 'print' in code:
        exec(code[code.index('print') : code.index(')') + 1])
    if 'exit()' in code:
        exec(code[code.index('exit') : code.index('exit') + len('exit()')])

import sys
sys.setrecursionlimit(10000)

# If a filename has been specified, we try to run it.
def main():
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                code = f.read()
            # Skip the comment
            import re
            code = re.sub(re.compile(r'/\*.*?\*/', re.S), ' ', code)
            cf_run(code)
        except FileNotFoundError:
            print("File not found!")
    else:
        print("Please input your filename!")

if __name__ == '__main__':
    main()