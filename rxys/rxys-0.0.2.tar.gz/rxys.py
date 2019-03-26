#!usr/bin/env python

# This is the "nester.py" module, it provides one function called print_lol() which may or may not include nested lists

movies = ['The Holy Grail', 'Life of Brian', 'The Meaning of Life']

cast = ['Cleese', 'Palin', 'George', 'Idle']

names = ['Michael', 'Terry']

""" 
    def print_lol(): #lol stands for list of list
        #docstring here
        #function definition here
        #return not required, task is output
"""


def print_lol(the_list): 
    """
       This function takes a positional argument called "the_list", which is any 
       Python list (of, possibly, nested lists). Each data item in the provided list
       is (recursively) printed to the screen on its own line.
    """     
    for each_item in the_list:    
        if isinstance(each_item, list):
           print_lol(each_item)
        else:
           print each_item

if __name__ == '__main__':

    # we put all our function calls over here.

    print(movies[1])
    print(cast)
    print(len(cast))
    print(cast[1])

    cast.append('Gilliam')
    cast.pop()
    cast.extend(['Gilliam', 'Chapman']
    print(cast)

    cast.remove("Chapman")
    print(cast)
    cast.insert(0, "Chapman)
    print(cast)

    isinstance(name, list) #True
    
    num_names = len(names) #numeric value

    isinstance(num_names, list) #False

    nested_list = [
        "The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
            ["Graham Chapman",
                ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]
    ]

    print_lol(nested_list)

#src: Lists are like arrays, page 9-10, HFP by Paul Barry, O'Reilly

# This demo file was made to be presented on Friday, 22/2/19 

#Please read the external README.md file for details   