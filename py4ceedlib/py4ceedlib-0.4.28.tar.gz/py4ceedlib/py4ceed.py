import ipywidgets as widgets
import difflib
import requests
import pandas as pd
import os
from os.path import expanduser
import subprocess
import warnings
import sys
import nbconvert
import nbformat
from nbconvert import HTMLExporter
import time


base_url='https://4ceed.illinois.edu'

warnings.filterwarnings("ignore")


# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it
this.meta_data = None
this.credentials = None
this.key = None
this.validated_credentials = False

def set_base_url(url):
    this.base_url = url
    if this.base_url[-1] == '/':
        this.base_url = this.base_url[:-1]

def print_base_url():
    print(this.base_url)


########### Start  API calls to 4Ceed  with API Key ################
def test_credentials(key):

    url = '%s/api/collections?key=%s' % (base_url, key)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        print("Successfully validated credentials")
        this.validated_credentials = True
        this.key = key
    else:
        raise ValueError('Invalid credentials, please try again')
        this.validated_credentials = False


def get_all_spaces(key):
    url = '%s/api/spaces?key=%s' % (base_url, key)
    return requests.get(url, verify=False).json()

def get_all_collections(key):
    url = '%s/api/collections?key=%s' % (base_url, key)
    colls = requests.get(url, verify=False).json()
    detailed_colls = []
    for coll in colls:
        detailed_coll = get_collection_by_id(coll['id'],key)
        detailed_colls.append(detailed_coll)
    return detailed_colls

def get_collection_by_id(coll_id, key):
    url = '%s/api/collections/%s?key=%s' % (base_url, coll_id, key)
    #url = '%s/api/collections/%s' % (base_url, coll_id)
    return requests.get(url, verify=False).json()

def get_collections_for_space(space_id,key):
    url = '%s/api/spaces/%s/collections?key=%s' % (base_url, space_id, key)
    colls = requests.get(url, verify=False).json()
    detailed_colls = []
    for coll in colls:
        detailed_coll = get_collection_by_id(coll['id'],key)
        detailed_colls.append(detailed_coll)
    return detailed_colls


def get_datasets_for_collection(coll_id, key):
    url = '%s/api/collections/%s/datasets?key=%s' % (base_url, coll_id, key)
    return requests.get(url, verify=False).json()

def get_datasets_for_space(space_id, key):
    url = '%s/api/spaces/%s/datasets?key=%s' % (base_url, space_id, key)
    return requests.get(url, verify=False).json()

def get_files_for_dataset(dataset_id, key):
    url = '%s/api/datasets/%s/files?key=%s' % (base_url, dataset_id, key)
    return requests.get(url, verify=False).json()

def get_text_metadata(file_id, file_path, key):
    url = '%s/api/files/%s/?key=%s' % (base_url, file_id, key)
    file_data = requests.get(url, verify=False)
    df = parse_txt_metadata(file_data.text, file_id, file_path)
    return df

def get_template_by_dataset_id(dataset_id, key):
    url = '%s/t2c2/templates/getByDatasetId/%s?key=%s' % (base_url, dataset_id, key)
    return requests.get(url, verify=False).json()



def save_notebook(filename, save_as=''):

    #get home directory
    home = expanduser("~")

    #append ipynb if not there
    if '.ipynb' not in filename:
        filename += '.ipynb'

    #check outputfile name
    if save_as:
        if '.ipynb' not in filename:
            save_as += '.ipynb'
    else:
        save_as = filename

    #find notebook path
    notebook_path = ''
    for r, d, f in os.walk(home):
        for files in f:
            if files == filename:
                notebook_path = os.path.join(r, files)

    if not notebook_path:
        print("Could not find notebook with the name ", filename)
    #print(notebook_path)

    # read raw contents
    with open(notebook_path, 'r') as content_file:
        content = content_file.read()

    # read in nbformat
    ipynb_content = nbformat.read(notebook_path, as_version=4)


    #create html exporter
    html_exporter = HTMLExporter()
    html_exporter.template_file = 'basic'

    #convert to .html
    (html_body, resources) = html_exporter.from_notebook_node(ipynb_content)
    #subprocess.call(["jupyter", "nbconvert", notebook_path, "--to", "html"])
    #html_notebook_path = os.path.dirname(notebook_path) + '/' + filename.replace('ipynb','html')

    #read contents of html
    #with open(html_notebook_path, 'r') as content_file:
        #htmlcontent = content_file.read()

    #print(htmlcontent)

    data = dict()
    data["notebookName"] = save_as
    data["htmlNotebookContent"] = str(html_body)
    data["notebookContent"] = content

    url = '%s/api/notebook/submit?key=%s' % (base_url, this.key)
    resp = requests.post(url, data, verify=False)
    print(resp)
    if resp.status_code == 200:
        print(resp.json())
    else:
        print(resp.reason)


