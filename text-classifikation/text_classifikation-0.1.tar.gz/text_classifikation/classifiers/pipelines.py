from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, \
    TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
#from text_classifikation.features.gensim_transformers import \
#    TokenizerTransformer, LdaTransformer, Doc2BOW
from text_classifikation.features import LemmatizerTransformer, \
    POSTaggerVectorizer, NERVectorizer
from text_classifikation.features.word_vecs import Word2VecVectorizer#, \
    #Doc2VecTransformer, DocumentTransformer


def get_ngram_range(n=3):
    return CountVectorizer(ngram_range=(1, n))


pipeline__ner = Pipeline([
    ('ner', NERVectorizer())
])

pipeline__postag = Pipeline([
    ('pos_tag', POSTaggerVectorizer())
])

pipeline__unigram = Pipeline([
    ('cv', get_ngram_range(1))
])

pipeline__bigram = Pipeline([
    ('cv', get_ngram_range(2))
])

pipeline__trigram = Pipeline([
    ('cv', get_ngram_range(3))
])

pipeline__cv = pipeline__unigram
pipeline__cv2 = pipeline__bigram
pipeline__cv3 = pipeline__trigram

pipeline__lemma_cv = Pipeline([
    ("lemma", LemmatizerTransformer()),
    ('cv', CountVectorizer(min_df=.05, max_df=.4))
])
pipeline__lemma_cv2 = Pipeline([
    ("lemma", LemmatizerTransformer()),
    ('cv', get_ngram_range(2))
])
pipeline__lemma_cv3 = Pipeline([
    ("lemma", LemmatizerTransformer()),
    ('cv', get_ngram_range(3))
])

pipeline__lemma_tfidf = Pipeline([
    ("lemma", LemmatizerTransformer()),
    ('tfidf', TfidfVectorizer(min_df=.05, max_df=.4))
])

pipeline__tfidf = Pipeline([
    ('tfidf', TfidfVectorizer(min_df=.05, max_df=.4))
])
"""
pipeline__lda = Pipeline([
    ('tokenize', TokenizerTransformer()),
    ('doc2bow', Doc2BOW()),
    ('lda', LdaTransformer(num_topics=200, iterations=50))
])

pipeline__lemma_lda = Pipeline([
    ("lemma", LemmatizerTransformer()),
    ('tokenize', TokenizerTransformer()),
    ('doc2bow', Doc2BOW()),
    ('lda', LdaTransformer(num_topics=200, iterations=50))
])

pipeline__d2v = Pipeline([('doc', DocumentTransformer()),
                          ('doc2vec', Doc2VecTransformer())])


pipeline__lemma_d2v = Pipeline([
    ("lemma", LemmatizerTransformer()),
    ('doc', DocumentTransformer()),
    ('doc2vec', Doc2VecTransformer())
])
"""

pipeline__w2v = Pipeline([
    ('w2v', Word2VecVectorizer())
])

pipeline__lemma_w2v = Pipeline([
    ("lemma", LemmatizerTransformer()),
    ('w2v', Word2VecVectorizer())
])

pipeline__text = Pipeline([('cv', get_ngram_range(1)),
                           ('tfidf', TfidfTransformer())])

pipeline__text_bi = Pipeline([('cv', get_ngram_range(2)),
                              ('tfidf', TfidfTransformer())])

pipeline__text_tri = Pipeline([('cv', get_ngram_range(3)),
                               ('tfidf', TfidfTransformer())])

pipeline__lemma_text = Pipeline([('lemma', LemmatizerTransformer()),
                                 ('cv', get_ngram_range(1)),
                                 ('tfidf', TfidfTransformer())])

pipeline__lemma_text_bi = Pipeline([('lemma', LemmatizerTransformer()),
                                    ('cv', get_ngram_range(2)),
                                    ('tfidf', TfidfTransformer())])

pipeline__lemma_text_tri = Pipeline([('lemma', LemmatizerTransformer()),
                                     ('cv', get_ngram_range(3)),
                                     ('tfidf', TfidfTransformer())])
default_pipelines = {
    'cv': pipeline__cv,
    'cv2': pipeline__cv2,
    'cv3': pipeline__cv3,
    'tfidf': pipeline__tfidf,
    'tfidf2': pipeline__text_bi,
    'tfidf3': pipeline__text_tri,
    # 'lda': pipeline__lda,
    'w2v': pipeline__w2v,
    # 'd2v': pipeline__d2v,
    'cv_lemma': pipeline__lemma_cv,
    'cv2_lemma': pipeline__lemma_cv2,
    'cv3_lemma': pipeline__lemma_cv3,
    'tfidf_lemma': pipeline__lemma_tfidf,
    # 'lda_lemma': pipeline__lemma_lda,
    'w2v_lemma': pipeline__lemma_w2v,
    # 'd2v_lemma': pipeline__lemma_d2v,
    # 'text': pipeline__text,
    'tfidf2_lemma': pipeline__lemma_text_bi,
    'tfidf3_lemma': pipeline__lemma_text_tri,
    'postag': pipeline__postag,
    'ner': pipeline__ner
}


def generate_unions(pipelines=None, independent_components=None, deep=True):
    pipelines = pipelines or default_pipelines

    independent_components = independent_components or {
        "cv": ("cv", "cv2", "cv3", "cv_lemma", "cv2_lemma", "cv3_lemma"),
        "tfidf": ("tfidf", "tfidf2", "tfidf3", "tfidf_lemma", "tfidf2_lemma",
                  "tfidf3_lemma"),
        "w2v": ("w2v", "w2v_lemma"),
        "postag": ("postag"),
        "ner": ("ner")
    }
    pipeline_unions = {}

    for c in independent_components:
        others = [co for co in independent_components if co != c]
        for f in independent_components[c]:
            if f not in pipelines:
                continue
            for o in others:
                for s in independent_components[o]:
                    if s not in pipelines or f == s:
                        continue
                    name = f + "_" + s
                    inv_name = s + "_" + f
                    if inv_name in pipeline_unions:
                        continue
                    pipeline_unions[name] = FeatureUnion([
                        (f, pipelines[f]),
                        (s, pipelines[s])
                    ])
    if deep:
        for f in list(pipeline_unions.keys()):
            for o in independent_components:
                for s in independent_components[o]:
                    if s not in pipelines or o in f:
                        continue
                    name = f + "_" + s
                    inv_name = s + "_" + f
                    if inv_name in pipeline_unions:
                        continue
                    pipeline_unions[name] = FeatureUnion([
                        (f, pipeline_unions[f]),
                        (s, pipelines[s])
                    ])
    return pipeline_unions


default_pipeline_unions = generate_unions(default_pipelines)
