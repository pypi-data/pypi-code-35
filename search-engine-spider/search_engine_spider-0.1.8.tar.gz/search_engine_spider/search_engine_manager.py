# -*- coding:utf-8 -*-

import importlib
import itertools
import json
import os
import random
import sys

from numpy import median

from .search_engine import urlparse

from .config import DATA_DIR, SEARCH_ENGINE_SPIDER_DIR, file2list


class SearchEngineManager():
    '''
    search engine manager
    '''

    def __init__(self):
        self.user_agents_file = os.path.join(DATA_DIR, "user_agents.txt")
        self.user_agents = file2list(self.user_agents_file)
        self.search_engine_dir_name = "search_engine"
        self.search_engine_dir = os.path.join(SEARCH_ENGINE_SPIDER_DIR,
                                              self.search_engine_dir_name)
        self.search_engine_dict = dict()
        self.load_search_engine()

    def load_search_engine(self):
        '''
        from SEARCH_ENGINE_SPIDER_DIR/search_engine find search_engine
        '''
        for file_name in os.listdir(self.search_engine_dir):
            module_name, ext = os.path.splitext(file_name)
            if ext != ".py" or not module_name:
                continue
            module = importlib.import_module(".".join(
                (os.path.basename(SEARCH_ENGINE_SPIDER_DIR),
                 self.search_engine_dir_name, module_name)))
            search_engine_class = vars(module).get('LoadSearchEngine')
            if search_engine_class:
                search_engine = search_engine_class()
                self.search_engine_dict[
                    search_engine.get_name()] = search_engine

    def random_user_agent(self):
        '''
        random user agent
        '''
        return random.choice(self.user_agents)

    def get_search_engine(self, name):
        '''
        from name get search_engine object
        '''
        return self.search_engine_dict.get(name)

    def must_get_search_engine(self, name):
        '''
        if have not search_engine object, exit
        '''
        search_engine = self.get_search_engine(name)
        if search_engine:
            return search_engine
        print("没有该搜索引擎: " + name)
        exit(1)
        return False

    def print_search_engine(self):
        '''
        列出当前搜索引擎
        '''
        for search_engine_name in self.search_engine_dict:
            print(search_engine_name)

    def product_urls(self, engine_name, *url_file_list):
        '''
        产生该搜索引擎要搜索的url
        '''
        assert len(url_file_list) >= 1
        search_engine = self.must_get_search_engine(engine_name)
        for words in itertools.product(*map(file2list, url_file_list)):
            query_word = " ".join(words)
            print(search_engine.get_url(query_word))

    @classmethod
    def product_query(cls, *url_file_list):
        '''
        产生要搜索的query
        '''
        for words in cls.get_combination_word(*url_file_list):
            query_word = " ".join(words)
            print(query_word)

    @classmethod
    def filter_key(cls, json_result_file, max_num, *key_file_list):
        '''
        过滤出包含当前query的结果行
        '''
        keys = list()
        assert len(key_file_list) >= 1
        for words in cls.get_combination_word(*key_file_list):
            keys.append(" ".join(words))
        max_num = int(max_num)
        with open(json_result_file) as json_result_f:
            for line in json_result_f:
                line = line.strip()
                key, url, index = line.split("\t")
                index = int(index)
                if index <= max_num and key in keys:
                    print(line)

    @staticmethod
    def extract_text(search_engine,
                     content,
                     max_num,
                     first_word=None,
                     end_word=None):
        '''
        from text extract search results
        '''
        results = list()
        for index, item in enumerate(search_engine.content2items(content)):
            if index >= max_num:
                continue
            results.append(
                list(
                    filter(None,
                           (first_word, item['url'], index + 1, end_word))))
        return results

    def extract_html(self, search_engine, html_path, max_num):
        '''
        from html_path get search_results
        '''
        with open(html_path) as html_f:
            return self.extract_text(search_engine, html_f.read(), max_num)

    def extract_json(self, search_engine, json_path, max_num):
        '''
        from json_path get search_results
        '''
        with open(json_path) as json_f:
            j = json.loads(json_f.read())
            url = j["url"]
            content = j["content"]
            query = search_engine.get_query(url)
            return self.extract_text(search_engine, content, max_num, query)

    def print_extract_html(self, engine_name, html_path, max_num=10000):
        '''
        提取html内容
        '''
        max_num = int(max_num)
        search_engine = self.must_get_search_engine(engine_name)
        if os.path.isdir(html_path):
            for html_file in os.listdir(html_path):
                html_file = os.path.join(html_path, html_file)
                self.print_extract_html(engine_name, html_file, max_num)
        else:
            for item in self.extract_html(search_engine, html_path, max_num):
                print("\t".join(map(str, item)))

    def print_extract_json(self, engine_name, json_path, max_num=10000):
        '''
        提取json内容. json文件有url，content字段
        '''
        max_num = int(max_num)
        search_engine = self.must_get_search_engine(engine_name)
        if os.path.isdir(json_path):
            for json_file in os.listdir(json_path):
                json_file = os.path.join(json_path, json_file)
                self.print_extract_json(engine_name, json_file, max_num)
        else:
            for item in self.extract_json(search_engine, json_path, max_num):
                print("\t".join(map(str, item)))

    @staticmethod
    def recovery_rate(local_site_file, json_result_file, max_num=10000):
        '''
        根据本地已经有的站点和extrct-json的结果计算本地覆盖率
        '''
        local_site_set = set(file2list(local_site_file))
        search_site_dict = dict()
        with open(json_result_file) as json_result_f:
            for line in json_result_f:
                _, url, index = line.split("\t")
                if index > max_num:
                    continue
                parsed = urlparse(url)
                search_site_dict[parsed.hostname] = search_site_dict.get(
                    parsed.hostname, 0) + 1
        results = list()
        for site, items in search_site_dict.items():
            results.append([site, items, int(site in local_site_set)])
        results.sort(key=lambda x: x[1], reverse=True)
        for _ in results:
            print(" ".join(map(str, _)))

    @staticmethod
    def get_calc_func(calc_type):
        '''
        get calc func
        '''
        if calc_type == "len":
            calc_func = len
        elif calc_type == "median":
            calc_func = median
        elif calc_type == "reciprocal_median":
            calc_func = lambda x: median(map(lambda i: 1.0 / i, x))
        elif calc_type == "reciprocal_sum":
            calc_func = lambda x: sum(map(lambda i: 1.0 / i, x))
        else:
            print("error: calc_type")
            return False
        return calc_func

    @staticmethod
    def get_combination_word(*file_list, **kwargs):
        '''
        from multi file get combination words
        words_handle arg handle each words
        '''
        words_handle = kwargs.get("words_handle")
        if not words_handle:
            words_handle = lambda x: x
        combination_words = list()
        for words in itertools.product(*map(file2list, file_list)):
            if words:
                combination_words.append(words_handle(words))
        return combination_words

    def get_seed_value(self, calc_type, json_result_file, max_num,
                       *end_exclude_word_file_list):
        '''
        calculate seed value
        support len, median, reciprocal_median, reciprocal_sum
        '''
        calc_func = self.get_calc_func(calc_type)
        if not calc_func:
            return False

        max_num = int(max_num)
        exclude_words = self.get_combination_word(
            *end_exclude_word_file_list, words_handle=lambda x: (" ".join(x), len(" ".join(x))))
        exclude_words.sort(key=lambda x: x[1], reverse=True)
        search_word_dict = dict()
        '''
        {
            search_word: {
                seed: {
                    "value": 0,
                    "index_list": [index1, index2]
                }
            }
        }
        '''
        with open(json_result_file) as json_result_f:
            for _ in json_result_f:
                search_word, seed, index = _.strip().split("\t")
                index = int(index)
                if index > max_num:
                    continue
                for exclude_word, exclude_word_len in exclude_words:
                    if search_word.endswith(exclude_word):
                        search_word = search_word[:-exclude_word_len].strip()
                        break
                search_word_obj = search_word_dict.get(search_word)
                if search_word_obj is None:
                    search_word_obj = dict()
                    search_word_dict[search_word] = search_word_obj
                seed_obj = search_word_obj.get(seed)
                if seed_obj is None:
                    seed_obj = {
                        "value": 0,
                        "index_list": list(),
                    }
                    search_word_obj[seed] = seed_obj
                seed_obj["index_list"].append(index)
            for search_word, search_word_obj in search_word_dict.items():
                for seed, seed_obj in search_word_obj.items():
                    index_list = seed_obj["index_list"]
                    index_list.sort()
                    seed_obj["value"] = calc_func(index_list)
        return search_word_dict

    def seed_value(self, calc_type, json_result_file, max_num, output_dir,
                   *end_exclude_word_file_list):
        '''
        calculate seed value and print
        support len, median, reciprocal_median, reciprocal_sum
        '''
        search_word_dict = self.get_seed_value(
            calc_type, json_result_file, max_num, *end_exclude_word_file_list)
        if not search_word_dict:
            return False
        for search_word, search_word_obj in search_word_dict.items():
            seed_obj_list = list(search_word_obj.items())
            seed_obj_list.sort(key=lambda x: x[1]["value"], reverse=True)
            if output_dir == "-":
                output_file = sys.stdout
            else:
                output_file = open(os.path.join(output_dir, search_word), "w")
            for seed, seed_obj in seed_obj_list:
                seed_value = seed_obj["value"]
                index_list = seed_obj["index_list"]
                output_file.write(seed)
                output_file.write("\t")
                output_file.write(str(seed_value))
                output_file.write("\t")
                output_file.write(",".join(map(str, index_list)))
                output_file.write("\n")

            if output_file != sys.stdout:
                output_file.close()
        return True

    def get_site_value(self, calc_type, seed_calc_type, json_result_file,
                       max_num, *end_exclude_word_file_list):
        '''
        calculate site value
        support len, median, reciprocal_median, reciprocal_sum
        '''
        search_word_dict = self.get_seed_value(
            seed_calc_type, json_result_file,
            max_num * end_exclude_word_file_list)
        if not search_word_dict:
            return False
        calc_func = self.get_calc_func(calc_type)
        if not calc_func:
            return False
        search_word_site_dict = dict()
        for search_word, search_word_obj in search_word_dict.items():
            site_value_dict = dict()
            search_word_site_dict[search_word] = site_value_dict
            for seed, seed_obj in search_word_obj.item():
                hostname = urlparse(seed).hostname
                site_value_obj = site_value_dict.get(hostname)
                if not site_value_obj:
                    site_value_obj[hostname] = {
                        "value": 0,
                        "seed_value_list": list()
                    }
                site_value_obj[hostname]["seed_value_list"].append(
                    seed_obj["value"])
        for search_word, site_value_dict in search_word_site_dict.items():
            for site_value_obj in site_value_obj.values():
                site_value_obj["seed_value_list"].sort()
                site_value_obj["value"] = calc_func(
                    site_value_obj["seed_value_list"])

        return search_word_site_dict

    def site_value(self, calc_type, seed_calc_type, json_result_file, max_num,
                   output_dir, *end_exclude_word_file_list):
        '''
        calculate site value and print
        support len, median, reciprocal_median, reciprocal_sum
        '''
        search_word_site_dict = self.get_site_value(
            calc_type, seed_calc_type, json_result_file, max_num,
            *end_exclude_word_file_list)
        if not search_word_site_dict:
            return False
        for search_word, site_value_dict in search_word_site_dict.items():
            site_value_list = list(site_value_dict.items())
            site_value_list.sort(key=lambda x: x[1]["value"], reverse=True)
            with open(os.path.join(output_dir, search_word), "w") as output_f:
                for site, site_obj in site_value_list:
                    output_f.write(site)
                    output_f.write("\t")
                    output_f.write(site_obj["value"])
                    output_f.write("\n")
        return True
