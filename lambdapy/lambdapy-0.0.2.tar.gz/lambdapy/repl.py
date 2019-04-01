from lambdapy.core import lambdapy, assign, LambdaPySyntaxError
import tatsu
import tatsu.exceptions
import re

lambda_ascii = """
\033[35m __\033[0m 
\033[35m \ \\\033[0m      LambdaPy Interactive shell 
\033[35m  ⟩ \\\033[0m      type \033[36m.help\033[0m for help
\033[35m / ^ \\\033[0m      type \033[36m.quit\033[0m to exit
\033[35m/_/ \_\\\033[0m
"""

help_ascii = """
forms of lambda terms:
   \033[31mx\033[0m - variable 
   \033[31m(λx.E)\033[0m - lambda abstraction where x is a variable and E is a lambda term
   \033[31m(E₁ E₂)\033[0m - application where E₁ and E₂ are lambda terms
   
\033[36m.help\033[0m to display this message, \033[36m.quit\033[0m to quit
"""

assignment = re.compile(r"^([^\\\.\(\)\s\n\tλ,=]+)[\s\t]*=[\s\t]*(.+)")


def mainloop(prompt=">>> "):
    while True:
        try:
            command = input(prompt)
            if not command:
                continue
            elif command.rstrip() == ".help":
                print(help_ascii)
                continue
            elif command.rstrip() == ".quit":
                return
            else:
                try:
                    assg = assignment.match(command)
                    if assg:
                        expr = lambdapy(assg.group(2))
                        assign(assg.group(1), expr)
                    else:
                        expr = lambdapy(command)
                    expr.display()
                except LambdaPySyntaxError as e:
                    print("\033[31msyntax error: " + str(e) + "\033[0m")
        except KeyboardInterrupt:
            print()
            return


def repl(prompt=">>> "):
    print(lambda_ascii)
    mainloop(prompt)
    print("\033[31mgoodbye.\033[0m")