#!/usr/bin/env python
import os
import ast
from csr_cloud.csr_cloud import csr_cloud as cloud
import logging
from os.path import expanduser
import json

logger = logging.getLogger('HA')
node_file = expanduser("~") + '/cloud/HA/node_file'


class NodeTable:
    md = None

    def __doc__(self):
        "This class represents a list of redundancy nodes"

    def __init__(self): #pragma: no cover
        self.nodes = []
        self.c = cloud('HA')
        self.node_file = node_file
        self.read_table_from_file()

    def create_node(self, params):
        response_json = {}
        # Check if the node already exists
        node_index = params['index']
        node = self.find_node(node_index)
        if node != None:
            # Node already exists. Just update its parameters
            return self.set_params(params)

        # Ask cloud specific code to create a node from the input parameters
        node = self.c.ha.create_node(params)

        self.nodes.append(node)
        self.write_table_to_file()
        self.c.log.info("Created new node with index {}".format(node_index))
        response_json['code'] = 200
        response_json['msg'] = "Successfully created new node with index {} \n{}".format(node_index, json.loads(self.show_node(node))['msg'])
        return json.dumps(response_json)


    def set_params(self, new_params):
        response = {}
        response['msg'] = ""
        response['code'] = 200
        node_index = new_params['index']
        node = self.find_node(node_index)
        if node == None:
            self.c.log.info("Node with index %s not found" % node_index)
            resp = self.create_node(new_params)
            node = self.find_node(node_index)
        else:
            for param in new_params.keys():
                node[param] = new_params[param]
            self.write_table_to_file()
            self.c.log.info("Set parameters on node with index %s" % node_index)
        if node:
            response = self.c.ha.validate_set_param_inputs(node, new_params)
            response['msg'] = response['msg'] + "\n200: Updated node {} Successfully".format(node_index)

        return json.dumps(response)

    def clear_params(self, old_params):
        response_json = {}
        node_index = ''
        i = 0
        for token in old_params:
            if token == '-i':
                node_index = old_params[i + 1]
                break
            i = i + 1

        node = self.find_node(node_index)
        if node == None:
            self.c.log.error("Node with index {} not found".format(node_index))
            response_json['code'] = 400
            response_json['msg'] = "Node with index {} not found".format(node_index)
            return json.dumps(response_json)

        i = 1
        while i < len(old_params):
            keyword = " "
            if old_params[i] == '-i':
                # Can not clear the index parameter
                keyword = "dummy"
                i = i + 1
            else:
                if "-m" in old_params[i]:
                    keyword = "mode"
                else:
                    keyword = self.c.ha.check_clear_param(i, old_params)
            if keyword == " ":
                self.c.log.info("Invalid parameter format {}".format(old_params[i]))
            if keyword in node:
                del node[keyword]
            i = i + 1

        self.write_table_to_file()
        self.c.log.info("Cleared parameters on node with index {}".format(node_index))
        response_json['code'] = 200
        response_json['msg'] = "Cleared parameters on node with index {}".format(node_index)
        return json.dumps(response_json)

    def delete_node(self, param):
        response_json = {}
        node_index = param['index']
        node = self.find_node(node_index)
        if node == None:
            self.c.log.error("Node with index {} not found".format(node_index))
            response_json['code'] = 400
            response_json['msg'] =  "Node with index {} not found".format(node_index)
            return json.dumps(response_json)

        self.nodes.remove(node)
        self.write_table_to_file()
        self.c.log.info("Deleted node with index {}".format(node_index))
        response_json['code'] = "200"
        response_json['msg'] = "Successfully deleted node {}".format(node_index)
        return json.dumps(response_json)

    def find_node(self, index):
        for node in self.nodes:
            # Find the existing node
            if node['index'] == index:
                self.c.log.info("node: {}".format(node))
                return node
        return None

    def show_node(self, param):
        response_json = {}
        # Parameter should only be the node index
        node_index = param['index']
        node = self.find_node(node_index)
        if node == None:
            response_json['code'] = 400
            response_json['msg'] = "Node with index {} not found".format(node_index)
            return json.dumps(response_json)

        node_str = "Redundancy node configuration:\n"
        for key in node:
            param_str = "{:15s}{} \n".format(key, node[key])
            node_str = node_str + param_str

        response_json['code'] = 200
        response_json['msg'] = node_str
        return json.dumps(response_json)

    def show_table(self):
        response_json = {}
        total_nodes = ""
        if self.nodes:
            for node in self.nodes:
                total_nodes += "\nRedundancy node configuration:\n"
                for key in node:
                    total_nodes += "{:15s}{} \n".format(key, node[key])
            response_json['code'] = 200
            response_json['msg'] = total_nodes
            return json.dumps(response_json)
        response_json['code'] = 400
        response_json['msg'] = "No redundancy nodes found"
        return json.dumps(response_json)


    def write_table_to_file(self):
        with open(self.node_file, 'w') as write_fh:
            for node in self.nodes:
                out_str = str(node) + '\n'
                write_fh.write(out_str)

    def read_table_from_file(self):
        if os.path.exists(self.node_file):
            with open(self.node_file, 'r') as read_fh:
                for line in read_fh:
                    input_str = line.strip()
                    node = ast.literal_eval(input_str)
                    self.create_node(node)
