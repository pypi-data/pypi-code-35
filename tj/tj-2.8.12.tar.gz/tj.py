import os
import sys
import time
import shutil
import random
import base64
import hashlib
import os.path
import zipfile
from email import encoders
from email.header import Header
import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage


__version__ = "2.8.12"
__author__ = "Tushar Jain"

__doc__ = '''

 _______ ________
|__   __|___   __| PRODUCTIONS 2019
   | |      | |
   | |    __| |
   |_|   \\___/


A simple but powerful module that will provide you many useful methods.

Version: %s

Updated on: 17th March 01:35 PM
''' % ( __version__)


colors = {"BLACK": [0, 0, 0], "WHITE": [255, 255, 255], "GOLD": [255, 223, 0], "METALLIC GOLD": [212, 175, 55], "LIGHT YELLOW": [255, 255, 224],
          "YELLOW": [255, 255, 40], "ORANGE": [255, 165, 0], "DARK ORANGE": [255, 140, 0], "RED": [255, 0, 0],
          "DARK RED": [135, 0, 0], "MAROON": [120, 0, 0], "BROWN": [165, 42, 42], "PINK": [255, 192, 203],
          "HOT PINK": [255, 105, 180], "LIGHT PINK": [255, 182, 193], "VIOLET": [148, 0, 211], "PURPLE": [160, 32, 240],
          "INDIGO": [75, 0, 130], "BLUE": [0, 0, 255], "SKY BLUE": [135, 206, 250], "DARK BLUE": [0, 0, 139],
          "LIGHT GREEN": [0, 200, 0], "GREEN": [50, 205, 50], "DARK GREEN": [0, 139, 0], "LIME": [0, 255, 0], "FOREST GREEN": [35, 140, 35],
          "GRAY": [128, 128, 128], "CRIMSON": [220, 20, 60], "BRICK": [178, 34, 34], "FUCHSIA": [255, 0, 255],
          "LIGHT GRAY": [211, 211, 211], "SILVER": [92, 192, 192], "DARK GRAY": [105, 105, 105], "OLIVE": [128, 128, 0],
          "TEAL": [0, 128, 128], "CYAN": [0, 255, 255], "CHARCOAL": [54, 70, 80], "CHOCOLATE": [210, 105, 30],
          "WOOD": [255, 165, 79], "FERRARI": [255, 40, 0], "PEACH": [255, 218, 185], "CREAM": [245, 255, 250],
          "GRAPE": [110, 45, 168], "DENIM": [21, 96, 189], "ARMY": [75, 83, 32], "COFFEE": [111, 78, 55],
          "IRON": [203, 205, 205], "COPPER": [184, 115, 51]}

color_names = list(colors.keys())


term_text_colors = {'BLACK': 30, 'RED': 31, 'GREEN': 32, 'YELLOW': 33, 'BLUE': 34,
                    'PURPLE': 35, 'OLIVE': 36, 'WHITE': 37, '': ''}

term_background_colors = {'BLACK': 40, 'RED': 41, 'GREEN': 42, 'YELLOW': 43, 'BLUE': 44,
                          'PURPLE': 45, 'OLIVE': 46, 'WHITE': 47, '': ''}

styles = {'NORMAL': 0, 'ITALIC': 3, 'BOLD': 1, 'UNDERLINE': 4}


