import base64
import csv
import datetime
import getpass
import json
import os
import pickle
import secrets
import string
import sys
from time import sleep

import pyperclip
from passlib.hash import pbkdf2_sha256 as p_hash
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def setup():
    # Welcome, Instructions
    print('    ***************************\n' +
          '    SimplePass Password Manager\n' +
          '    ***************************\n')
    # Select Master Password
    create_master()
    mydict = {"passwords": []}
    with open(directory('') + 'store.json', 'w', encoding='utf-8') as f:
        json.dump(mydict, f)
    # TODO Import passwords here


def create_folders():

    """
    Ensure that Program folders are available and created in the
    users home directory.
    """

    try:
        os.mkdir(directory(''))
    except OSError:
        print("Creation of the directory %s failed" % directory(''))
    else:
        print("Successfully created the directory %s " % directory(''))
        os.mkdir(directory('import'))
        os.mkdir(directory('export'))


def get_print(text):
    get_version()
    if check:
        print(text)
    else:
        pass


def get_user():
    return getpass.getuser()


def get_version():
    v = sys.version_info[:2]
    if v >= (3, 0):
        check = True
    else:
        check = False
    return check


def directory(folder):
    dir_ = os.path.expanduser('~') + '/SimplePass/'
    if folder:
        if folder == 'import':
            d = dir_ + 'import/'
        elif folder == 'export':
            d = dir_ + 'export/'
        else:
            d = dir_
        dir_ = d
    return dir_


def salt1():
    salt1 = b'EC6873C47AD2F3FABCCC62AF564996F3F84ECD446433DDE'
    return salt1


"""
        Import / Export
"""


def getfieldnames(path):
    with open(path, newline='', encoding='utf-8') as f:
        csv_header = csv.reader(f)
        header = next(csv_header)
        mylist = []

    for index, item in enumerate(header, 1):
        myitem = {index: item}
        mylist.append(myitem)


def save_import(import_list):
    with open(directory('') + 'store.json', 'r') as f:
        store_dict = json.load(f)
    mylist = []
    passlist = store_dict['passwords']
    for s in passlist:
        mylist.append(s)
    for count, s in enumerate(import_list, 1):
        mylist.append(s)
    mydict = {"passwords": mylist}
    with open(directory('') + 'store.json', 'w', encoding='utf-8') as f:
        json.dump(mydict, f)
    print('    Complete. %d records imported.' % count)


def export(key):
    date = str(datetime.datetime.now())[:10]
    with open(directory('') + 'store.json', 'r') as f:
        store_dict = json.load(f)

    exportlist = store_dict['passwords']
    header = ('id', 'title', 'site', 'username', 'email', 'password',
              'note', 'date_modified', 'date_exported')
    file_name = 'export-%s.csv' % date
    file_path = os.path.join(directory('export'), file_name)
    try:
        os.mkdir(directory('export'))
    except OSError:
        pass
    else:
        print("Successfully created the directory %s " % directory('export'))
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        w = csv.writer(csvfile, delimiter=',',
                       quotechar='"', quoting=csv.QUOTE_MINIMAL)
        c = 0
        w.writerow(header)
        for r in exportlist:
            password = r['password']
            salt2 = password['salt']
            token = password['token']
            pw = unlock(key, salt1(), salt2, token)
            w.writerow([str(r['pid'])] +
                       [r['title']] +
                       [r['site']] +
                       [r['username']] +
                       [r['email']] +
                       [pw] +
                       [r['note']] +
                       [r['timestamp'][:10]] +
                       [date])
            c += 1
    print('%d passwords exported.' % c)


def imp_csv(key):
    file_name = input('    Enter file name: ')
    file_path = os.path.join(directory('import'), file_name)
    if os.path.exists(file_path):
        import_list = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                site = row['site']
                username = ""
                email = row['username']
                date = str(datetime.datetime.now())
                pid = id_(date)
                if row['password']:
                    salt2 = get_salt()
                    token = lock(key, salt1, salt2, row['password'].encode())
                    salt = pickle_bytes(salt2)
                else:
                    password = 'NA'
                password = {"salt": salt, "token": token}
                title = row['title']
                note = row['note']
                new_dict = create_passcard(
                    site,
                    username,
                    email,
                    password,
                    date,
                    title,
                    note,
                    pid
                )
                import_list.append(new_dict)
                sleep(.1)
        save_import(import_list)
    else:
        print('File does not exist.')


