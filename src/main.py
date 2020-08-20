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
#   GET IN POSITION [A]:1!
#   FOLLOW ME!
#   REPORTING IN [A]!
#   KEEP YOUR FIRE [A]!
#       REPORTING IN "Go to hell!"!
#   HOLD YOUR FIRE!
#   FIRE IN THE HOLE!
# ENEMY DOWN!

keyword = {
    "PRINT" : "REPORTINGIN",      # REPORTING IN
    "EXIT"  : "FIREINTHEHOLE"     # FIRE YOU GO HOLE
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
    cf_eval(code)

def cf_eval(code):
    if 'print' in code:
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