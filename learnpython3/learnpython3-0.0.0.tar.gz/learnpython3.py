dict = ['moive1', 'moive2', 'moive3']

dict.insert(1, 1995)
dict.insert(3, 1994)
dict.append(2009)
print(dict)

for moive in dict:
    print(moive)

nest_dict = ['hello', 'world',['UK', 'England', ['Coventry', 'Birmingham']]]
for item in nest_dict:
    if isinstance(item, list):
        for nested_item in item:
            print(nested_item)
    else:
        print(item)
'''
This is a comment for 
multiple lines
'''
# TODO the default length of recurison is no longer than 100 times
def print_nested_list(nest_list):
    for item in nest_list:
        if isinstance(item, list):
            print_nested_list(item)
        else:
            print(item)

if __name__ == "__main__":
    print_nested_list(nest_dict)