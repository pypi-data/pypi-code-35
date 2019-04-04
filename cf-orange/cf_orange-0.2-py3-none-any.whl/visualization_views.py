import Orange
from django.shortcuts import render



def orng_table_to_dict(data):
    if data==None:
        raise Exception("Empty dataset")
    attrs, metas, data_new = [], [], []
    try:
        class_var = data.domain.class_var.name
    except:
        class_var = ''
    for m in data.domain.metas:
        metas.append(m[0]) #?? todo
    for a in data.domain.attributes:
        attrs.append(a.name)
    pretty_float = lambda x, a: '%.3f' % x if a is Orange.data.variable.ContinuousVariable and x!='?' else x
    for inst in range(len(data)):
        inst_new = []
        for a in data.domain.variables:
            value = data[inst][a.name].value
            inst_new.append((a.name, pretty_float(value, a)))
        for m in data.domain.metas:
            value = data[inst][m].value
            a = data.domain.get_meta(m)
            inst_new.append((a.name, pretty_float(value, a)))
        data_new.append(inst_new)
    return {'attrs':attrs, 'metas':metas, 'data':data_new, 'class_var':class_var}



def table_viewer(request, input_dict, output_dict, widget):
    data = input_dict['data']

    return render(request, 'visualizations/table_viewer.html',
                  {'widget': widget, 'input_dict': input_dict, 'output_dict': orng_table_to_dict(data)})


def odt_to_tab(request, input_dict, output_dict, widget):
    from mothra.settings import MEDIA_ROOT
    from workflows.helpers import ensure_dir
    destination = MEDIA_ROOT + '/' + str(request.user.id) + '/' + str(widget.id) + '.tab'
    ensure_dir(destination)
    input_dict['data'].save(destination)
    filename = str(request.user.id) + '/' + str(widget.id) + '.tab'
    output_dict['filename'] = filename
    return render(request, 'visualizations/string_to_file.html',
                  {'widget': widget, 'input_dict': input_dict, 'output_dict': output_dict})


def odt_to_csv(request, input_dict, output_dict, widget):
    from mothra.settings import MEDIA_ROOT
    from workflows.helpers import ensure_dir
    destination = MEDIA_ROOT + '/' + str(request.user.id) + '/' + str(widget.id) + '.csv'
    ensure_dir(destination)
    input_dict['data'].save(destination)
    filename = str(request.user.id) + '/' + str(widget.id) + '.csv'
    output_dict['filename'] = filename
    return render(request, 'visualizations/string_to_file.html',
                  {'widget': widget, 'input_dict': input_dict, 'output_dict': output_dict})


def odt_to_arff(request, input_dict, output_dict, widget):
    from mothra.settings import MEDIA_ROOT
    from workflows.helpers import ensure_dir
    destination = MEDIA_ROOT + '/' + str(request.user.id) + '/' + str(widget.id) + '.arff'
    ensure_dir(destination)
    input_dict['data'].save(destination)
    filename = str(request.user.id) + '/' + str(widget.id) + '.arff'
    output_dict['filename'] = filename
    return render(request, 'visualizations/string_to_file.html',
                  {'widget': widget, 'input_dict': input_dict, 'output_dict': output_dict})


def treeToJSON(node, path="", nodes={}):
    # made by Bogdan Okresa Duric :)

    import json

    if not node:
        return

    if path == "":  # get the dictionary prepared, insert root node
        nodes.update({  # root node properties
            "name": "root",
            # "name":node.node_classifier.class_var.name,
            "ID": node.reference(),
            "children": []
        })
        path = "['children']"  # prepare path for future use, it points into 'children' property of the root node

    if node.branch_selector:  # if the node has branches
        for n in range(len(node.branches)):  # walk through all the branches one by one
            try:
                if node.branches[n].branch_selector:  # if the node (branch) has branches
                    child = {  # set node properties
                        "name": node.branch_selector.class_var.name[:15] + " "
                                + node.branch_descriptions[n][:10],
                        "ID": node.branches[n].reference(),
                        "children": []  # stays open for future descendant nodes
                    }

                    eval("nodes" + path + ".append(" + str(child) + ")")  # write node properties
                    # 'nodes' is the dictionary
                    # path is the path to the current node, i.e. current parent node
                    # child is dictionary with node properties

                else:  # if node is a leaf
                    child = {
                        "name": node.branch_selector.class_var.name + " "
                                + node.branch_descriptions[n]
                                + ": "
                                + node.branches[n].node_classifier.default_value.value
                                + " ("
                                + str(node.branches[n].node_classifier.GetProbabilities * 100)
                                + "%)",
                        "ID": node.branches[n].reference(),
                    }
                    eval("nodes" + path + ".append(" + str(child) + ")")
            except:
                pass
        for i in range(len(node.branches)):  # go and work with the branches, one by one
            treeToJSON(node.branches[i], path + "[" + str(i) + "]" + "['children']",
                       nodes)  # work with child node, adding it's "address"
    else:  # if the node has no branches, simply return
        return

    return json.JSONEncoder().encode(nodes)  # output complete JSON description of the tree


def tree_visualization(request, input_dict, output_dict, widget):
    tc = input_dict['clt']
    tree_string = tc.print_tree() #'\n'.join(map(lambda x: x[4:], tc.print_tree().split('\n')))
    return render(request, 'visualizations/tree_visualization.html',
                  {'widget': widget, 'input_dict': input_dict, 'tree_string': tree_string})