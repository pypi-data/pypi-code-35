def Mode_number(List1):
    count_dict = dict()
    for item in List1:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    print(count_dict)
    print(sorted(count_dict.items(),key=lambda  item:item[1]))
    z=list(sorted(count_dict.items(),key=lambda  item:item[1]))
    output = str(z[-1]) + 'The first number is the mode and second number is it\'s frequency'
    return output        




# This function will allow you to input some numbers and then find the most frequent one.
# Our group's package is uploaded in account 4320180939871.





    

    
        
    
    
    
