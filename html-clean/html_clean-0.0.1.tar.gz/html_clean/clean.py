import re

"""
"<style>([\s\S]*?)</style>",
                                     "<p([\s\S]*?)>",
                                     "<span([\s\S]*?)>",
                                     "</span>","</p>",
                                     "<p>","<a([\s\S]*?)>",
                                     "<div([\s\S]*?)>",
                                     "</div>",
                                     "<font([\s\S]*?)>",
                                     "</font>",
                                     "<b>",
                                     "</b>",
                                     # "<(\w+?)([\s\S]*?)>",
                                     "<td([\s\S]*?)>",
                                     "<table([\s\S]*?)>",
                                     "<tbody>","<tr>","</td>","</tr>","</tbody>","</table>",
                                     "<tr([\s\S]*?)>"
                                     "<h1>([\s\S]*?)</h1>",
                                     "</a>","<h([\d]*?)>","</h([\d]*?)>",
                                     "<!([\s\S]*?)>",
                                     "<v:([\s\S]*?)>",
                                     "</v:([\s\S]*?)>",
                                     "<strong>",
                                     "</strong>",
                                     "<b([\s\S]*?)>",
                                     '<b style="FONT-FAMILY: ">',
                                     "<o:([\s\S]*?)>",
                                     "</o:([\s\S]*?)>",
                                     "<\?xml:([\s\S]*?)>",
                                     "<br([\s\S]*?)>","""
Useless_string = ["<p>","</p>"]
def Clean(html):
    for string in Useless_string:
        html = re.sub(string,"", html)
    return html