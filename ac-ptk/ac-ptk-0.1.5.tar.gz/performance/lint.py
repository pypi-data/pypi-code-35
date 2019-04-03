def get_errors_warnings(file: str):
    try:
        html = open(file, 'r')
        html_lines = html.readlines()
        tar_line = ''
        for line in html_lines:
            if not line.__contains__("Lint Report:"):
                continue
            else:
                tar_line = line
                break
        html.close()
        words = tar_line.strip().split(">")[1].strip().split("<")[0]
        return words
    except Exception as e:
        print("get_errors_warnings: ", e)
    return 'Lint Report: no data'