def color_text(text, text_color='', background_color='',
               bold=False, italic=False, underline=False):
    """Args->

    text-> The string which the user provides to be colored

    text_color-> An optional argument, set to WHITE by default.
            This argument decides the color of the text.

    background_color-> An optional argument, set to BLACK by default.
            This argument decides the background color of the text.

    bold-> An optional argument, set to False by default.
            This argument when set to True, bolds the text.

    italic-> An optional argument, set to False by default.
            This argument when set to True, makes the text italic.

    underline-> An optional argument, set to False by default.
            This argument when set to True, underlines the text.


    color_text is a function, which returns a string of colored text,
    which can be printed to look the information more attractive.
    This function returns a string. Which when printed, is printed in the
    designated color and style.
    NOTE: Don't use this colored string for any other thing, than printing!
        Also the bold, italic and underline feature might not work in Windows.

    You have the following color choices for both, the text and background-
    WHITE, BLACK, RED, BLUE, GREEN, YELLOW, OLIVE, PURPLE.

    eg.
    colored_text = color_text(
    "Hello",text_color='BLUE',italic=True)
    print('This text is'+colored_text)

    Output: This text is Hello | Here "Hello" will be BLUE in color and in italic
    """
    global term_text_colors, term_background_colors, styles
    is_present = True

    try:
        import colorama
        colorama.init()
    except ModuleNotFoundError:
        is_present = False

    if not is_present:
        raise ModuleNotFoundError(
            """colorama module not found.
    Install colorama module using 'pip install colorama'

    * colorama is used to display colored text""")

    reset = '\x1b[0m'
    L = []

    tc_int = term_text_colors[
        text_color.upper()]  # int for text color
    bc_int = term_background_colors[
        background_color.upper()]  # int for background color

    if bold:
        L.append(styles['BOLD'])
    if italic:
        L.append(styles['ITALIC'])
    if underline:
        L.append(styles['UNDERLINE'])

    if background_color!='':
        L += [tc_int, bc_int]
    else:
        L += [tc_int]
    L = [str(i) for i in L]

    temp = ';'.join(L)
    color = "\x1b[%sm" % temp
    colored_text = color + text + reset
    return colored_text


def transform_color(color1, color2, skipR=1, skipG=1, skipB=1):
    """
transform_color(color1, color2, skipR=1, skipG=1, skipB=1)


This function takes 2 color1 and color2 RGB color arguments, and then returns a
list of colors in-between the color1 and color2

eg- tj.transform_color([0,0,0],[10,10,20]) returns a list:-
[[0, 0, 0], [1, 1, 1], [2, 2, 2] ... [9, 9, 9], [10, 10, 10], [10, 10, 11] ... [10, 10, 20]]

This function is very useful for creating color fade or color transition effects in pygame.

There are 3 optional arguments, which are skip arguments set to 1 by default.
"""
    L = []
    if (color1[0] < color2[0]):
        i = list(range(color1[0],
                       color2[0] + 1,
                       skipR))
    else:
        i = list(range(color2[0], color1[0] + 1, skipR))[::-1]
    if i == []:
        i = [color1[0]]

    if (color1[1] < color2[1]):
        j = list(range(color1[1],
                       color2[1] + 1,
                       skipG))
    else:
        j = list(range(color2[1], color1[1] + 1, skipG))[::-1]
    if j == []:
        j = [color1[1]]

    if (color1[2] < color2[2]):
        k = list(range(color1[2],
                       color2[2] + 1,
                       skipB))
    else:
        k = list(range(color2[2], color1[2] + 1, skipB))[::-1]
    if k == []:
        k = [color1[2]]

    x = max(len(i), len(j), len(k))
    for m in range(len(i), x):
        i += [i[-1]]
    for m in range(len(j), x):
        j += [j[-1]]
    for m in range(len(k), x):
        k += [k[-1]]

    for m in range(x):
        l = [i[m], j[m], k[m]]
        L += [l]
    return L


def allcolors(color=None, flag=False):
    """allcolors(color=None)
If called, this function prints all the colors available in the module
If the optional color argument color is given, it will search colors related
    to the given color.
    eg- allcolors("GRAY") returns "GRAY" , "DARK GRAY", etc.

There is another optional argument called flag.
flag is set to False by default, and it prints the results, and doesn't return
flag=True returns the results in a list, and prints nothing."""
    if color is None:
        L = color_names
    else:
        L = []
        color = color.upper()
        for c in color_names:
            if color in c:
                L += [c]

    if flag == False:
        for i in L:
            print("%-20s   %s" % (i, colors[i]))
    else:
        return color_names


def get_filename(path):
    """Takes full path of the file as argument
Gives the file name from the full path of the file with extension"""
    path = os.path.abspath(path)
    x = os.path.basename(path)
    return x