########### End  API calls to 4Ceed  with API key ################


######################Create the GUI #########################
def create_tree_for_collection(coll, dic_for_tree, tree_items, credentials, space=False, show_files=False):

    current_coll_id = coll['id']
    if current_coll_id in dic_for_tree:
        return
    dic_for_tree[current_coll_id] = coll
    dic_for_tree[current_coll_id]['datasets'] = dict()


    collection_accordions = []
    collection_names = []
    if space:
        # get space datasets
        list_datasets = get_datasets_for_space(coll['id'], credentials)

        # get space collections
        space_collections = get_collections_for_space(coll['id'], credentials)
        for space_coll in space_collections:
            coll_accordion = create_tree_for_collection(space_coll, dic_for_tree, tree_items, credentials)
            if coll_accordion:
                collection_accordions.append(coll_accordion)
                display_name = space_coll['name'] + u'\t\t(Collection)' #+ (20 - len(space_coll['name']) ) * ' ' + 'Space'
                #print("Display_name=", display_name)
                collection_names.append(display_name)
    else:
        # get collection datasets
        list_datasets = get_datasets_for_collection(coll['id'], credentials)

        #get child collections
        child_coll_ids = coll['child_collection_ids'] #val[val.find("(")+1:val.find(")")]
        str_child_coll_ids = child_coll_ids[child_coll_ids.find("(")+1:child_coll_ids.find(")")]
        if str_child_coll_ids:
            child_coll_ids = str_child_coll_ids.split(', ')
            for child_coll_id in child_coll_ids:
                try:
                    child_coll = get_collection_by_id(child_coll_id, credentials)
                    coll_accordion = create_tree_for_collection(child_coll, dic_for_tree, tree_items, credentials)
                    if coll_accordion:
                        collection_accordions.append(coll_accordion)
                        display_name = child_coll['name'] + u'\t\t(Collection)' # + (20 - len(child_coll['name'])) * ' ' + 'Space'
                        #print("Display_name=", display_name)
                        collection_names.append(display_name)
                except: # if not authorized to see child collection of a shared collection
                    pass

    # build the multi select widget for datasets
    dataset_info = []
    dataset_names = []
    for dataset in list_datasets:
        dic_for_tree[current_coll_id]['datasets'][dataset['id']] = dataset
        dic_for_tree[current_coll_id]['datasets'][dataset['id']]['files'] = dict()
        dataset_info.append((dataset['id'], dataset['name'], dataset['created']))
        dataset_names.append(dataset['name'])
    datasets_widget = multi_checkbox_widget(dataset_names)
    if dataset_names:
        tree_items.append( (datasets_widget, dataset_info) )

    #create accordon for current collections and datasets
    if dataset_names:
        children = collection_accordions + [datasets_widget]
    else:
        children = collection_accordions
    accordion = widgets.Accordion(children=children)
    for i in range(0, len(collection_names)):
        accordion.set_title(i, collection_names[i])
    if dataset_names:
        accordion.set_title(len(children) - 1, 'datasets')

    return accordion


