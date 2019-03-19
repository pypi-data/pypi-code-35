import re


def build_time(tag,fields,case):
    tag_text = fields.pop(0)
    s = """
          <tr class='additional case_%s'>
            <td>
              <label class="control-label">%s</label>
            </td>
            <td >
              <input id="%s-hours-text"   size="2" value="0"  type="tel"> h
              <input id="%s-minutes-text" size="2" value="30" type="tel"> m
              <input name="dyn_dyn_%s_dyn_%s" size="5" value="00:30"  type="hidden"> 
            </td>
          </tr>

    """ % (case,tag_text,tag, tag, case,tag)
    return s

def build_select(tag,fields,case):
    tag_text = fields.pop(0)
    s = """
          <tr class='additional case_%s'>
            <td>
              <label class="control-label">%s</label>
            </td>
            <td>
              <select name="dyn_dyn_%s_dyn_%s" class="form-control dynamic jobform">
    """ % (case,tag_text,case,tag)

    options = fields.pop(0).split(",")
    for o in options:
        s = s + """\t\t<option value="%s">%s</option>
        """ % (o,o)
    s = s + """
              </select>
            </td>
          </tr>
    """
    return s

def build_input(tag,fields,case):
    tag_text = fields.pop(0)
    if len(fields):
        tag_type = fields.pop(0)
    else:
        tag_type = "text"
    s = """
          <tr class='additional case_%s'>
            <td>
              <label class="control-label">%s</label>
            </td>
            <td>
              <input name="dyn_dyn_%s_dyn_%s" type="%s">


    """ % (case,tag_text,case,tag,tag_type)


    s = s + """
            </td>
          </tr>
    """
    return s


def build_gui_from_template(job_file,case):

    job_file_content = "".join(open(job_file,"r").readlines())

    variables =  [ x[2:-2] for x in re.findall('__.+__', job_file_content)]

    tags = {}

    l = ""

    for v in variables:
        print(v)

        fields = v.split(";")

        tag = fields.pop(0)

        if len(fields):

            web_type = fields.pop(0)

            if web_type == "select":

                s = build_select(tag,fields,case)
                l = l + s

            elif web_type == "time":
        
                s = build_time(tag,fields,case)
                l = l +s

            elif web_type == "input":
        
                s = build_input(tag,fields,case)
                l = l +s
    return l

                
if __name__ == "__main__":
    job_file = "/home/kortass/JUPYTER/job_templates/sk/00 - lab.template"

    l = build_gui_from_template(job_file)
    print(l)

    
    

