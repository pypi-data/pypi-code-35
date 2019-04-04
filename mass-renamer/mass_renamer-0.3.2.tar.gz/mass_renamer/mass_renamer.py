# Code by mrniceguy127
# github.com/mrniceguy127

import os
import sys
import getopt
import re

def parse_options(options):
    options_dict = {
        "to_replace": '',
        "replace_with": '',
        "path": './',
        "replace_what": 'file',
        "use_regex": False,
        "verbose": False
    }

    for option in options:
        option_name = option[0]
        args = option[:]

        if option_name == '-q':
            options_dict["to_replace"] = args[1]
        elif option_name == '-r':
            options_dict["replace_with"] = args[1]
        elif option_name == '-p':
            options_dict["path"] = args[1]
        elif option_name == '-t':
            options_dict["replace_what"] = args[1]
        elif option_name == '-x':
            options_dict["use_regex"] = True
        elif option_name == '-v':
            options_dict["verbose"] = True

    return options_dict

def get_matching_items(items, options):
    matching_items = []

    if options['use_regex']:
        matching_items = [item for item in items if re.search(options['to_replace'], item)]
    else:
        matching_items = [item for item in items if options['to_replace'] in item]

    return matching_items

def rename_items(items, options):
    items_abs = []
    new_items_abs = []
    curr_item = "NONE"

    try:
        matching_items = get_matching_items(items, options)
        if len(matching_items) > 0:
            print("Renaming file 0/0...\r", end='')
            for i in range(0, len(matching_items)):
                item = matching_items[i]

                if not options["verbose"]:
                    print("Ranaming file %d/%d..." % (i + 1, len(matching_items)), ' ' * 10, '\r',  end='')

                curr_item = os.path.join(os.path.abspath(options["path"]), item)
                abs_path = curr_item
                new_abs_path = ''
                if not options["use_regex"]:
                    new_abs_path = os.path.join(os.path.abspath(options["path"]), item.replace(options["to_replace"], options["replace_with"]))
                else:
                    new_name = re.sub(options["to_replace"], options["replace_with"], item)
                    new_abs_path = os.path.join(os.path.abspath(options["path"]), new_name)

                os.replace(abs_path, new_abs_path)

                if options["verbose"]:
                    print('RENAMED (%d): %s' % (i + 1, abs_path))
                    print('TO:', new_abs_path)

                items_abs.append(abs_path)
                new_items_abs.append(new_abs_path)

            print()
            print('Success!')
        else:
            print("No matching files or directories found.")

    except:
        print("Failed to replace all file/directory names.", "Failed at \"%s\"." % curr_item)
        print("Would you like to return the files to their original names (YES/NO)?")
        answer = ""
        try:
            answer = input()
        except:
            print("Error getting your answer...")
            quit(0)

        valid = False

        while not valid:
            if answer == 'YES':
                valid = True
                i = 0
                try:
                    for item in new_items_abs:
                        curr_item = new_items_abs[i]
                        os.replace(item, items_abs[i])
                        i += 1
                    print("Successfully returned items to their original names!")
                except OSError:
                    print("Failed to return all items to their original names.", "Failed at \"%s\"." % curr_item)
            elif answer == 'NO':
                valid = True
                print("Did not return files to their original names.")
            else:
                print('Invalid response. Please answer "YES" or "NO".')

        quit(0)

def run():
    args = ['-x', '-v', '-q', '-r', '-t', 'p', 'use_regex', 'verbose_logging', 'path', 'query', 'replace_with', 'item_type']
    optlist, args = getopt.getopt(sys.argv[1:], 'xvp:q:r:t:')

    options = parse_options(optlist)

    try:
        files = [f for f in os.listdir(options["path"]) if os.path.isfile(os.path.join(options["path"], f))]
        dirs = [f for f in os.listdir(options["path"]) if os.path.isdir(os.path.join(options["path"], f))]

        if options["replace_what"] == 'file':
            rename_items(files, options)
        elif options["replace_what"] == 'dir':
            rename_items(dirs, options)
        elif options["replace_what"] == 'both':
            rename_items(dirs + files, options)
        else:
            print('Invalid argument "' + options["replace_what"] + '" for option ' + '"-t"' + '.')

    except OSError:
        print('Error accessing the path "' + options["path"] + '".')
        print("Make sure you have proper access rights to this directory and that it exists.")

    print("Exiting...")

if __name__ == "__main__":
    run()