def get_foldername(path):
    """Takes a path as an argument. Path can be of a folder or file, in string
    Returns the path of the containing folder of that file/folder.

    eg.
    Input: C:\\Users\\<Username>\\Desktop\\Project\\New Folder\\Experiment.py
    Output: C:\\Users\\<Username>\\Desktop\\Project\\New Folder"""
    path = os.path.abspath(path)
    temp = path.split("\\")
    temp = temp[:-1]
    x = "\\".join(temp)
    return x


def get_files_in_folder(path, show_progress=False):
    """Args->

    path-> The path of the directory.

    show_progress-> It is an optional argument set to False by default.
        When show_progress is True, the progress will be displayed.

    This function returns the full path of all the files and sub-files present
    in the directory."""

    is_present = True
    if show_progress != False:
        try:
            from tqdm import tqdm
        except:
            is_present = False

        if not is_present:
            raise ModuleNotFoundError(
                """tqdm module not found.
    Install tqdm module using 'pip install tqdm'

    * tqdm module is required to show progress""")
        generator = tqdm(os.walk(os.path.abspath(path)))
    else:
        generator = os.walk(os.path.abspath(path))

    L = []

    for root, dirs, files in generator:
        for file in files:
            L += [os.path.join(root, file)]
    return L


def get_folders_in_folder(path, show_progress=False):
    """Args->

    path-> The path of the directory.

    show_progress-> It is an optional argument set to False by default.
        When show_progress is True, the progress will be displayed.

    This function returns the full path of all the folders that folder and its
    subfolders, in a list"""

    is_present = True
    if show_progress != False:
        try:
            from tqdm import tqdm
        except:
            is_present = False

        if not is_present:
            raise ModuleNotFoundError(
                """tqdm module not found.
    Install tqdm module using 'pip install tqdm'

    * tqdm module is required to show progress""")
        generator = tqdm(os.walk(os.path.abspath(path)))
    else:
        generator = os.walk(os.path.abspath(path))

    return [i for i, j, k in generator]


def get_folder_contents(path, show_progress=False):
    """Args->

    path-> The path of the directory.

    show_progress-> It is an optional argument set to False by default.
        When show_progress is True, the progress will be displayed.

    This function returns the full path of all the files and folders that folder
    and its subfolders, in a list of lists.
    Returned list will look like [ [...Folders...] , [...Files...] ]"""

    is_present = True
    if show_progress != False:
        try:
            from tqdm import tqdm
        except:
            is_present = False

        if not is_present:
            raise ModuleNotFoundError(
                """tqdm module not found.
    Install tqdm module using 'pip install tqdm'

    * tqdm module is required to show progress""")
        generator = tqdm(os.walk(os.path.abspath(path)))
    else:
        generator = os.walk(os.path.abspath(path))

    Files = []
    Folders = []

    for root, dirs, files in generator:
        Folders += [root]
        for file in files:
            Files += [os.path.join(root, file)]
    return [Folders, Files]


def factorial(num):
    """Takes a number as argument
Gives factorial of that argument"""
    if num < 0:
        raise "Number is less than 0"
    if not isinstance(num, type(1)):
        raise "Number is not an integer"
    r = 1
    for i in range(1, num + 1):
        r = r * i
    return r


