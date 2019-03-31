import sys
from uk_postcodes.postcodes import format_postcode,basic_validation,deep_validaion,load_postcodes


if __name__ == '__main__':

    #code = sys.argv[-1]
    code = 'AI2 9AA' # example

    if not code.endswith('.py'):

        # load the pkl file which contains all the postcodes data
        load_postcodes()

        # Call the format_postcode function to print the formatted code of input code
        format_code = format_postcode(code)
        print('The formatted code is', format_code)

        # Call the deep_validation function to validate the code actually exists or not (boolean)
        valid_code = deep_validaion(code)
        print('The code existence and validity is: {}.\n'.format(valid_code))

        # Call the basic_validation to match the code with the regex which follows some rules set for the UK postcodes
        if basic_validation(code):
            print('The following code is valid')
        else:
            print('The code is invalid')
    else:
        print('Please provide a postcode string')