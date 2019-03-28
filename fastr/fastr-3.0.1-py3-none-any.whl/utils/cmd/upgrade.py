# Copyright 2011-2014 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from collections import namedtuple
from copy import deepcopy

import fastr
from fastr import exceptions
from fastr.core.version import Version
from fastr.utils.cmd import add_parser_doc_link
FASTR_LOG_TYPE = 'none'  # Do not get info about fastr


class dummy_container:
    def __getitem__(self, value):
        return value


FastrNamespaceType = namedtuple('FastrNamespaceType', ['toollist', 'typelist'])


EVAL_GLOBALS = {
    'fastr': FastrNamespaceType(dummy_container(), dummy_container())
}


def get_parser():
    parser = argparse.ArgumentParser(
        description="Extract selected information from the extra job info. The path"
                    " is the selection of the data to retrieve. Every parts of the"
                    " path (separated by a /) is seen as the index for the previous"
                    " object. So for example to get the stdout of a job, you could use"
                    " 'fastr cat __fastr_extra_job_info__.json process/stdout'."
    )
    parser.add_argument('infile', metavar='NETWORK.py', help='Network creation file (in python) to upgrade')
    parser.add_argument('outfile', metavar='NEW.py', help='location of the result file')
    return parser


def find_tool(toolspec):
    if isinstance(toolspec, str):
        namespace = None
        toolname = toolspec
        version = None
    elif isinstance(toolspec, tuple):
        if len(toolspec) == 2:
            toolname, version = toolspec
            namespace = None
        elif len(toolspec) == 3:
            namespace, toolname, version = toolspec
        else:
            raise exceptions.FastrToolUnknownError(f'Cannot use illegal tool spec {toolspec} with len {len(toolspec)}')
    else:
        raise exceptions.FastrToolUnknownError(
            f'Invalid toolspec {toolspec} type to find a tool, must be str or tuple, got a {type(toolspec).__name__}'
        )

    if version is None and '/' in toolname:
        toolname, version = toolname.split('/', 1)

    if namespace is None and '.' in toolname:
        namespace, toolname = toolname.rsplit('.', 1)

    if isinstance(version, str):
        version = Version(version)

    if namespace:
        namespace = '/'.join(namespace.split('.'))

    matching_tools = [t for t in fastr.tools.values() if t._id == toolname and
                      (version is None or t.command_version == version) and
                      (namespace is None or t.namespace == namespace)]

    if not matching_tools:
        raise exceptions.FastrToolUnknownError('Could not find tool: {}/{}:{}'.format(
            namespace or '$NAMESPACE',
            toolname,
            version or '$VERSION'
        ))

    matching_tools.sort(key=lambda x: (x.command_version, x.version), reverse=True)

    return matching_tools[0]