"""
        Passcard Functions
"""


def id_(date):
    """
    Takes string from datetime.now() and returns 14 character
    unique id for each passcard
    """
    return date.translate(
        str.maketrans(' ', '-', string.punctuation)
        ).replace("-", "")[2:16]


def generate(length, complexity, key, username, site):
    pw = generate_password(length, complexity)
    pyperclip.copy(pw)
    date = str(datetime.datetime.now())
    title = ""
    note = ""
    salt2 = get_salt()
    token = lock(key, salt1(), salt2, pw.encode())
    password = {"salt": pickle_bytes(salt2), "token": token}
    passcard = create_passcard(
        site,
        username,
        username + '@moger.com',
        password,
        date,
        title,
        note,
        id_(date)
    )
    save_passcards(passcard)


def create_passcard(site, username, email, password, timestamp,
                    title, note, pid):
    keys = [
        'site',
        'username',
        'email',
        'password',
        'timestamp',
        'title',
        'note',
        'pid'
    ]
    values = [
        site,
        username,
        email,
        password,
        timestamp,
        title,
        note,
        pid
    ]
    new_dict = []
    new_dict = dict(zip(keys, values))
    return new_dict


def save_passcards(new_dict):
    with open(directory('') + 'store.json', 'r') as f:
        store_dict = json.load(f)
    mylist = []
    passlist = store_dict['passwords']
    saved = 0
    for s in passlist:
        if s['pid'] == new_dict['pid']:
            mylist.append(new_dict)
            saved = 1
        else:
            mylist.append(s)
    if not saved:
        mylist.append(new_dict)
    mydict = {"passwords": mylist}
    with open(directory('') + 'store.json', 'w', encoding='utf-8') as f:
        json.dump(mydict, f)
    print('    Record Saved')


def browse(site, key):
    browse.index = ""
    with open(directory('') + 'store.json', 'r') as f:
        store_dict = json.load(f)
        site_list = []
        countID = 0
    for row in store_dict['passwords']:
        if site in row['site']:
            countID += 1
            password = row['password']
            salt2 = password['salt']
            token = password['token']
            pw = unlock(key, salt1(), salt2, token)
            row_dict = row
            row_dict['countID'] = countID
            row_dict['temp_pw'] = pw
            site_list.append(row_dict)
    if len(site_list) == 0:
        print("    You have no passcards matching %s." % (site))
        x = input(
            "    Create a new passcard for %s? (y/N): " % (site))
        if x == 'y':
            browse.index = 0
    else:
        for r in site_list:
            print('')
            print('    countID  : [%s]' % r['countID'])
            print('    title    : %s' % r['title'])
            print('    site     : %s' % r['site'])
            print('    username : %s' % r['username'])
            print('    email    : %s' % r['email'])
            print('    password : %s' % r['temp_pw'])
            print('    modified : %s' % r['timestamp'][:16])
            print('    notes    : %s' % r['note'])
            print('    ........   ................')
            print('')

        print('\n    To COPY password to clipboard enter countID' +
              '\n    To EDIT a record enter \'E\' before the countID' +
              '\n    To DELETE a record enter \'D\' before the countID' +
              '\n    Enter nothing to cancel')
        x = input('    Enter choice (1-%d): ' % countID)
        if x.isdigit():
            if 1 <= int(x) <= countID:
                passcard = search(site_list, 'countID', int(x))
                pyperclip.copy(passcard['temp_pw'])
                print("    Done! %s saved to clipboard."
                      % passcard['temp_pw'])
            else:
                print('     Out of range')
        elif x.startswith('E'):
            y = int(x.lstrip('E'))
            passcard = search(site_list, 'countID', y)
            print('\n    >>title: %s' % passcard['title'])
            title2 = input('    Press Enter to keep, or type new title: ')
            print('\n    >>site: %s' % passcard['site'])
            site2 = input('    Press Enter to keep, or type new site: ')
            print('\n    >>username: %s' % passcard['username'])
            username2 = input(
                '    Press Enter to keep, or type new username: ')
            print('\n    >>email: %s' % passcard['email'])
            email2 = input('    Press Enter to keep, or type new email: ')
            print('\n    >>password: %s' % passcard['temp_pw'])
            password2 = input(
                '    Press Enter to keep, or type new password: ')
            note2 = input('\n    Enter a note: ')
            date = str(datetime.datetime.now())
            if site2:
                passcard['site'] = site2
            if username2:
                passcard['username'] = username2
            if email2:
                passcard['email'] = email2
            if password2:
                token = lock(key, salt1(),
                             unpickle_string(passcard['password']['salt']),
                             password2.encode())
                passcard['password']['token'] = token
            if title2:
                passcard['title'] = title2
            if note2:
                note = passcard['note']
                passcard['note'] = date[:16] + ': ' + note2 + '\n' + note
            with open(directory('') + 'store.json', 'r') as f:
                store_dict = json.load(f)
            passlist = store_dict['passwords']
            mylist = []
            for r in passlist:
                if r['pid'] == passcard['pid']:
                    if "temp_pw" in passcard:
                        del passcard['temp_pw']
                    if "countID" in passcard:
                        del passcard['countID']
                    mylist.append(passcard)
                else:
                    mylist.append(r)
            mydict = {"passwords": mylist}
            with open(directory('') + 'store.json', 'w',
                      encoding='utf-8') as f:
                json.dump(mydict, f)
            print('    Saved')
        elif x.startswith('D'):
            y = int(x.lstrip('D'))
            with open(directory('') + 'store.json', 'r') as f:
                store_dict = json.load(f)
            mylist = []
            passlist = store_dict['passwords']
            passcard = search(site_list, 'countID', y)
            for r in passlist:
                if r['pid'] == passcard['pid']:
                    pass
                else:
                    mylist.append(r)
            mydict = {"passwords": mylist}
            with open(directory('') + 'store.json',
                      'w', encoding='utf-8') as f:
                json.dump(mydict, f)
            print('    Record Deleted')
        else:
            pass