def email(email_id, password, recievers, body, subject="Email sent by TJ module Python",
          attachments=[], email_type='plain', html_resources=[]):
    """Args->

    email_id-> The email id of the sender.

    password-> The password of email the sender.

    receivers-> The list of email id of receivers. receivers argument
    should compulsorily be a list, even if there is just 1 receiver.

    body-> The body of the email.

    subject-> subject of email.

    attachments-> A list of paths of files which you need to send
    as attachment. It is an optional argument.

    email_type-> The type of email text you are going to send. It is set to
    'text' by default, but by setting email_type to 'html', you will be able to
    send beautiful looking emails.In this case, you need to provide the html code
    instead of any body, i.e. body will contain the html code.

    html_resources-> If your html page contains pictures, then your will have to
    send the path of those pictures in the form of a list. You also have to edit your
    html file such that in all the image tags, src = "cid:res<number>", instead of
    writing the path of the file in the image tag. Also, you need to rename all the
    image files accordingly as res0.png, res1.png, res2.jpg, etc.

    eg.
    HTML code:
    <html >
    .
    .
    <image src = "cid:res0" ... >
    .
    .
    . . . < image src = "cid:res1"... >
    .
    .
    <image src = "cid:res2"... >
    .
    .

    <\html >

    and here, html_resources = ['images\\res0.png', 'images\\res1.png', 'images\\res2.jpg']

    # So all the image paths should be replaced by
    # "cid:res<number>" and this
    number should be a proper sequence of 0, 1, 2, 3 and so on. Any error in this part,
    would result into not showing up your image.

    *Also it is advised to rename the files accordingly to their cid, as shown in the
    above example.

    This function uses the SMTP library to send an email to the receivers using
    the email id of the sender. It can also send attachments in the email.

    *If you are using Gmail, then you might want to change the settings of your
    email account to allow 3rd party apps to send or receive emails, or else
    you will not be able to send emails using that email id.
    """

    uname = email_id
    pword = password

    emailfrom = email_id
    emailto = recievers

    body = [body]
    subject = subject

    msg = MIMEMultipart()
    msg['From'] = emailfrom
    msg['To'] = ', '.join(emailto)
    msg['Subject'] = subject

    if email_type.upper() == 'HTML':
        msg.attach(MIMEText(''.join(body), 'html'))
    else:
        msg.attach(MIMEText(''.join(body)))

    for i in range(len(html_resources)):
        resource = html_resources[i]
        f = open(resource, 'rb')
        data = f.read()
        f.close()
        msgRes = MIMEImage(data)
        s_temp = "<res%s>" % i
        msgRes.add_header('Content-ID', s_temp)
        msg.attach(msgRes)

    # ATTACH FILES
    for item in attachments:
        part = MIMEBase('application', "zip")

        f = open(item, "rb")
        datatemp = f.read()

        part.set_payload(datatemp)
        encoders.encode_base64(part)
        filename = get_filename(item)
        part.add_header(
            'Content-Disposition',
            'attachment',
            filename=(
                Header(
                    filename,
                    'utf-8').encode()))
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % filename)
        msg.attach(part)

        # SECURE CONNECTION
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(uname, pword)

    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()


def is_Folder(path):
    """Takes the path of the folder as argument
Returns is the path is a of a Folder or not in bool"""
    if os.path.isdir(path):
        return True
    else:
        return False


def is_File(path):
    """Takes the path of the folder as argument
Returns is the path is a of a Folder or not in bool"""
    if os.path.isfile(path):
        return True
    else:
        return False


def get_startup_path():
    """Takes no arguments
Gives a list of full startup paths on a computer
eg:
[
 "C:\\Users\\ABC\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\",
 "C:\\Users\\John PC\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\",
 "C:\\Users\\Monica\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"]

 *[Public, Default, All Users, Default User] user will not be included in this list
"""

    a = "C:\\Users\\"
    b = "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
    user_L = os.listdir(a)
    L = []
    for user in user_L:
        if user in ['Public', 'Default',
                    'All Users', 'Default User']:
            continue
        if not is_Folder(a + user):
            continue
        path = a + user + b
        L += [path]
    return L


def convert_bytes(size):
    '''Takes bytes as input
    Converts those bytes into KB, MB, etc.
    And returns the size as a string.

    eg:
        >>>tj.convert_bytes(18244)
        '17.81 KB'
        >>>tj.convert_bytes(1024)
        '1.0 KB'
    '''
    L = ["Bytes", "KB", "MB", "GB", "TB"]
    for i in range(len(L)):
        if size // (1024 ** i) == 0:
            break
    s = str(size / 1024 ** (i - 1))
    s = s.split(".")
    s1 = s[0]
    s2 = s[1]
    s2 = s2[:2]
    s = s1 + "." + s2
    return "%s %s" % (s, L[i - 1])


