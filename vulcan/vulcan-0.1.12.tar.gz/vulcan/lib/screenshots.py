from urwid import html_fragment
from textwrap import dedent

from controller import VulcanController
import vulcan.lib.store
import os
from collections import namedtuple

def blank_doc():
    return dedent("""
    <style type="text/css">
        pre, span {
            margin-top: -1px;
            margin-bottom: -1px;
            display: inline-block;
        }
        .urwid_fragment_usage {
            font-size: 0.8em;
        }
    </style>
    <div>
    %s
    </div>
    """)

def section(text, screenshot):
    return dedent(f"""
        <div>
            <p>{text}</p>
            <div  class='urwid_fragment_usage'>
            {screenshot}
            </div>
        </div>
    """)

def main(db_path):

    DocEntry = namedtuple("DocEntry", ["text", "key_sequence"])

    entries = [
        DocEntry("Press ctrl n to enter the edit card screen", ['ctrl n']),
        DocEntry("Add a question and an answer", ['down'] + list("Einstein's Famous Equation") + ['down'] + list("e=mc^2") + ['down'] + list("physics") + ['down']),
        DocEntry("Pressing 'Add' adds to card to the deck, and resets the input fields", ['enter']),
        DocEntry("Let's add a second card", ['up']*4 + list("Famous vulcan saying") + ['down'] + list("live long and ________") + ['down'] + list("prosper") + ['down'] + list('trivia') + ['down']),
        DocEntry("And a third", ['enter'] + ['up']*3 + list("Logic is the _______ of our civilization, with which we ascend from chaos, using reason as our guide.") + ['down'] + list("cement") + ['down'] + list('trivia') + ['down']),
        DocEntry("Vulcan now proceeds to asking you those questions", ['enter'] + ['down'] + ['enter']),
        DocEntry("What happens if we enter the wrong answer", list('f = ma') + ['enter']),
        DocEntry("Vulcan has an in-built help menu you can access with F1", ['f1']),
        DocEntry("Let's take a look at your stats by pressing F5", ['f5']),
        DocEntry("Vulcan can also display your cards in a grid by pressing F3", ['f3']),
    ]

    large = (110, 30)
    mid = (80, 20)

    html_fragment.screenshot_init([large], [x.key_sequence for x in entries])

    controller = VulcanController(db_path)
    controller.main(screenshot_mode=True)

    html = html_fragment.screenshot_collect()

    text = ""

    for i, doc in enumerate(html):
        try:
            text += section(entries[i-1].text if i > 0 else '', doc.replace('e5e5e5', '02233f').replace('0000ee', '1f7ad8'))
        except:
            pass

    with open('../docs/_static/usage.html', 'w') as w:
        w.write(blank_doc()%text)