"""
            Vault Functions
"""


def create_master():
    master = getpass.getpass(prompt="    Create a Master password: ")
    hashpass = p_hash.hash(master)
    fh = open(directory('') + 'hash', 'w', encoding='utf-8')
    fh.write(hashpass)
    fh.close()


def getkey(master):
    password = master.encode()
    salt = b'EC6873C47AD2F3FABCCC62AF564996F3F84ECD446433DDE'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def get_salt():
    return os.urandom(16)


def encrypt(key, salt, password):
    f = Fernet(key)
    encrypted = f.encrypt(password)
    return encrypted


def decrypt(key, salt, password):
    f = Fernet(key)
    decrypted = f.decrypt(password)
    return decrypted


def pickle_bytes(token):
    p = pickle.dumps(token)
    return base64.b64encode(p).decode('ascii')


def unpickle_string(token):
    p = base64.b64decode(token)
    return pickle.loads(p)


def lock(key, salt1, salt2, password):
    encrypted = pickle_bytes(
        encrypt(key, salt2, encrypt(key, salt1, password)))
    return encrypted


def unlock(key, salt1, salt2, token):
    decrypted = decrypt(
        key, salt1, decrypt(key, salt2,
                            unpickle_string(token)))
    return decrypted.decode()


def change_master(key):
    while True:
        new_master = getpass.getpass(
            prompt='    Create a new Master password: ')
        new_master2 = getpass.getpass(
            prompt='    Enter new Master password again: ')
        if new_master == new_master2:
            key2 = getkey(new_master)
            new_list = []
            with open(directory('') + 'store.json', 'r') as f:
                store_dict = json.load(f)
            for row in store_dict['passwords']:
                password = row['password']
                salt2 = unpickle_string(password['salt'])
                old_token = password['token']
                token = unlock(key, salt1(), salt2, old_token)
                row['password']['salt'] = pickle_bytes(salt2)
                row['password']['token'] = lock(
                    key2, salt1(), salt2, token.encode())
                new_list.append(row)
            newdict = {"passwords": new_list}
            with open(directory('') + 'store.json', 'w',
                      encoding='utf-8') as f:
                json.dump(newdict, f)
            hashpass = p_hash.hash(new_master)
            fh = open(directory('') + 'hash', 'w', encoding='utf-8')
            fh.write(hashpass)
            fh.close()
            master = new_master
            change_master.key = key2
            print('    Master password and all passcards updated')
            break
        else:
            print("    Passwords do not match. Try again.")


def generate_password(length, complexity):
    alphabet = string.ascii_letters + string.digits
    alnum = length
    symbols = '!'+'@'+'#'+'$'+'%'+'^'+'&'+'*'
    if complexity in ('y', 'Y', 'yes', 'Yes'):
        alphabet = alphabet + symbols
        alnum = length - 1
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                sum(c.isdigit() for c in password) >= 2 and
                sum(c.isalnum() for c in password) == alnum):
            break
    return password