def upgrade(infile, outfile):
    try:
        from redbaron import RedBaron
    except ImportError:
        print("The upgrade command needs the redbaron package which is currently not installed. "
              "Please install the package.\n\nExample using pip:\n  $ pip install redbaron")
        return

    fastr.log.info('Loading input file...')
    with open(infile, 'r') as file_handle:
        code_file = RedBaron(file_handle.read())

    # Add import of resourcelimit
    fastr.log.info('Adding ResourceLimit import')
    for node in code_file.find_all('ImportNode', value=lambda x: x.dumps() == 'fastr'):
        node.insert_after('from fastr.api import ResourceLimit')

    # Replace all fastr.Network by fastr.create_network
    fastr.log.info('Updating network creation...')
    matches = code_file.find_all('AtomtrailersNode', value=lambda x: x.dumps().startswith('fastr.Network'))
    network_id = None
    for match in matches:
        if match.value[1].value != 'Network':
            continue

        match.value[1] = 'create_network'

        # Save the network id for later use
        for nr, subnode in enumerate(match.value[2]):
            if (subnode.target is None and nr == 0) or subnode.target.value == 'id_':
                network_id = eval(subnode.value.dumps(), EVAL_GLOBALS, {})

    # Change arguments for functions
    fastr.log.info('Updating method arguments...')
    for arg in code_file.find_all('CallArgumentNode'):
        if arg.target and arg.target.value == 'id_':
            arg.target.value = 'id'

        if arg.target and arg.target.value in ['nodegroup', 'sourcegroup']:
            arg.target.value = 'node_group'

        if arg.target and arg.target.value in ['stepid']:
            arg.target.value = 'step_id'

    # Add tool version and update tool name
    fastr.log.info('Updating create_node to include more version info...')
    for node in code_file.find_all('CallNode'):
        if node.previous.value == 'create_node':
            tool = eval(node.value[0].dumps(), EVAL_GLOBALS, {})
            tool = find_tool(tool)
            fastr.log.info('Found tool {}'.format(tool))

            node.value[0].value = "'{}'".format(tool.ns_id)
            full_syntax = node.fst()
            if len(full_syntax['value']) < 3:
                raise ValueError('Cannot understand indentation of:\n{}'.format(node))

            # Get comma spec
            if len(full_syntax['value']) < 4:
                comma = deepcopy(full_syntax['value'][1])
            else:
                comma = deepcopy(full_syntax['value'][3])

            # Get call argument spec
            if not full_syntax['value'][2]['target']:
                full_syntax['value'][2]['target'] = {'type': 'name', 'value': 'id'}
            extra_arg = deepcopy(full_syntax['value'][2])

            if comma['type'] != 'comma' or extra_arg['type'] != 'call_argument':
                raise ValueError('Cannot understand syntax of:\n{}'.format(node))

            # Adapt call spec to correct values
            extra_arg['target']['value'] = 'tool_version'
            extra_arg['value']['value'] = f"'{tool.version}'"

            # Insert and rebuild
            full_syntax['value'].insert(2, extra_arg)
            full_syntax['value'].insert(3, comma)
            node.replace(node.from_fst(full_syntax))

            # Get resource limits
            args = []
            to_remove = []
            for subnode in node.value:
                if subnode.target is not None and subnode.target.value == 'cores':
                    args.append(f'cores={subnode.value}')
                    to_remove.append(subnode)

                if subnode.target is not None and subnode.target.value == 'memory':
                    args.append(f'memory={subnode.value}')
                    to_remove.append(subnode)

                if subnode.target is not None and subnode.target.value == 'walltime':
                    args.append(f'time={subnode.value}')
                    to_remove.append(subnode)

            for subnode in to_remove:
                node.remove(subnode)

            if len(args) > 0:
                node.value.append('resources=ResourceLimit({})'.format(', '.join(args)))

    # Update draw_network -> draw and all argument changes
    fastr.log.info('Updating network draw to to new syntax...')
    for node in code_file.find_all('CallNode'):
        if node.previous.value != 'draw_network':
            continue

        node.previous.value = 'draw'

        name = network_id
        parsed_name = True
        img_format = 'svg'
        parsed_img_format = True
        file_path_node = None
        img_format_node = None
        for nr, subnode in enumerate(node.value):
            if (subnode.target is None and nr == 0) or (subnode.target is not None and subnode.target.value == 'name'):
                try:
                    name = eval(subnode.value.dumps(), EVAL_GLOBALS, {})
                except Exception:
                    name = subnode.value.dumps()
                    parsed_name = False

                file_path_node = subnode

            if (subnode.target is None and nr == 1) or (subnode.target is not None and subnode.target.value == 'img_format'):
                try:
                    img_format = eval(subnode.value.dumps(), EVAL_GLOBALS, {})
                except Exception:
                    img_format = subnode.value.dumps()
                    parsed_img_format = False

                img_format_node = subnode

            if (subnode.target is None and nr == 2) or (subnode.target is not None and subnode.target.value == 'draw_dimension'):
                subnode.target = 'draw_dimensions'

            if (subnode.target is None and nr == 3) or (subnode.target is not None and subnode.target.value == 'expand_macro'):
                subnode.target = 'expand_macros'

        # Construct correct file_path value
        if parsed_name and parsed_img_format:
            file_path_value = "'{}.{}'"
        elif parsed_name and not parsed_img_format:
            file_path_value = "'{}.' + {}"
        elif not parsed_name and parsed_img_format:
            file_path_value = "{} + '.{}'"
        else:
            file_path_value = "{} + '.' + {}"

        file_path_value = file_path_value.format(name, img_format)

        # Replace name and format arguments with the file_path argument
        if file_path_node is not None:
            file_path_node.replace("file_path={}".format(file_path_value))

        if img_format_node is not None:
            if file_path_node is not None:
                node.remove(img_format_node)
            else:
                img_format_node.replace("file_path={}".format(file_path_value))

    fastr.log.info('Writing output file...')
    with open(outfile, 'w') as output_file_handle:
        output_file_handle.write(code_file.dumps())


def main():
    """
    Print information from a job file
    """
    # No arguments were parsed yet, parse them now
    parser = add_parser_doc_link(get_parser(), __file__)
    args = parser.parse_args()
    try:
        upgrade(args.infile, args.outfile)
    except exceptions.FastrToolUnknownError as exception:
        print('[ERROR] {}'.format(exception))


if __name__ == '__main__':
    main()
