# -*- coding: utf-8 -*-
"""
Python编程：使用gensim tf-idf 对中文文本进行相似度计算
https://blog.csdn.net/mouday/article/details/87921873
"""

from __future__ import unicode_literals, print_function

import logging

import jieba
from gensim import corpora, models, similarities

jieba.setLogLevel(logging.INFO)


class DocumentSimilar(object):
    def __init__(self, documents):
        self.documents = documents
        self.dictionary = None
        self.tfidf = None
        self.similar_matrix = None
        self.calculate_similar_matrix()

    @staticmethod
    def split_word(document):
        """
        分词，去除停用词
        """
        stop_words = {":", "的", "，", "”"}

        text = []
        for word in jieba.cut(document):
            if word not in stop_words:
                text.append(word)

        logging.debug(text)

        return text

    def calculate_similar_matrix(self):
        """
        计算相似度矩阵及一些必要数据
        """
        words = [self.split_word(document) for document in self.documents]

        self.dictionary = corpora.Dictionary(words)
        corpus = [self.dictionary.doc2bow(word) for word in words]
        self.tfidf = models.TfidfModel(corpus)
        corpus_tfidf = self.tfidf[corpus]
        self.similar_matrix = similarities.MatrixSimilarity(corpus_tfidf)

    def get_similar(self, document):
        """
        计算要比较的文档与语料库中每篇文档的相似度
        """
        words = self.split_word(document)
        corpus = self.dictionary.doc2bow(words)
        corpus_tfidf = self.tfidf[corpus]
        return self.similar_matrix[corpus_tfidf]


def main():
    # 语料库
    documents = [
        "货运物流供应商Flexport完成10亿美元融资",
        "一笔300亿并购落地，一个新游戏帝国崛起",
        "讯轻科技”累计完成近千万元融资",
        "窝趣公寓完成近2亿元B轮融资主打品质和轻松社交的居住环境",
        "IBM的区块链副总裁JesseLund:比特币将达到100万美元",
    ]

    # 要比较的文档
    new_doc = "窝趣公寓完成近2亿元B轮融资"

    doc_similar = DocumentSimilar(documents)

    # 获取相似度
    similar_scores = doc_similar.get_similar(new_doc)
    print(similar_scores)
    # [0.03441829 0.         0.09512201 0.6641873  0.        ]

    # 输出完整预料和相似度
    for value, document in zip(doc_similar.get_similar(new_doc), documents):
        print("{:.2f}".format(value), document)


if __name__ == '__main__':
    main()