"""
            Other
"""


def search(list, key, value):
    for item in list:
        if item[key] == value:
            return item


def view_json():
    with open(directory('') + 'store.json', 'r') as f:
        store_dict = json.load(f)
        print(json.dumps(store_dict, indent=4, sort_keys=False))


def section_title(option):
    print(
          '\n' + '    ' + option +
          '\n' + '    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def is_empty(anything):
    if anything:
        return False
    else:
        return True


def goback():
    x = input("    Go Back to Menu (m) or Exit (X) :")
    if x == "m":
        goback.index = ""
    else:
        goback.index = 7


def main():
    index = ""
    site = ""
    menu_items = {
        '1': 'Create New Password',
        '2': 'Browse Passcards',
        '3': 'Generate Random Password',
        '4': 'View JSON',
        '5': 'Import Passwords',
        '6': 'Change Master Password',
        '7': 'Export Passwords',
        '8': 'Quit'
    }
    key = ""
    tries = 3
    if not os.path.exists(directory('')):
        create_folders()
    while is_empty(key):
        if os.path.exists(directory('') + 'hash'):
            master = getpass.getpass(prompt='    Password: ')
            with open(directory('') + 'hash', 'r', encoding='utf-8') as f:
                saved_hash = f.read()
            if p_hash.verify(master, saved_hash):
                print("    Welcome. Login successful!")
                key = getkey(master)
                switch = 1
            else:
                tries -= 1
                switch = 0
                if tries > 0:
                    print("    Password failed. %d attemps left." % (tries))
                elif tries == 0:
                    print("    Password failed. Good-bye.")
                    break
        else:
            setup()
            if os.path.exists(directory('') + 'hash'):
                print('    Login to continue setup.')
            else:
                print('    Something has gone wrong. Quitting.')
                break

    while switch == 1:
        if index == "":
            section_title('Menu')
            for (k, v) in menu_items.items():
                print('    [' + k + '] ' + v)
            print('\n')
            x = input('    Enter number to select: ')
            index = int(x)-1
        elif index == 0:            # Create New Password
            section_title(menu_items['1'])
            if is_empty(site):
                site = input("    Enter site name: ")
            else:
                print("    Site: %s" % (site))

            length = input("    Enter number of characters. Default is 12 : ")
            if is_empty(length):
                length = 12
            complexity = input("    Include special characters?(N/y): ")
            username = input("    Enter username: ")
            generate(int(length), complexity, key, username, site)
            print("    Done! %s saved to clipboard." % pyperclip.paste())
            goback()
            index = goback.index
        elif index == 1:            # Browse Passcards
            section_title(menu_items['2'])
            site = input("    Enter site name: ")
            browse(site, key)
            if browse.index == 0:
                index = browse.index
            else:
                goback()
                index = goback.index
        elif index == 2:            # Generate Random Password
            section_title(menu_items['3'])
            length = input("    Enter number of characters. Default is 12 : ")
            if is_empty(length):
                length = 12
            complexity = input("    Include special characters?(N/y): ")
            if is_empty(complexity):
                complexity = "No"
            pw = generate_password(int(length), complexity)
            print("    Done!  %s saved to clipboard." % pw)
            goback()
            index = goback.index
        elif index == 3:            # View JSON
            section_title(menu_items['4'])
            view_json()
            goback()
            index = goback.index
        elif index == 4:           # Import passwords
            section_title(menu_items['5'])
            imp_csv(key)
            goback()
            index = goback.index
        elif index == 5:           # Change Master Password
            section_title(menu_items['6'])
            change_master(key)
            key = change_master.key
            goback()
            index = goback.index
        elif index == 6:           # Export Paswords
            section_title(menu_items['7'])
            export(key)
            goback()
            index = goback.index
        elif index == 7:            # Quit and Exit Program
            print("    Thanks for playing. Goodbye!\n")
            break
        else:
            print("    [%s] not a valid option!\n" % x)
            x = input('    Try again? ')
            if x.isdigit():
                index = int(x)-1
            else:
                index = ""


if __name__ == '__main__':
    if get_version():
        main()
    else:
        print('You need to be on Python 3.0 or greater to run SimplePass.')