def convert_time(t, r=2):
    '''Takes time in seconds as input
    Converts that time into s, min. , hr. , ms, day etc.
    And returns the time as a string.

    Also takes an optinal argument 'r', with default value
    of 2. When round is given, the time is rounded to that decimal
    digits. If 0 is given, then integer is used instead of float

    The function also takes into account the whether the number is 
    singular or plural, to give pleasing results.

    eg:
        >>>tj.convert_time(358610.0321233, r=4)
        '4.1506 Days'
        >>>tj.convert_time(86400,0)
        '1 Day'
        >>>tj.convert_bytes(0.3867455753)
        '386.75 ms'
        >>>tj.convert_bytes(2764)
        '46.07 min'
        >>>tj.convert_bytes(2764, r=0)
        '46 min'
    '''
    t=float(t)
    L=['micro sec', 'ms' ,'s' ,'min' ,'hr' ,'Day' ,'Month' ,'Year' ,'Decade', 'Century']
    if r==0:r=None
    else:r=int(r)

    converted_t=t/(10*10*12*30*24*60*60)
    if converted_t>0.95:
        if converted_t!=1.0:return f'{round(converted_t,2)} Centuries'
        else: return f'{round(converted_t,r)} Century'

    converted_t=t/(10*12*30*24*60*60)
    if converted_t>0.95:
        if converted_t!=1.0:plural='s'
        else: plural=''
        return f'{round(converted_t,r)} Decade{plural}'
    
    converted_t=t/(12*30*24*60*60)
    if converted_t>0.95:
        if converted_t!=1.0:plural='s'
        else: plural=''
        return f'{round(converted_t,r)} Year{plural}'
    
    converted_t=t/(30*24*60*60)
    if converted_t>0.95:
        if converted_t!=1.0:plural='s'
        else: plural=''
        return f'{round(converted_t,r)} Month{plural}'
    
    converted_t=t/(24*60*60)
    if converted_t>0.95:
        if converted_t!=1.0:plural='s'
        else: plural=''
        return f'{round(converted_t,r)} Day{plural}'
    
    converted_t=t/(60*60)
    if converted_t>0.95:
        return f'{round(converted_t,r)} hr'
    
    converted_t=t/(60)
    if converted_t>0.95:
        return f'{round(converted_t,r)} min'
    
    converted_t=t
    if converted_t>0.95:
        return f'{round(converted_t,r)} s'
    
    converted_t=t*1000
    if converted_t>0.95:
        return f'{round(converted_t,r)} ms'
    
    converted_t=t*(1000*1000)
    if converted_t>0.95:
        return f'{round(converted_t,r)} micro sec'
    
    else:
        converted_t=t*(1000*1000*1000)
        return f'{round(converted_t,r)} nano sec'
    

def file_size(file_path, Flag=False):
    """file_size(file_path, Flag=False)

Takes the full path of the file as input
Gives the size of the file in bytes

There is another argument Flag(set to False by default).
If Flag is true, it returns in format like 2.3 GB, 5.0 MB, etc.
    """
    size = os.path.getsize(file_path)
    if Flag:
        return convert_bytes(size)
    else:
        return size


def get_last_modified(path, flag=False):
    '''Get the date the the file was last modified of the.
    Arguments:\n path-> the path of the file
    flag-> Its a bool value, when False, the time is returned in
    Epoch seconds, if flag is True, time is returned in proper format.'''

    is_file = True
    try:
        a = os.stat(path)[-2]
    except FileNotFoundError:
        is_file = False

    if not is_file:
        raise FileNotFoundError("Path not found")

    if flag == False:
        return a
    if flag == True:
        return time.asctime(time.localtime(a))


def passed_time(flag=True):
    '''if flag=False, then returns the time after the function is called
        from the time the function was called first time in the program

    if flag=True, then returns the time in seconds b/w two successive calls
    Use it as a generator function
    You can create different instances to use it as per your convenience
    eg-
    import tj
    a=tj.passed_time()
    print(a.next()); time.sleep(5)
    print(a.next()) #This is used after waiting 5 sec.
    b=tj.passed_time()
    print(b.next()); time.sleep(5)
    print(a.next()); time.sleep(5)
    print(b.next())
    >>>0.0
    >>>5.0
    >>>0.0
    >>>5.0
    >>>10.0
    '''
    t = time.time()
    while True:

        if flag:
            m = time.time() - t
            t = time.time()
            yield m
        if not flag:
            yield time.time() - t


