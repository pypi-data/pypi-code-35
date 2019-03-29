import re

USELESS_STRING = ["<p>", "</p>",
                  "</div>", "<div([\s\S]*?)>",
                  "<style>([\s\S]*?)</style>",
                  "<p ([\s\S]*?)>",
                  "<span([\s\S]*?)>", "</span>",
                  "<font([\s\S]*?)>", "</font>",
                  "<b>", "</b>",
                  "<strong>", "</strong>",
                  "<!-([\s\S]*?)/>",
                  "<\?xml([\s\S]*?)/>",
                  "<v:([\s\S]*?)>",
                  "</v:([\s\S]*?)>",
                  "<o:([\s\S]*?)>",
                  "</o:([\s\S]*?)>",
                  "<td([\s\S]*?)>", "</td>", "</tr>", "</tbody>", "</table>",
                  "<a([\s\S]*?)>", "</a>",
                  "<br/>",
                  "<tbody>", "<tr([\s\S]*?)>", "<td([\s\S]*?)>", "<table([\s\S]*?)>",
                  "<b([\s\S]*?)>",
                  "&nbsp;"]


def Clean(html, append_to_change=[], do_not_change=[]):
    if type(append_to_change) != type([]):
        raise Exception("append_to_change must be list")
    if type(do_not_change) != type([]):
        raise Exception("do_not_change must be list")
    for string in USELESS_STRING:
        if string in do_not_change:
            continue
        html = re.sub(string, "", html)

    for string in append_to_change:
        html = re.sub(string, "", html)

    return html
