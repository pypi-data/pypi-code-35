# -*- coding: utf-8 -*-
import xslide

slide = xslide.XSlide("Title of example from README")

slide.markdown("""
# xslide

- Can accept a `markdown`
- Can draw graphs in `grot` (`graphviz` overlay)
- Can use HTML in `xplant`

Author: [Michał Kaczmarczyk](mailto:michal.s.kaczmarczyk@gmail.com), 

""")

slide.next("Header of the next slide")
slide.markdown("This one contains a graph:")

with slide.make_graph("this_dot_name", html_style="max-width: 55%;") as g:
    stage_1 = g.node("Stage 1", shape="box3d")
    stage_2 = g.node("Stage\n2", shape="circle", penwidth="3.1")
    g.edge(stage_1, stage_2, penwidth="2.6")
    sink = g.node("This\nsinks\nall")

    for n in ["alfa", "beta", "gamma", "delta"]:
        if n == "gamma":
            g.edge(stage_2, n, sink, penwidth="2.6", color="#314289")
        else:
            g.edge(stage_2, n, sink, color="#aabbcc", style="dashed")

slide.flush()  # makes a break
slide.markdown("""
*Markdown* with `nice_code` formatting. This example generates such a files:

```
>$ tree XSLIDE/examples/output/readme_example
XSLIDE/examples/output/readme_example
|-- index.html
|-- readme_example_01.html
|-- readme_example_01.html_this_dot_name.dot
|-- readme_example_01.html_this_dot_name.dot.svg
|-- readme_example_02.html
|-- serve.py
`-- xslide.css
```
""")

slide.store()
