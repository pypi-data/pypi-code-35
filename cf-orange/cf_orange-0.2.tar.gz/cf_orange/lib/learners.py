import Orange
from Orange.classification import NaiveBayesLearner, KNNLearner, SVMLearner, CN2Learner, TreeLearner, \
    LogisticRegressionLearner, MajorityLearner, RandomForestLearner
from Orange.data import Table, Domain


def orange_build_classifier(input_dict):
    learner = input_dict['learner']
    data = input_dict['data']

    classifier = learner(data)

    output_dict = {'classifier': classifier}

    return output_dict


def orange_apply_classifier(input_dict):
    classifier = input_dict['classifier']
    data = input_dict['data']

    Y=classifier(data)

    new_data=Table.from_numpy(data.domain, data.X, Y=Y,metas=data.metas)

    # new_domain = Domain(data.domain, classifier(data[0]).class_variable)
    # new_domain.add_metas(data.domain.get_metas())
    #
    # new_data = Table(new_domain, data)
    #
    # for i in range(len(data)):
    #     c = classifier(data[i])
    #     new_data[i][c.variable.name] = c
    #
    output_dict = {'data': new_data}

    return output_dict


# ORANGE CLASSIFIERS (update imports when switching to new orange version)

def orange_bayes(input_dict):
    output_dict = {}
    output_dict['bayesout'] = NaiveBayesLearner()
    return output_dict


def orange_knn(input_dict):
    output_dict = {}
    output_dict['knnout'] = KNNLearner()
    return output_dict


# def orange_rules(input_dict):
#     output_dict = {}
#     output_dict['rulesout'] = RuleLearner(name="Rule Learner (Orange)")
#     return output_dict


def orange_cn2(input_dict):
    output_dict = {}
    output_dict['cn2out'] = CN2Learner()
    return output_dict


def orange_svm(input_dict):
    output_dict = {}
    output_dict['svmout'] = SVMLearner() #name='SVM (Orange)')
    return output_dict


# def orange_svmeasy(input_dict):
#     output_dict = {}
#     output_dict['svmeasyout'] = SVMLearnerEasy(name='SVMEasy (Orange)')
#     return output_dict


def orange_class_tree(input_dict):
    output_dict = {}
    output_dict['treeout'] = TreeLearner() #name="Classification Tree (Orange)")
    return output_dict


# def orange_c45_tree(input_dict):
#     output_dict = {}
#     output_dict['c45out'] = C45Learner(name="C4.5 Tree (Orange)")
#     return output_dict


def orange_logreg(input_dict):
    output_dict = {}
    output_dict['logregout'] = LogisticRegressionLearner() #name="Logistic Regression (Orange)")
    return output_dict


def orange_majority_learner(input_dict):
    output_dict = {}
    output_dict['majorout'] = MajorityLearner() #name="Majority Classifier (Orange)")
    return output_dict


# def orange_lookup_learner(input_dict):
#     output_dict = {}
#     output_dict['lookupout'] = LookupLearner(name="Lookup Classifier (Orange)")
#     return output_dict


def orange_random_forest(input_dict):
    # from workflows.helpers import UnpicklableObject
    output_dict = {}
    # rfout = UnpicklableObject("orngEnsemble.RandomForestLearner(trees=" + input_dict['n'] + ", name='RF" + str(
    #     input_dict['n']) + " (Orange)')")
    # rfout.addimport("import orngEnsemble")
    # output_dict['rfout'] = rfout
    output_dict['rfout']= RandomForestLearner(n_estimators=input_dict['n']) #, name='RF' + str(input_dict['n']) + " (Orange)")
    return output_dict


# HARF (HIGH AGREEMENT RANDOM FOREST)

# def orange_harf(input_dict):
#     # import orngRF_HARF
#     from workflows.helpers import UnpicklableObject
#     agrLevel = input_dict['agr_level']
#     # data = input_dict['data']
#     harfout = UnpicklableObject(
#         "orngRF_HARF.HARFLearner(agrLevel =" + agrLevel + ", name='HARF-" + str(agrLevel) + "')")
#     harfout.addimport("import orngRF_HARF")
#     # harfLearner = HARFLearner(agrLevel = agrLevel, name = "_HARF-"+agrLevel+"_")
#     output_dict = {}
#     output_dict['harfout'] = harfout
#     return output_dict


# CLASSIFICATION NOISE FILTER

