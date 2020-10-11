# What is CF-lang
CF-lang is a General Infantry's programming language, Let's kill all the enemy!    
![image](img/special-forces.jpg)  
# Examples
HelloWorld:
```
DEFENSE POSITION!   /* Main begin */
   FIRE!            /* nop */
   REPORTING IN "Hello World"!  /* print "Hello World */
   FIRE IN THE HOLE!  /* exit */
MISSION SUCCESS!    /* Main end */
```
  
endless loop:
```
DEFENSE POSITION!           /* Main begin */
   FIRE!                    /* nop */
   I AM IN POSITION A : 1!  /* A = 1 */
   FOLLOW ME!               /* end assign */
   REPORTING IN A!          /* print A */
   KEEP YOUR FIRE <A>!      /* while A */
       REPORTING IN "Go-to-hell!"!     /* print "Go-to-hell" */
   HOLD YOUR FIRE!          /* end while */
   FIRE IN THE HOLE!        /* exit */
MISSION SUCCESS!            /* Main end */
```
FizzBuzz:
```
DEFENSE POSITION!        /* Main begin */
    FIRE!                /* nop */
    I AM IN POSITION A : 0!   /* A = 0 */
    FOLLOW ME!           /* end assign */
    KEEP YOUR FIRE <A <= 100>!   /* while A <= 100 */
        WAIT FOR MY GO <A % 3 == 0>!    /* if A % 3 == 0 */
            REPORTING IN "Fizz"!        /* print "Fizz" */
        GO!GO!GO!                       /* end if */
        WAIT FOR MY GO <A % 5 == 0>!    /* if A % 5 == 0 */
            REPORTING IN "Buzz"!        /* print "Buzz" */
        GO!GO!GO!                       /* end if */
        MOVE ON A!         /* A -= 1 */
    HOLD YOUR FIRE!        /* end while */
    FIRE IN THE HOLE!      /* exit */
MISSION SUCCESS!         /* Main end */
```
#### Try more [examples](examples)!

`DEFENSE POSITION!`: MAIN BEGIN  
`MISSION SUCCESS!`:  MAIN END  
`REPORTING IN`: PRINT FUNCTION  
`FIRE IN THE HOLE`: EXIT FUNCTION  
`KEEP YOUR FIRE`: WHILE  
`HOLD YOUR FIRE`: END WHILE  
`WAIT FOR MY GO`: IF  
`GO! GO! GO!`: ENDIF  
`I AM IN POSITION [varname]:[value]`: ASSIGN  
`FOLLOW ME`: END ASSIGN  
`MOVE ON` : ++  
`MOVE BACK`: --  
`FIRE`: NOP

# How to run?
```
cd src/
python main.py [-filepath]
```

## TODOs
* Support function define
* Add `ElseIf stmt`
* Support `For Loop`

## Contributing
Welcome to pull a request or open a issue!

## LICENSE
MIT LICENSE

## The Author
CF-lang was designed and developed by [Stepfen Shawn](https://github.com/StepfenShawn) in 2020.