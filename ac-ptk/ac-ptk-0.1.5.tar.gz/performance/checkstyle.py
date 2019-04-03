def get_errors_warnings(file: str):
    try:
        html = open(file, 'r')
        html_lines = html.readlines()
        tar_line = ''
        approach = False
        count = 0
        for line in html_lines:
            if approach:
                count += 1
            if count == 3:
                tar_line = line
                break
            if not line.__contains__("<th>Files</th><th>Errors</th>"):
                continue
            else:
                approach = True
        html.close()
        words = tar_line.strip().replace("<td>", ' ').replace("</td>", '').split()
        files = int(words[0].strip())
        errors = int(words[1].strip())
        return "CheckStyle Report: %d files and %d errors" % (files, errors)
    except Exception as e:
        print(e)
    return 'CheckStyle Report: no data'