# def orange_classification_filter(input_dict, widget):
#     import noiseAlgorithms4lib
#     output_dict = {}
#     output_dict['noise_dict'] = noiseAlgorithms4lib.cfdecide(input_dict, widget)
#     return output_dict


def orange_send_filename(input_dict):
    output_dict = {}
    output_dict['filename'] = input_dict['fileloc'].strip('\"').replace('\\', '\\\\')
    return output_dict

# SATURATION NOISE FILTER

def orange_saturation_filter(input_dict, widget):
    import noiseAlgorithms4lib
    output_dict = {}
    output_dict['noise_dict'] = noiseAlgorithms4lib.saturation_type(input_dict, widget)
    return output_dict


# NOISE RANK

def orange_noiserank(input_dict):
    allnoise = {}
    data = input_dict['data']
    for item in input_dict['noise']:
        det_by = item['name']
        for i in item['inds']:
            if not allnoise.has_key(i):
                allnoise[i] = {}
                allnoise[i]['id'] = i
                allnoise[i]['class'] = data[int(i)].getclass().value
                allnoise[i]['by'] = []
            allnoise[i]['by'].append(det_by)
            print
            allnoise[i]['by']

    from operator import itemgetter
    outallnoise = sorted(allnoise.values(), key=itemgetter('id'))
    outallnoise.sort(compareNoisyExamples)

    output_dict = {}
    output_dict['allnoise'] = outallnoise
    output_dict['selection'] = {}
    return output_dict


def orange_compareNoisyExamples(item1, item2):
    len1 = len(item1["by"])
    len2 = len(item2["by"])
    if len1 > len2:  # reversed, want to have decreasing order
        return -1
    elif len1 < len2:  # reversed, want to have decreasing order
        return 1
    else:
        return 0


def orange_noiserank_select(postdata, input_dict, output_dict):
    try:
        output_dict['indices'] = outselection = [int(i) for i in postdata['selected']]
        data = input_dict['data']
        selection = [0] * len(data)
        for i in outselection:
            selection[i] = 1
        outdata = data.select(selection, 1)
        output_dict['selection'] = outdata
    except KeyError:
        output_dict['selection'] = None

    return output_dict


# EVALUATION OF NOISE DETECTION PERFORMANCE

def orange_add_class_noise(input_dict):
    import noiseAlgorithms4lib
    output_dict = noiseAlgorithms4lib.insertNoise(input_dict)
    return output_dict


def orange_aggr_results(input_dict):
    output_dict = {}
    output_dict['aggr_dict'] = {'positives': input_dict['pos_inds'], 'by_alg': input_dict['detected_inds']}
    return output_dict


def orange_eval_batch(input_dict):
    alg_perfs = input_dict['perfs']
    beta = float(input_dict['beta'])
    performances = []
    for exper in alg_perfs:
        noise = exper['positives']
        nds = exper['by_alg']

        performance = []
        for nd in nds:
            nd_alg = nd['name']
            det_noise = nd['inds']
            inboth = set(noise).intersection(set(det_noise))
            recall = len(inboth) * 1.0 / len(noise) if len(noise) > 0 else 0
            precision = len(inboth) * 1.0 / len(det_noise) if len(det_noise) > 0 else 0

            print
            beta, recall, precision
            if precision == 0 and recall == 0:
                fscore = 0
            else:
                fscore = (1 + beta ** 2) * precision * recall / ((beta ** 2) * precision + recall)
            performance.append(
                {'name': nd_alg, 'recall': recall, 'precision': precision, 'fscore': fscore, 'fbeta': beta})

        performances.append(performance)

    output_dict = {}
    output_dict['perf_results'] = performances
    return output_dict


def orange_eval_noise_detection(input_dict):
    noise = input_dict['noisy_inds']
    nds = input_dict['detected_noise']

    performance = []
    for nd in nds:
        nd_alg = nd['name']
        det_noise = nd['inds']
        inboth = set(noise).intersection(set(det_noise))
        recall = len(inboth) * 1.0 / len(noise) if len(noise) > 0 else 0
        precision = len(inboth) * 1.0 / len(det_noise) if len(det_noise) > 0 else 0
        beta = float(input_dict['f_beta'])
        print
        beta, recall, precision
        if precision == 0 and recall == 0:
            fscore = 0
        else:
            fscore = (1 + beta ** 2) * precision * recall / ((beta ** 2) * precision + recall)
        performance.append({'name': nd_alg, 'recall': recall, 'precision': precision, 'fscore': fscore, 'fbeta': beta})

    from operator import itemgetter
    output_dict = {}
    output_dict['nd_eval'] = sorted(performance, key=itemgetter('name'))
    return output_dict


