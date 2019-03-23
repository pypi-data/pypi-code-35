from frogtips import constants
import random
import os


def say(text_to_say, tip_id=0):
    """Formats and prints the given input text so that it appears to come from
    the speech bubble of FROG ASCII art. Automatically figures out the width of
    the ASCII art and sizes the speech bubble appropriately. The maximim width
    of this function's output is determined by constants.FROGSAY_MAX_COLS"""
    ascii_art = [constants.FROG_IMAGE_1,
                 constants.FROG_IMAGE_2,
                 constants.FROG_IMAGE_3,
                 constants.FROG_IMAGE_4,
                 constants.FROG_IMAGE_5,
                 constants.FROG_IMAGE_6]

    secure_random = random.SystemRandom()

    frog_image = secure_random.choice(ascii_art)
    frog_image_width = get_max_width(frog_image.split("\n"))

    #max_text_width = constants.FROGSAY_MAX_COLS - frog_image_width - 4

    try:
        columns, rows = os.get_terminal_size(0)
    except OSError:
        columns, rows = os.get_terminal_size(1)

    max_text_width = columns - frog_image_width - 4

    formatted_rows = format_text(text_to_say, max_text_width)

    print_bubble(formatted_rows, frog_image_width, tip_id)

    print(frog_image)


def format_text(text_to_format,text_width):
    input_words = text_to_format.split(' ')
    this_row = ''
    previous_row = ''
    rows = []


    for word in input_words:
        this_row += word + ' '

        if len(this_row) > text_width:
            rows.append(previous_row[:-1])
            this_row = ''
            this_row += word + ' '
        else:
            previous_row = this_row

    if not this_row == '':
        rows.append(this_row)

    return rows


def print_bubble(rows_to_print=[], frog_image_width=0, tip_id=0):

    # figure out the actual length of the longest row of rows_to_print
    tip_width = get_max_width(rows_to_print)
    left_margin = (' ' * frog_image_width)

    bubble_border_top = left_margin + '╔' + ('═' * (tip_width + 2)) + '╗'
    bubble_border_bottom = left_margin + '╚' + ('═' * (tip_width + 2)) + '╝'

    print(bubble_border_top)

    for row in rows_to_print:
        # Add spaces at the end of each row so the speech bubble's ends
        # are aligned
        row += (' ' * (tip_width - len(row)))

        print(left_margin + "║ " + row + " ║")

    print(bubble_border_bottom)

    url = "https://" + constants.FROG_TIPS_DOMAIN + "/#" + str(tip_id)
    num_of_spaces = tip_width - len(url)
    print(left_margin + " ╱" + (' ' * num_of_spaces) + url)
    print(left_margin + "╱")


def get_max_width(text_array):
    width = 0

    for row in text_array:
        if len(row) > width:
            width = len(row)

    return width