def take_src(name="src.png", DIR=""):
    """Args->

    name-> It as an optional argument, set to "src.png" by default.
        It is the name of the file can end with .png or .bmp extension

    DIR-> It is an optional argument, set to "" by default which means
        same as the working directory.
        It is the folder where you want to save the file.

    Prints and saves full - screen screen - shots in .png or .bmp format in a location"""

    is_present = True

    try:
        from autopy import bitmap
    except:
        is_present = False

    if not is_present:
        raise ModuleNotFoundError(
            """autopy module not found.
    Install autopy module using 'pip install autopy'

    * autopy module is required to take screenshots""")

    path = os.path.join(DIR, name)
    bitmap2 = bitmap.capture_screen()
    bitmap2.save(path)


def convert_currency(c1, c2, rate=None, flag=True):
    """Args->

    c1-> This is the currency which will be the input
        c1 should consist of amount and type in a single string, separated
            by a space
            eg. '100 EUR' where 100 is the amount and EUR is the type

    c2-> This is the currency which will be the output
        c2 should only consist of currency only
            eg. 'INR' or 'USD'

        *The purpose of using this string format is to reduce confusion.
        '40 USD' in a single string and 'INR' in another string gives
        clear indication of which currency is being converted in which.

    rate-> This is the rate of conversion. This argument is set
        to None by default. When rate is None, the rate of conversion
        will be automatically fetched from the Internet. When rate is
        provided by the user, that rate will be used instead. The rate
        should be such that c2 = c1 * rate(output=input * rate)

    flag-> True by default. If flag is False, all print statements of the
        function will be disabled.

    converts currency c1 to c2 using the currency rate 'rates'. This 'rates'
    Argument will be fetched from the Internet automatically from the Internet
    or will be provided by the user.

    An example of usage is:
    convert_currency('52.5 USD', 'INR') would result in 3727.5INR(taking 1USD=71INR)

    convert_currency('10 EUR', 'USD', 1.1) would result in 11USD (user gives 1EUR=1.1USD)"""

    amt1, type1 = c1.split(" ")
    amt1 = float(amt1)
    type1 = type1.upper()
    amt1 = round(amt1, 3)
    type2 = c2
    type2 = type2.upper()

    if rate is None:
        is_present = True
        try:
            from forex_python.converter import CurrencyRates
        except ModuleNotFoundError:
            is_present = False

        if not is_present:
            raise ModuleNotFoundError(
                """forex_python module not found.
    Install forex_python module using 'pip install forex-python'

    * forex - python is used to get the latest currency - exchange rates""")

        if flag:
            print(
                'Fetching currency exchange rates from Internet...\n\n')
        c = CurrencyRates()
        # All the exchange rates will be based on USD
        All_rates = c.get_rates(type1)
        rate = All_rates[type2]
        amt2 = amt1 * rate
        amt2 = round(amt2, 3)

        if flag:
            s_temp = "%s %s equals %s %s" % (
                amt1, type1, amt2, type2)
            print(s_temp)

    else:
        amt2 = amt1 * rate
        amt2 = round(amt2, 3)
        if flag:
            s_temp = "%s %s equals %s %s" % (
                amt1, type1, amt2, type2)
            print(s_temp)

    s_temp = "%s %s" % (amt2, type2)
    return s_temp


def getRandomString(L=None, number=None):
    '''Args->

    L-> optional argument, the function will return a random string of
    characters from the characters provided in the list L. Characters are case-sensitive
    Set to none by default, so any visible characters including a-z, A-Z, 0-9 and special
    symbols will be included. Characters from the order 33-126 will be included.

    number-> Length of the string.Set to None by default. When number=None, it will be
    determined randomly in the range 8-20.

    This function provides a sting of random characters.

    *make sure you type getRandomCharacters(number=8) if you want to change the
    number of characters instead of getRandomCharacters(8).
    '''
    s = ''
    if L is None:
        L = [chr(i) for i in range(33, 127)]

    if number is None:
        number = random.randint(8, 20)

    for j in range(number):
        temp = str(random.choice(L))
        s += temp
    return s


