import re


def build_time(tag,fields,case):
    tag_text = fields.pop(0)
    s = """
          <tr class='additional case___CASE__'>
            <td>
              <label class="control-label">__TAG_TEXT__</label>
            </td>
            <td >
              <input id="__CASE__-__TAG__-hours"   size="2" value="0"  type="tel" 
                     onChange="$('#__CASE__-__TAG__-whole').val($('#__CASE__-__TAG__-hours').val()+':'+$('#__CASE__-__TAG__-minutes').val()+':00')" > h
              <input id="__CASE__-__TAG__-minutes" size="2" value="30" type="tel"
                     onChange="$('#__CASE__-__TAG__-whole').val($('#__CASE__-__TAG__-hours').val()+':'+$('#__CASE__-__TAG__-minutes').val()+':00')" > m
              <input id="__CASE__-__TAG__-whole" name="dyn_dyn___CASE___dyn___TAG__" size="5" value="00:30:00"  type="hidden">
            </td>
          </tr>

    """
    s = s.replace('__CASE__',case).replace('__TAG_TEXT__',tag_text).replace('__TAG__',tag)
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
    tag_type = "text"
    tag_default_value = ""
    if len(fields):
        tag_type = fields.pop(0)
        if len(fields):
            tag_default_value = fields.pop(0)
    s = """
          <tr class='additional case_%s'>
            <td>
              <label class="control-label">%s</label>
            </td>
            <td>
              <input name="dyn_dyn_%s_dyn_%s" type="%s" value="%s">


    """ % (case,tag_text,case,tag,tag_type,tag_default_value)


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

    
    

