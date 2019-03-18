#coding: utf8
from __future__ import absolute_import
import os
from flask import request, g
from farbox_lite.utils import same_slash
from farbox_lite.compiler.site import get_site_doc, update_site_doc
from farbox_lite.utils.lazy import get_value_from_data


sites = {}


# webserver 运行之前, 进行的构建
def create_site(site_folder, site_folder_name=''):
    site_folder = same_slash(site_folder)
    site_doc = get_site_doc(site_folder)
    if not site_doc:
        return {}# ignore

    domains = get_value_from_data(site_doc, 'domains', [])
    if not isinstance(domains, (list, tuple)):
        domains = []
    for domain in domains:
        domain = domain.strip().lower()
        domain = domain.split('://')[-1]
        domain = domain.strip('/').split('/')[0]
        if '.' not in domain and domain not in ['localhost']:
            break
        key =  domain
        sites[key] = site_doc

    if site_folder_name and site_folder_name not in sites:
        sites[site_folder_name] = site_doc

    return sites



def create_sites(site_folders_root):
    # 一个 folder 左右所有 sites 的集合
    if not os.path.isdir(site_folders_root):
        return
    sub_names = os.listdir(site_folders_root)
    for sub_name in sub_names:
        if sub_name.startswith('.') or sub_name.startswith('~'):
            continue
        site_path = os.path.join(site_folders_root, sub_name)
        site_folder_name = sub_name.lower().strip()
        if os.path.isdir(site_path):
            create_site(site_path, site_folder_name=site_folder_name)


def get_site_from_domain(domain):
    if ':' in domain:
        domain = domain.split(':')[0]
    domain = domain.lower()

    # os.environ first!
    site_folder_name = os.environ.get('farbox_lite_site_folder_name')
    if site_folder_name:
        matched_site_doc = sites.get(site_folder_name.lower().strip())
        if matched_site_doc:
            return matched_site_doc

    site_doc = sites.get(domain) or sites.get(domain.replace('www.', '')) or sites.get('www.'+domain)
    if site_doc:
        return site_doc

    # 仍然没有, 则默认 hit 一个
    for k, site_doc in sites.items():
        if site_doc.get('template_resources'):
            return site_doc



def get_site_from_request():
    g_site = getattr(g, 'site', None)
    if g_site:
        site = g_site
    else:
        site = get_site_from_domain(request.host)
        g.site = site
    return site


def get_sites():
    return sites