def encryptFile(InputFile, OutputFile=None,
                password=None, delete=False):
    '''Args->

    InputFile-> This is the file which will undergo encryption

    OutputFile-> This is the file you will get after encryption. It
    is an optional argument and set to None by default. When it is None,
    the OutputFile will have the same name an InputFile, and the original
    InputFile will be deleted.

    password-> The password which you will use to encrypt the file. It is an
    optional argument. It only consisting of only numbers, of length 8-20.

    delete-> This is an optional argument, set to False by default. If delete=True,
    the original InputFile will be deleted, and you will be left with the OutputFile.
    However, if OutputFile is None, or if OutputFile==InputFile, then it will not delete
    the OutputFile/InputFile.

    This function encrypts a file using AES-256 encryption. It takes a non-encrypted file
    as InputFile and then encrypts it as OutputFile.

    *The buffer-size used for encryption is 32*1024.'''

    is_present = True

    try:
        import pyAesCrypt as crypt
    except ModuleNotFoundError:
        is_present = False

    if not is_present:
        raise ModuleNotFoundError(
            """pyAesCrypt module not found.
    Install pyAesCrypt module using 'pip install pyAesCrypt'

    * pyAesCrypt is used for encrypting files.""")

    tempFile = 'temp.tjenc'

    try:
        os.remove(tempFile)
    except:
        pass
    try:
        os.remove(OutputFile)
    except:
        pass
    bufferSize = 32 * 1024
    if password is None:
        L = [str(i) for i in range(10)] + [str(i)
                                           for i in range(65, 91)]
        password = getRandomString(
            L=L, number=random.randint(8, 20))

    crypt.encryptFile(InputFile, tempFile, password, bufferSize)

    if delete:
        os.remove(InputFile)

    if (OutputFile is None) or (OutputFile == InputFile):
        OutputFile = InputFile
        os.remove(InputFile)

    os.rename(tempFile, OutputFile)
    return password


def decryptFile(InputFile, password,
                OutputFile=None, delete=False):
    '''Args->

    InputFile-> This is the file which will undergo decryption, it
    is assumed that InputFile was earlier encrypted with the 'encrypt'
    function of this module.

    password-> The password which you used to encrypt the file.

    OutputFile-> This is the file you will get after decryption. It
    is an optional argument and set to None by default. When it is None,
    the OutputFile will have the same name an InputFile, and the original
    InputFile will be deleted.

    delete-> This is an optional argument, set to False by default. If delete=True,
    the original InputFile will be deleted, and you will be left with the OutputFile.
    However, if OutputFile is None, or if OutputFile==InputFile, then it will not delete
    the OutputFile/InputFile.

    This function decrypts a file encrypted with AES-256 encryption. It takes an encrypted file
    as InputFile and then decrypts it as OutputFile.

    *The buffer-size used for decryption is 32*1024.'''

    is_present = True

    try:
        import pyAesCrypt as crypt
    except ModuleNotFoundError:
        is_present = False

    if not is_present:
        raise ModuleNotFoundError(
            """pyAesCrypt module not found.
    Install pyAesCrypt module using 'pip install pyAesCrypt'

    * pyAesCrypt is used for encrypting files.""")

    tempFile = 'temp.tjenc'

    try:
        os.remove(tempFile)
    except:
        pass
    try:
        os.remove(OutputFile)
    except:
        pass
    bufferSize = 32 * 1024

    crypt.decryptFile(InputFile, tempFile, password, bufferSize)

    if delete:
        os.remove(InputFile)

    if (OutputFile is None) or (OutputFile == InputFile):
        OutputFile = InputFile
        os.remove(InputFile)

    os.rename(tempFile, OutputFile)


def delete(path):
    '''Takes a path as an argument
The path can be of a folder or a file.

Automatically determines whether the path is a file/folder and
is it an empty folder or non-empty folder and then deletes it.

An error will be raise if not able to delete the file/folder.'''

    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def __keyGenerator(p):
    '''This function is not for use outside this module'''
    is_present = True

    try:
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
    except:
        is_present = False

    if not is_present:
        raise ModuleNotFoundError(
            """cryptography module not found.
    Install cryptography module using 'pip install cryptography'

    * cryptography is used for encrypting text.""")

    password_provided = p
    # Convert string to binary string
    password = password_provided.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'',
        iterations=5000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(
        kdf.derive(password))  # Can only use kdf once
    return key


