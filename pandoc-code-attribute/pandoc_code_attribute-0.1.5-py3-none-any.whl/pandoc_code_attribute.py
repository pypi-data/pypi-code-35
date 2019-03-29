"""
Add attribute to code blocks
"""

import panflute as pf

def action(elem, doc):
    if isinstance(elem, pf.CodeBlock):
        # Check whether emtpy
        if elem.classes: 
            config = doc.get_metadata('code-attribute')

            # Check config
            if config == True or (type(config) == list and elem.classes[0] in config):
                # Assign the class name to style attribute
                elem.attributes['style'] = elem.classes[0]

def main(doc=None):
    return pf.run_filter(action, doc=doc) 

if __name__ == '__main__':
    main()

