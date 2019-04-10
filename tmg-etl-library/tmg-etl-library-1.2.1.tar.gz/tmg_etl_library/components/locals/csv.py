from tmg_etl_library.components.locals.local import Local


class CSVClient(Local):
    def __init__(self, log):
        super().__init__(log)

    def get_headers(self):
        pass
        # TODO: Complete

    def merge_csv_files(self, input_file_names, output_file_name, files_have_headers=False):
        """
        Merge multiple csv files into single CSV file.

        :param input_file_names: list of csv files
        :param output_file_name: output file
        :return:
        """

        self.logger.info('Merging CSVs on local to file %s' % output_file_name)
        with open(output_file_name.full_path, 'wt') as outfile:
            # writing the first csv file
            with open(input_file_names[0].full_path, 'rt', encoding="ISO-8859-1") as infile_obj:
                infile = infile_obj.read()
                for line in infile:
                    outfile.write(line)

            # writing other csv files
            for input_file_name in input_file_names[1:]:
                with open(input_file_name.full_path, 'rt', encoding="ISO-8859-1") as infile:
                    if files_have_headers:
                        next(infile)  # skip the header
                    for line in infile:
                        outfile.write(line)

        outfile.close()


class CSVFile:
    # TODO: Discuss, is it better to have one parameter for the full path?
    def __init__(self, name, path, delimiter, quote_char=None):
        self.name = name
        self.path = path
        self.delimiter = delimiter
        self.quote_char = quote_char
        self.full_path = '%s/%s' % (self.path, self.name)
        self.client = None

    def read_data(self, skip_leading_row=False):
        with open(self.full_path, 'rt') as f:
            if skip_leading_row:
                f.__next__()
            data = [line.strip().split(self.delimiter) for line in f]

        return data

    def delete_file(self):
        pass

    def insert_data(self, data, headers, write_headers=False):
        with open(self.full_path, 'wt') as f:
            if write_headers:
                f.write(self.delimiter.join(headers) + '\n')
            for row in data:
                f.write(self.delimiter.join(row) + '\n')
