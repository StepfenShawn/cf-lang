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
    "ENDIF"     : "GOGOGO"            # GO!GO!GO!
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
        code = code.replace(keyword["ENDWHILE"], "endwhile")
    if keyword["IF"] in code:
        code = code.replace(keyword["IF"], "if")
    if keyword["ENDIF"] in code:
        code = code.replace(keyword["ENDIF"], "endif")
    cf_eval(code)

key = []
value = []

def cf_eval(code):
    endassign = False
    endwhile = False
    endif = False
    if 'assign' in code:
        key.append(code[code.index(code[code.index('(') + 1 : code.index(')')]) : code.index(':')])
        value.append(code[code.index(':') + 1 : code.index(')')])
        if not endwhile:
            code = code[code.index(')') + 1 : ]
        endassign = True
    
    if endassign and 'endassign' not in code:
        print("You need soldiers to follow you when you're in position")
    
    if 'while' in code:
        endwhile = True
        cond = code[code.index('(') + 1 : code.index(')')]
        code = code[code.index(')') + 1 : ]
        while_block = code[code.index(')') + 1 : code.index('endwhile')]
        print(while_block)
        if code[code.index('(') + 1: code.index(')')].isalpha():
            while bool(value[key.index(cond)]):
                cf_eval(while_block)

    if 'if' in code:
        endif = True
        cond = code[code.index('(') + 1 : code.index(')')]
        code = code[code.index(')') + 1 : ]
        if_block = code[code.index(')') + 1 : code.index('endif')]
        if bool(if_block):
            cf_eval(if_block)
    
    if endif and 'endif' not in code:
        print("Error: Please Go!(No endif foound)")

    if endwhile and 'endwhile' not in code:
        print("You've run out of bullets. Mission failed")
    
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
            cf_run(code)
        except FileNotFoundError:
            print("File not found!")

if __name__ == '__main__':
    main()