def orange_avrg_std(input_dict):
    perf_results = input_dict['perf_results']
    stats = {}
    # Aggregate performance results
    n = len(perf_results)
    for i in range(n):
        for item in perf_results[i]:
            alg = item['name']
            if not stats.has_key(alg):
                stats[alg] = {}
                stats[alg]['precisions'] = [item['precision']]
                stats[alg]['recalls'] = [item['recall']]
                stats[alg]['fscores'] = [item['fscore']]
                stats[alg]['fbeta'] = item['fbeta']
            else:
                stats[alg]['precisions'].append(item['precision'])
                stats[alg]['recalls'].append(item['recall'])
                stats[alg]['fscores'].append(item['fscore'])

            # if last experiment: compute averages
            if i == n - 1:
                stats[alg]['avrg_pr'] = reduce(lambda x, y: x + y, stats[alg]['precisions']) / n
                stats[alg]['avrg_re'] = reduce(lambda x, y: x + y, stats[alg]['recalls']) / n
                stats[alg]['avrg_fs'] = reduce(lambda x, y: x + y, stats[alg]['fscores']) / n

    # Compute Standard Deviations
    import numpy
    avrgstdout = []
    print
    stats
    for alg, stat in stats.items():
        avrgstdout.append({'name': alg, 'precision': stat['avrg_pr'], 'recall': stat['avrg_re'],
                           'fscore': stat['avrg_fs'],
                           'fbeta': stat['fbeta'],
                           'std_pr': numpy.std(stat['precisions']),
                           'std_re': numpy.std(stat['recalls']),
                           'std_fs': numpy.std(stat['fscores'])})

    from operator import itemgetter
    output_dict = {}
    output_dict['avrg_w_std'] = sorted(avrgstdout, key=itemgetter('name'))
    return output_dict




# FILE LOADING

def orange_uci_to_odt(input_dict):
    from mothra.settings import FILES_FOLDER
    output_dict = {}
    output_dict['data'] = Table("iris") #FILES_FOLDER + "uci-datasets/" + input_dict['filename'])
    return output_dict


def orange_odt_to_arff(input_dict):
    from noiseAlgorithms4lib import toARFFstring
    output_dict = {}
    f = toARFFstring(input_dict['odt'])
    output_dict['arff'] = f.getvalue()
    return output_dict


def orange_string_to_file(input_dict):
    return {}


def orange_alter_table(input_dict):
    return {'altered_data': None}


def orange_alter_table_finished(postdata, input_dict, output_dict):
    import Orange
    from Orange.feature import Type
    from visualization_views import orng_table_to_dict
    widget_id = postdata['widget_id'][0]
    # Parse the changes
    altered_cells = json.loads(postdata['alteredCells' + widget_id][0])
    new_table = Orange.data.Table(input_dict['data'])
    for cell, new_value in altered_cells.items():
        tokens = cell.split('_')
        inst_idx, att = int(tokens[1]), str(tokens[2])
        if new_table[inst_idx][att].var_type == Type.Continuous:
            new_table[inst_idx][att] = float(new_value)
        else:  # Discrete or string
            # TODO:
            # This raises an exception if new_value is not among the legal values for the discrete attribute
            # - add a dropdown list of legal values when editing the table!
            try:
                new_table[inst_idx][att] = str(new_value)
            except:  # Catch orange exception and give a proper error message.
                raise Exception("Illegal value '%s' for discrete attribute '%s', legal values are: %s." % (
                new_value, att, new_table.domain[att].values))
    return {'altered_data': new_table}


def orange_tree_visualization(input_dict):
    return {}


def orange_example_distance(input_dict):
    return input_dict


def orange_example_distance_post(postdata, input_dict, output_dict):
    return {}


def orange_createBlaString():
    return "bla";


import hashlib


def orange_hash_it(input_dict):
    output_dict = {}
    output_dict["output1"] = hashlib.sha256(input_dict["input1"]).hexdigest()
    output_dict["numLoop"] = input_dict["numLoop"]
    for i in range(1, input_dict["numLoop"]):
        output_dict["output1"] = hashlib.sha256(output_dict["output1"]).hexdigest();
    return output_dict
