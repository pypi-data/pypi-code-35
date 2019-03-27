"""
Add attribute to code blocks
"""

import panflute as pf

def action(elem, doc):
    if isinstance(elem, pf.CodeBlock):
        # Assign the class name to style attribute
        elem.attributes['style'] = elem.classes[0]

def main(doc=None):
    return pf.run_filter(action, doc=doc) 

if __name__ == '__main__':
    main()