def build_tree_view(key, show_files=False):
    ## Populate the ree
    dic_for_tree = dict()
    tree_items = []

    first_level_widgets = []
    first_level_names = []
    list_spaces = get_all_spaces(key)
    for space in list_spaces:
        #if "GaN" in space['name']:
        space_widget = create_tree_for_collection(space, dic_for_tree, tree_items, key, space=True, show_files=show_files)
        if space_widget:
            first_level_widgets.append(space_widget)
            first_level_names.append(space["name"] + u'\t\t(Space)')

    list_collection = get_all_collections(key)
    for collection in list_collection:
        coll_widget = create_tree_for_collection(collection, dic_for_tree, tree_items, key, show_files=show_files)
        if coll_widget:
            first_level_widgets.append(coll_widget)
            first_level_names.append(collection["name"] + u'\t\t(Collection)')

    accordion = widgets.Accordion(children=first_level_widgets)
    for i in range(0, len(first_level_names)):
        accordion.set_title(i, first_level_names[i])
    #accordion.set_title(len(collection_accordions) - 1, 'datasets')

    display(accordion)

    button = widgets.Button(description="Submit")
    display(button)
    #future_checked_items = asyncio.Future()
    checked_items = []

    def on_button_clicked(change):
        #see checked items
        checked_items = []  # reset the checked items
        for item in tree_items:
            widget = item[0]
            dataset_info = item[1]
            check_boxes = widget.children[0]
            for i in range (0,len(check_boxes.children)):
                if check_boxes.children[i].value:
                    checked_items.append(dataset_info[i])

        if not checked_items:
            print("Please choose some datasets and try again")
        else:
            this.meta_data = display_data_frame(checked_items, key)
            display(this.meta_data)

    button.on_click(on_button_clicked)

def display_data_frame(checked_items, credentials):
    meta_data_df = pd.DataFrame()

    for dataset_id, dataset_name, upload_data in checked_items:

        dataset_template = get_template_by_dataset_id(dataset_id, credentials)
        one_dataset_metadata = dict()
        if not dataset_template or len(dataset_template) == 0:
            sys.stderr.write("Dataset " + dataset_name + " has no metadata\n")
            continue
        for term in dataset_template[0]["terms"]:
            if '-----' not in term['default_value']:
                #append the unit to the column name
                #if '-----' not in term['units']:
                #    col_name = term['key'] + ' [' + term['units'] + ']'
                #else:
                #    col_name = term['key']
                try:
                    one_dataset_metadata[col_name] = float(term['default_value'])
                except:
                    one_dataset_metadata[col_name] = term['default_value']
        df = pd.DataFrame(one_dataset_metadata, index=[dataset_name, ])
        meta_data_df = pd.concat([meta_data_df, df], axis=0, ignore_index=False)

    # fix column names
    if not meta_data_df.empty:
        meta_data_df.columns = meta_data_df.columns.str.strip().str.replace(u'\xa0', '_').str.replace('(', '').str.replace(
        ')', '')

        print("Done Retrieving ... ")

    return meta_data_df

def read_datasets_metadata():
    if not this.validated_credentials:
        print("Credentials are not validated, please execute py4ceed.enter_credentials() to enter your credentials")
        return
    print("Retrieving datasets ... ")
    build_tree_view(this.key, show_files=False)

def get_metadeta():
    return this.meta_data

def multi_checkbox_widget(descriptions):
    """ Widget with a search field and lots of checkboxes """
    #search_widget = widgets.Text()
    options_dict = {description: widgets.Checkbox(description=description, value=False) for description in descriptions}
    options = [options_dict[description] for description in descriptions]
    options_widget = widgets.VBox(options, layout={'overflow': 'scroll'})
    #multi_select = widgets.VBox([search_widget, options_widget])
    multi_select = widgets.VBox([options_widget])

    # Wire the search field to the checkboxes
    def on_text_change(change):
        search_input = change['new']
        if search_input == '':
            # Reset search field
            new_options = [options_dict[description] for description in descriptions]
        else:
            # Filter by search field using difflib.
            close_matches = difflib.get_close_matches(search_input, descriptions, cutoff=0.0)
            new_options = [options_dict[description] for description in close_matches]
        options_widget.children = new_options

    #search_widget.observe(on_text_change, names='value')
    return multi_select


# API key Widget
def enter_key():
    key_widget = widgets.Text(
        value='',
        description='User Key:',
        disabled=False
    )



    def on_cred_button_clicked(change):
        # test that credentials works
        text_key = key_widget.value
        test_credentials(text_key)



    display(key_widget)

    button = widgets.Button(description="Submit")
    display(button)

    button.on_click(on_cred_button_clicked)






