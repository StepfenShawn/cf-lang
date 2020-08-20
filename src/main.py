# Enemy spotted              :    START
# Reporting in               :    PRINT
# Enemy Down                 :    END
# Fire in the hole           :    exit function
# Keep your fire             :    while
# Hold your fire             :    end while
# wait for my go             :    IF
# Follow me                   :    end assign
# get in position [varname]:[value]   :    assign

# Examples:

# /* PRINT "Hello World" on the screen */
# ENEMY SPOTTED!
#   REPORTING IN ["Hello World"]!
#   FIRE IN THE HOLE!
# ENEMY DOWN!

# /* A +oo Loop! */
# ENEMY SPOTTED!
#   GET IN POSITION [A : 1]!
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
    "ASSIGN"    : "GETINPOSITION",    # GET IN POSITION
    "ENDASSIGN" : "FOLLOWME"          # FOLLOW ME
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
    cf_eval(code)

key = []
value = []

def cf_eval(code):
    global endassign
    if 'assign' in code:
        key.append(code[code.index(code[code.index('(') + 1 : code.index(')')]) : code.index(':')])
        value.append(code[code.index(':') + 1 : code.index(')')])
        code = code[code.index(')') + 1:]
        endassign = True
    
    if not endassign and 'endassign' not in code:
        print("You need soldiers to follow you when you're in position");
        
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
sys.path.insert(0, "../..")

# If a filename has been specified, we try to run it.
def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            code = f.read()
        cf_run(code)

if __name__ == '__main__':
    main()