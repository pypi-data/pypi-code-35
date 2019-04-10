#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import numpy as np
import xml.etree.ElementTree as ET


def parse_rec(filename, Price=False):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['class'] = str(obj.find('name').text)
        if Price:
            pass
            # TODO read price in prices
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(float(bbox.find('xmin').text)),
                              int(float(bbox.find('ymin').text)),
                              int(float(bbox.find('xmax').text)),
                              int(float(bbox.find('ymax').text))]
        objects.append(obj_struct)
    return objects


def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def writeXml(bbox, img_name, xml_path, write_price=False, write_score=False):

    # [ { 'width': xx ; 'depth' : xx ; 'height': xx} ; {'name' : 'class_name' ; 'bbox' : [xmin ymin xmax ymax] }  ]
    new_xml = ET.Element('annotation')
    folder = ET.SubElement(new_xml, 'folder')
    folder.text = 'VOC2007'
    filename = ET.SubElement(new_xml, 'filename')
    filename.text = img_name

    size = ET.SubElement(new_xml, 'size')
    width = ET.SubElement(size, 'width')
    width.text = bbox[0]['width']
    height = ET.SubElement(size, 'height')
    height.text = bbox[0]['height']
    depth = ET.SubElement(size, 'depth')
    depth.text = bbox[0]['depth']

    for i in range(1, len(bbox)):

        object = ET.SubElement(new_xml, 'object')
        name = ET.SubElement(object, 'name')
        name.text = str(bbox[i]['name'])

        if write_price:
            price = ET.SubElement(object, 'price')
            price.text = str(bbox[i]['price'])
        if write_score:
            score = ET.SubElement(object, 'score')
            score.text = str(bbox[i]['score'])

        difficult = ET.SubElement(object, 'difficult')
        difficult.text = '0'

        bndbox = ET.SubElement(object, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(float(bbox[i]['bbox'][0]))
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(float(bbox[i]['bbox'][1]))
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(float(bbox[i]['bbox'][2]))
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(float(bbox[i]['bbox'][3]))

    indent(new_xml)
    et = ET.ElementTree(new_xml)  # 生成文档对象
    et.write(xml_path, encoding='utf-8', xml_declaration=True)
















def main():
    pass


if __name__ == "__main__":
    main()