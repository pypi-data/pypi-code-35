"""
Name        concurrent_insert.py
Purpose     A module for simple posting to graph server
Usage       Call the insert function with a graph name and a point to post and it will be sent to the specified server
Author      Dor Genosar (dor.genosar@outlook.com)
Change log
    2019 03 29  Created
"""


import time
import requests
import threading

url = 'https://flask-logger.herokuapp.com/'
# url = 'http://127.0.0.1:5000'
queues = dict()
interval = 1


def _uploader_function():
    print('Started uploading')
    while True:
        try:
            for graph_name, queue in queues.items():
                if len(queue) > 0:
                    requests.post(url + '/post/{}'.format(graph_name),
                                  '\n'.join('{},{}-{}'.format(x, y, label) for x, y, label in queue))
                    queues[graph_name] = []
            time.sleep(interval)
        except:
            print('upload error')

uploader = threading.Thread(target=_uploader_function)
uploader.daemon = True


def insert(graph_name, point):
    """
    Post a new point to the graph server
    :param graph_name: The name of the graph to post the point to
    :type graph_name: str
    :param point: A tuple of 3 parts: (x, y, tag)
    :type point: tuple
    """
    try:
        queues[graph_name] = queues.get(graph_name, []) + [point]
        if not uploader.is_alive():
            uploader.start()
    except:
        print('logging error')


def clear(graph):
    """
    Clear all point of a specified graph on the server
    :param graph: The name of the graph to clear
    :type graph: str
    :return: The content from the server's response
    :rtype: str
    """
    try:
        return requests.get(url + '/clear/{}'.format(graph)).content
    except:
        return 'clear error'
