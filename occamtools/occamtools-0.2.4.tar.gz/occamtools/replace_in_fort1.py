import os


def replace_in_fort1(input_file, output_path, **kwargs):
    if (output_path is None) or (output_path == ''):
        output_path = os.path.join(os.path.dirname(input_file),
                                   input_file + '_new')

    keys = list(kwargs.keys())
    values = [kwargs[k] for k in keys]
    with open(input_file, 'r') as in_file, open(output_path, 'w') as out_file:
        next_replace = False
        replace_index = None

        for line in in_file:
            if not next_replace:
                out_file.write(line)
                matches = [k in line for k in keys]
                if any(matches):
                    next_replace = True
                    replace_index = matches.index(True)
            else:
                out_file.write(str(values[replace_index]) + '\n')
                next_replace = False
                replace_index = None
    return output_path
