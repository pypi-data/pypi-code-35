# nusplit_stringhell.py
# version 1.0
# Josh Prakke
# Description: A simple script to 
# make your text meme appropriate
# ie: iN a Nusplit_stringHeLl 

import pyperclip as pc
import text

print(text.intro)

img = Image.open("images/mEme.jpg")
img.show()

def meme():
    """ Makes user input into nutshell text """

    counter = 1
    user_input = input("What would you like put in a nutshell? ")
    input_split = list(user_input.lower())
    split_string = []

    for i in input_split:
        if counter % 2 != 0:
            split_string.append(i)
        elif counter % 2 == 0:
            split_string.append(i.upper())
        counter += 1    

    output ="".join(split_string)

    print(f"Someone: \"{user_input}\"")
    print(f"Me: {output}")

    copy_query = input(text.copy_it).lower()

    while copy_query != "y" or copy_query != "n":
        if copy_query == "y":
            print(f"Copied \"{output}\".")
            pc.copy(output)
            copy_query = ""
            break
        elif copy_query == "n":
            copy_query = ""
            break
        else:
            copy_query = input(text.copy_it).lower()

meme()

restart = input(text.restart_it).lower()
while restart != "y" or restart != "n":
    if restart == "y":
        restart = ""
        meme()
    elif restart == "n":
        restart = ""
        print(text.outro)
        break
    else:
        restart = input(text.restart_it).lower()
