from __future__ import division, unicode_literals
import datetime, math
import urllib, operator
import function as fn
import numpy as np
import timeit
import operator
from . import connection as con
from . import gsearch
import random
import multiprocessing as mp
import platform
from .config import getConfig
from functools import partial
from .Tfidf import MyTfidfVectorizer
from .Symbiotic import Symbiotic
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
from furl import furl
from pprint import pprint


def collectOutlinks(globalDict, webpage):
    try:
        webpage.extract_outlinks(globalDict['output_prefix'])
        return webpage
    except Exception as ex:
        print str(ex)

class Population:
    def __init__(self, _crawlingQueue, _query):
        self.generation = 1
        self.query = fn.preprocess(_query)

        # list URL dari 1 populasi
        # semua outlink dari individuals
        self.listUrl = []

        # individuals isinya tipe data Webpage
        self.individuals = []

        # list. crawling queue yang akan diproses
        self.crawlingQueue = _crawlingQueue

        # tfidf matrix
        self.tfidf_matrix = None

        # topic-specific weight table
        self.weight_table = []

        self.relevant_count = 0

        self.DICT = {}
        
        self.fitness_history = []

        self.start = True


    def calcFitness(self):
        tfidf = MyTfidfVectorizer(decode_error='ignore')
        corpus = [ind.text for ind in self.individuals]

        tfidf_matrix = tfidf.fit_transform(corpus)
        feature_names = tfidf.get_feature_names()

        # create specific weight table
        if(self.generation == 1):
            # feature_index = tfidf_matrix[0,:].nonzero()[1]
            feature_index = range(tfidf.vocabulary_.__len__())

            # tuple index, weight
            tfidf_scores = zip(feature_index, [max(tfidf_matrix[:, x]).data.item() for x in feature_index])

            weight_table = []
            # append query to weight table with max weight
            for q in self.query.split():
                weight_table.append((q, float(1.0)))

            # normalize weight
            Wmax = max(tfidf_scores, key=operator.itemgetter(1))[1]
            for i, w in tfidf_scores:
                _scores = w / Wmax
                if (_scores >= getConfig('crawler', 'topic_keyword') and feature_names[i] not in self.query.split()):
                    weight_table.append((feature_names[i], _scores))

            # sort by weight
            # weight_table = sorted(
            #     weight_table, reverse=True, key=operator.itemgetter(1))
            self.weight_table.extend(weight_table)

        # calculate fitness from each page
        for i, webpage in enumerate(self.individuals):
            webpage_weight = []
            for k, w in self.weight_table:
                key_index = tfidf.vocabulary_.get(k)
                wk = tfidf_matrix[i, key_index] if key_index is not None else 0

                # weighting scheme
                wk *= getConfig('crawler', 'weight_text', float)
                if k in webpage.title.split():
                    wk += getConfig('crawler', 'weight_title', float)*wk
                webpage_weight.append(wk)

            # normalize weight
            Wmax = max(webpage_weight)
            if(Wmax > 0):
                webpage_weight = np.array([x / Wmax for x in webpage_weight])
            else:
                webpage_weight = np.array(webpage_weight)

            webpage.tfidf_matrix = tfidf_matrix[i]
            webpage.fitness = cosine_similarity(
                np.array(self.weight_table)[:, 1].reshape(1, -1),
                webpage_weight.reshape(1, -1)).flatten()[0]
            webpage.fitness += getConfig('crawler', "webpage_fitness_bias", float)

            # save webpage according to relevancy
            if webpage.fitness >= getConfig('crawler', "relevance_score", float):
                self.relevant_count += 1
                webpage.save_db(self.DICT['output_prefix'])
            else:
                webpage.save_trash(self.DICT['output_prefix'])

        # add most frequent keyword from  fitness page
        for i, webpage in enumerate(self.individuals):
            if (webpage.fitness >= getConfig('crawler', "min_fitness_extract", float)
                    and self.generation > 1):

                _best_keyword1 = np.argmax(webpage.tfidf_matrix.toarray())
                best_keyword = feature_names[_best_keyword1]

                # _best_keyword = np.argmax()
                # best_keyword = Counter(el for el in webpage.text.split(" ")).most_common(1)[0][0]
                if best_keyword not in [x for x,_ in self.weight_table]:
                    self.weight_table.append((best_keyword, webpage.fitness))
                    print "Added Keyword: " + str(best_keyword)

        best_webpage = max(self.individuals, key=operator.attrgetter('fitness'))
        print "Crawled: ", (str(self.individuals.__len__()))
        print "Best Fitness: ", (str(best_webpage.fitness))
        print ""

        pprint(self.weight_table)

        # stop if konvergen
        self.fitness_history.append(best_webpage.fitness)
        if(len(self.fitness_history) > 3) {
            self.fitness_history.pop(0)
            avg_last_fitness = sum(self.fitness_history) / len(self.fitness_history)
            if(avg_last_fitness < 0.5) self.start = False
            self.avg_last_fitness = avg_last_fitness
        }


    def generate(self):
        print "Generation: ", (str(self.generation))
        print "--------------------------------"

        # hitung fitness setiap individu
        self.calcFitness()

        # survived page from fitness
        count = getConfig('GA', "ga.max_survived_pages", int)
        if self.generation > 1:
            # buat list individu baru
            _individuals = []

            maxFitness = max(
                self.individuals, key=operator.attrgetter('fitness')).fitness
            for i in range(count):
                _ = fn.acceptReject(self.individuals, maxFitness)

                # for unique selection, remove selected
                # self.individuals.remove(_)
                _individuals.append(_)
            self.individuals = _individuals

        # collect all outbond link from survived pages
        globalDict = {'output_prefix': self.DICT['output_prefix']}
        listUrl = []
        p = mp.Pool(mp.cpu_count())
        # use set for optimization
        # results = p.map(collectOutlinks, set(self.individuals))
        results = p.map(partial(collectOutlinks, globalDict), set(self.individuals))
        p.close()

        # get outlinks from mapping
        for w in results:
            for outlinks in w.outlinks:
                listUrl.append(outlinks)

        # assign outlinks to individuals
        for i, w in enumerate(self.individuals):
            for r in results:
                if r == w:
                    self.individuals[i].outlinks = r.outlinks
                    break

        # for webpage in self.individuals:
        #     webpage.extract_outlinks()
        #     listUrl.extend(webpage.outlinks)

        # calculate fitness each outlinks
        # update old URL fitness
        for i, (url, fitness) in enumerate(self.listUrl):
            for page in self.individuals:
                if url in [x for x, _ in page.outlinks]:
                    self.listUrl[i][1] += page.fitness

        # calculate fitness remaining URL
        preventDuplicates = [x for x,_ in self.listUrl]
        weight_table_text = ' '.join([x for x, _ in self.weight_table])
        for url, href_text in listUrl:
            if url in preventDuplicates: continue
            _fitness = 0

            for page in self.individuals:
                if url in [x for x,_ in page.outlinks]:
                    _fitness += page.fitness

            _fitness += fn.get_jaccard_sim(weight_table_text, href_text) * (
                0.5 * getConfig('GA', "ga.max_crawling_queue", int))
            self.listUrl.append([url, _fitness])
            preventDuplicates.append(url)

        # sort crawlingqueue berdasarkan fitness
        # tuple (url, fitness)
        # crawlingQueue = sorted(
        #     crawlingQueue, key=lambda x: x[1], reverse=True)

        self.crawlingQueue = []
        maxFitness = max(self.listUrl, key=operator.itemgetter(1))[1]
        for i in range(getConfig('GA', "ga.max_crawling_queue", int)):
            if not self.listUrl: break
            _ = fn.acceptReject(self.listUrl, maxFitness, attribute=False)
            self.listUrl.remove(_)
            self.crawlingQueue.append(_[0])

        if random.random() < getConfig('GA', "ga.mutation_rate", float):
            print 'Doing Mutation...'
            self.mutate()

        # convert to np array url only
        # self.crawlingQueue = [x for x, _ in crawlingQueue][:getConfig("GA_MAX_CRAWLING_QUEUE")]

        # clear individual array
        self.individuals = []

        # iterasi generasi
        self.generation += 1

    def mutate(self):
        # mutasi SOS
        # START SOS ALGORITHM

        # create SOS object
        sos = Symbiotic(self.query)

        # generate sos chromosome
        # list of document from GA


        # np vector
        # X = tfidf.fit_transform([x.text for x in self.individuals])

        word_population = []
        for k in sos.query:
            word_population.append(k)

        for webpage in self.individuals:
            best_keyword = Counter(el for el in webpage.text.split(" ")).most_common(1)

            for k,_ in best_keyword:
                if k not in word_population:
                    word_population.append(k)

        _gen = [1 if term in sos.query else 0 for term in word_population]
        sos.set_keyword_document(word_population)
        sos.set_query(_gen)

        for webpage in self.individuals:
            _ = Counter(el for el in webpage.text.split(" ")).most_common(5)
            best_keyword = [x for x,_ in _]

            _gen = [1 if term in best_keyword else 0 for term in word_population]
            sos.append(_text=webpage.text, _gen=_gen)

        # iterate with sos
        while sos.generation < getConfig('SOS', "sos.max_generation", int):
            if sos.best.fitness >= getConfig('SOS', "sos.max_fitness", float):
                break
            sos.generate()

        new_query = sos.query_best
        print "New Query to search: " + new_query
        # crawl from google with new query
        results = gsearch.search(new_query, self.DICT['domain'])
        if results is None: return

        for url in results:
            if fn.check_url(url, con, self.DICT['output_prefix']):
                if url not in self.crawlingQueue:
                    self.crawlingQueue.append(url)

    def append(self, _webpage):
        self.individuals.append(_webpage)

    @property
    def last(self):
        if(len(self.individuals) == 0):
            raise RuntimeError
        return self.individuals[-1]

    @property
    def first(self):
        if(len(self.individuals) == 0):
            raise RuntimeError
        return self.individuals[0]

    @property
    def count(self):
        return len(self.individuals)

class Webpage:
    """ Webpage """

    def __init__(self, _url, _soup):
        self.url = _url
        self.outlinks = []
        self.fitness = 0
        self.tfidf_matrix = []
        self.soup = _soup

    def set_text(self, _text):
        # self.text_origin = _text
        self.text = _text

    def set_title(self, _text):
        self.title = _text

    def save_db(self, output_prefix):
        con.insert_page(str(self.url), str(self.title), str(self.text), output_prefix)

    def save_trash(self, output_prefix):
        con.trash_page(str(self.url), output_prefix)

    def extract_outlinks(self, output_prefix):
        preventDuplicates = []
        for url in self.soup.find_all('a', href=fn.filter_links):
            try:
                _url = url['href']
                if _url in preventDuplicates: continue
                preventDuplicates.append(_url)
                _url = furl(_url).remove(args=True, fragment=True).url
                href_text = fn.get_href_text(_url)

                if fn.check_url(_url, con, output_prefix, href_text):
                    self.outlinks.append((_url, href_text))

            except Exception as ex:
                print str(ex)
                pass

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)