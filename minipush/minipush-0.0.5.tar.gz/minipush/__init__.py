"""
Minipush
Copyright (c) 2019 Rémi LANGDORPH
Software under MIT license
https://opensource.org/licenses/mit-license.php
"""
__version__="0.0.5"
__doc__="""
minipush v"""+__version__+""" by Rémi "Mr e-RL" LANGDORPH
Copyright (c) 2019 Rémi LANGDORPH - mrerl@warlegend.net

This lib supports the followings filetypes: css, js
Sample config:
{
    "origin": {"folders":["css/", "js/core/", "js/plugins/", "js/"]},
    "destination": {"folder": "../templates/", "exts": ["htm", "html"], "type": "embed", "basefolderlink": "/static/"},
    "anchors": {"js": {"start": "<!--AutomatedJSExport-Start-->",
                "end": "<!--AutomatedJSExport-End-->"},
                "css": {"start": "<!--AutomatedCSSExport-Start-->",
                        "end": "<!--AutomatedCSSExport-End-->"},
                "conf": {"start": "<!--AutomatedExport-Start->",
                        "end": "<-AutomatedExport-End-->"}
                },
    "format":{"embed":{"js": "<!--{filename}--><script>{content}</script>",
                       "css": "<!--{filename}--><style>{content}</style>"},
              "link":{"js": "<script src='{path}'/>",
                      "css": "<link href='{path}' rel='stylesheet'/>"}
            },
    "cache": {"folder": "../static/",
              "enabled": true}
}

Example script:
from minipush import Minipush
Minipush(file="config.json").run()

Don't hesitate to use the 'python -m minipush' (-h to see help)
"""

from .push import *

class Minipush:
    def __init__(self, file=None, dic=None):
        self.cssmin=cssmin
        self.jsmin=jsmin
        self.config=parse_config(file, dic)
    def run(self):
        t0=time.time()
        scripts={"js": {}, "css": {}}
        cfiles={}
        cpath=None
        o=get_origins(self.config["origin"]["folders"], ["js", "css"])
        osize=len(o)
        if cache_status(self.config):
            cfiles=get_cached_files(self.config["cache"]["folder"])
            cpath=self.config["cache"]["folder"]
        l=[]
        n=1
        for _ in o:
            m=min(_, cfiles, cpath, f"[{n}/{osize}]\t")
            n+=1
            l.append(m)
            if m["status"]=="success":
                if m["type"]=="js":
                    scripts["js"][_]=m["result"]
                if m["type"]=="css":
                    scripts["css"][_]=m["result"]
        templates_list=edit_templates(self.config["destination"]["folder"], self.config["destination"]["exts"], scripts, self.config)
        if export_status(self.config): export(scripts, self.config["export"]["rules"])
        if cache_status(self.config): export_cache(l, self.config)
        return {
            "stats": {
                "origins": lenext(o),
                "templates": len(templates_list),
                "dur": round(time.time()-t0, 3)
            },
            "origins": o,
            "templates": templates_list
        }
    def __str__(self):
        return f"<Minipush  config: {self.config}>"
    def __repr__(self):
        return f"<Minipush  config: {self.config}>"
    def reset(self):
        edit_templates(self.config["destination"]["folder"], self.config["destination"]["exts"], {"js": {}, "css": {}})