def encrypt(message, password):
    '''Args->

    message-> This is the string which is going to be encrypted

    password-> This the password which you will use for to encryption

    This function is used to easily encrypt strings, using AES encryption.'''

    key = __keyGenerator(password)
    from cryptography.fernet import Fernet

    cipher = Fernet(key)
    e_message = cipher.encrypt(message.encode())
    return e_message.decode()


def decrypt(e_message, password):
    '''Args->

    e_message-> This is the encrypted string which is going to be decrypted.
    This string should be encrypted by the encrypt(...) function of this module.

    password-> This the password which you will have used for encryption

    This function is used to easily decrypt strings, which were encrypted by
    the encrypt(...) function of this module.'''
    key = __keyGenerator(password)
    from cryptography.fernet import Fernet

    cipher = Fernet(key)
    d_message = cipher.decrypt(e_message.encode())
    return d_message.decode()


def pinput(prompt='Password: '):
    '''Args->

    prompt-> Like the input() method, pinput also
    accepts a prompt string, which will be displayed
    to the user. It is an optional argument.

    pinput() (password-input) is a function, which makes entering
    sensitive data secure, by hiding the characters.'''
    x = getpass.getpass(prompt)
    return x


def make_hash(string):
    '''Args->

    string-> This is the string which you want to convert
    to hash.

    This function returns the hash of a string, using SHA256
    algorithm. Returns the hash as a binary string.'''

    hash_object = hashlib.sha256(string.encode())
    digest = hash_object.digest()
    return digest


def compress(InputFile, OutputFile=None):
    ''''Args->

    InputFile-> The path of the file you need to compress

    OutputFile-> The path of the file which you will get after compressing.
    It is an optional argument and is set to None by default. When it is None,
    the OutputFile will have the same same as InputFile, but with .zip extension.

    This function compress a file in .zip format

    eg.
    InputFile is "Datafile.txt"
    OutputFile is None. Then the compressed file created will be Datafile.zip

    InputFile is "My Presentation.ppt"
    OutputFile is "Compressed.rar". Then the compressed file created will be Compressed.rar
    '''
    if OutputFile is None:
        file_name = os.path.splitext(InputFile)[0]
        OutputFile = file_name + '.zip'

    zipF = zipfile.ZipFile(OutputFile, 'w')
    zipF.write(InputFile, compress_type=zipfile.ZIP_DEFLATED)
    zipF.close()


def extract(InputFile):
    ''''Args->

    InputFile-> The path of the file .zip you need to exctact

    This function extracts a zip file.
    '''
    tar = os.getcwd()
    zipF = zipfile.ZipFile(InputFile)
    zipF.extractall(tar)
    zipF.close()



def __getinput_win(string):
    '''This function is none of you business
    For windows'''
    is_present=True
    try:
        import msvcrt
    except:
        is_present=False
    if not is_present:
        raise ModuleNotFoundError(
            """msvcrt module not found.
    Install msvcrt module using 'pip install msvcrt'

    * msvcrt is used for get-ch function for instant inputs.""")

    x=str(msvcrt.getch().decode('utf-8'))
    return x


def __getinput_nix(string):
    '''This function is none of you business
    For Linux/Unix (*nix systems)'''
    import termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0

    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = str(os.read(fd, 1).decode('utf-8'))
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return str(c.decode('utf-8'))


def instant_input(string=None):
    '''instant_input(string=None)
    Like the built-in input() function, you
    can give a string to display for taking input from the user.

    Instant input, as the name suggests takes only one character from
    the user, and does not wait for the user to hit enter. 

    Returns the charcter enterd by the user.

    *This function is useful in making command-line games.
    '''
    if string!=None:print(string,end='')
    if 'win' in sys.platform:
        x=__getinput_win(string)
    else:
        x=__getinput_nix(string)
    return x


def get_ip_address():
    '''Returns the IP address of the computer'''
    import socket as s
    x=s.gethostname()
    x=s.gethostbyname(x)
    return x


if __name__ == '__main__':
    print(__doc__, '\n\n\n')
    try:
        f = open('README.md')
        data = f.read()
        f.close()
        print(data)
    except:
        pass
    input('\n\nEnter to continue...')