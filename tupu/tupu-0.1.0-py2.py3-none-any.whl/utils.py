import csv


def load_csv(fn):
    ext = fn.suffix
    delim = ',' if ext == '.csv' else '\t'
    with open(fn) as fh:
        reader = csv.reader(fh, delimiter=delim)
        header = next(reader)
        data = [row for row in reader]
        return header, data


def save_csv(fn, header, data, delimiter):
    with open(fn, 'w', newline='') as fh:
        writer = csv.writer(fh, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(data)


def get_args_from_filename(fn):
    # Allow arguments that change default header names
    # Example: some_fn.csv?lat=latitude&lon=long
    default_args = {'lat':'lat', 'lon':'lon', 'id':'id'}
    if '?' in fn:
        fn, new_args = fn.split('?', maxsplit=1)
        default_args.update(kv.split('=') for kv in new_args.split('&'))
    return fn, default_args


def get_coords(header, data, args):
    lat_i = header.index(args['lat'])
    lon_i = header.index(args['lon'])
    id_i = header.index(args['id'])
    #print(header)
    #print(id_i, lat_i, lon_i)
    coords = [(int(row[id_i]), float(row[lat_i]), float(row[lon_i])) for row in data]
    return coords

