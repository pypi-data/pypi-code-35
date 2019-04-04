#!/usr/bin/env python
from __future__ import print_function
import glob
from array import array
import pandas as pd
from . import io
from . import root_wrapper as rootw
import alphatwirl
import os
import collections
# import math
from jinja2 import Template
# import functools


class Analysis:

    analysis_name = ""
    version = ""
    dataset = ""
    luminosity = 0.

    regions = []

    categories_df = ""
    categories_pattern = []
    categories = {}

    data_names_df = ""
    data_input_df = ""
    data_names_dc = ""

    signals = []
    backgrounds = []
    systematics = []

    def __init__(self, config_file):

        with open(config_file, "r") as infile:
            import yaml
            cfg = yaml.load(infile)
            self.analysis_name = str(cfg["general"]["analysis_name"])
            self.version = str(cfg["general"]["version"])
            self.dataset = str(cfg["general"]["dataset"])
            self.luminosity = float(cfg["general"]["luminosity"])
            self.regions = cfg["regions"]["regions"]

            self.data_names_df = str(cfg["data"]["data_names_df"])
            self.data_input_df = str(cfg["data"]["input_df"])
            self.data_names_dc = str(cfg["data"]["data_names_dc"])

            self.signals = cfg["signals"]
            self.backgrounds = cfg["backgrounds"]
            self.systematics = cfg["systematics"]


def getCategorization(myAnalysis):

    df_name = ""
    for signal in myAnalysis.signals:
        df_name = signal["input_df"]
        continue

    df = io.custom_pd_read_table(
        df_name,
        dtype={
            'variable_low': str,
            'variable_high': str})

    groupByList = ["category", "region", "variable"]
    groups = df.groupby(groupByList)

    categories = {}

    for name, group in groups:
        sorted_bins = sorted(
            group["variable_low"].tolist() + group["variable_high"].tolist())
        sorted_bins = list(set(sorted_bins))
        if name[groupByList.index("category")] not in categories:
            categories[name[groupByList.index("category")]] = {}
        list1 = sorted(list(group["variable_low"].tolist()))
        list2 = sorted(list(group["variable_high"].tolist()))
        binning = list1 + list2
        binning_tmp = [float(i) for i in binning if i != "inf"]
        binning_tmp = sorted(list(set(binning_tmp)))
        binning_tmp = [str(i) for i in binning_tmp]
        binning_tmp2 = ["inf" for i in binning if str(i) == "inf"]
        binning = sorted(list(set(binning_tmp + binning_tmp2)))

        categories[name[groupByList.index("category")]][name[groupByList.index("region")]] = [
            name[groupByList.index("variable")], binning]

    return categories


def createHisto(name, binning):

    histo = rootw.TH1F(name, name, len(binning) - 1, array('f', binning))

    return histo


def createDictionary(myAnalysis, categories, type_processes):

    if type_processes == "signals":
        list_processes = myAnalysis.signals
    elif type_processes == "backgrounds":
        list_processes = myAnalysis.backgrounds
    elif type_processes == "data":
        list_processes = ["data"]

    histDict = {}

    for category in categories:

        histDict[category] = {}

        for region in myAnalysis.regions:

            histDict[category][region] = {}

            for process in list_processes:

                if type_processes == "backgrounds":

                    allowed_region = []
                    for i, value in enumerate(myAnalysis.backgrounds):
                        if myAnalysis.backgrounds[i]["name"] != process["name"]:
                            continue
                        allowed_region = myAnalysis.backgrounds[i]["regions"]

                    if region not in allowed_region:
                        continue

                if type_processes != "data":
                    histDict[category][region][process["name"]] = {}
                else:
                    histDict[category][region]["data"] = {}

    return histDict


def fillDictionary(myAnalysis, histDictionary, type_processes, categories):
    """ Fills the histograms within the dictionary with yield values from the dataframes.
    Histograms are stored in the output root datacards and their integrals used in the output txt datacards
        :param myAnalysis instance of Analysis, holds configuration
        :param histDictionary initialized with histograms that need to be filled
        :param type_processes is "signals", "backgrounds", or "data" and determines the dictionary to be filled
    """

    # histDictionary is a nested dict of TH1: histDictionary[category][region][process][systematic] = TH1
    if type_processes == "signals":
        list_processes = myAnalysis.signals
    elif type_processes == "backgrounds":
        list_processes = myAnalysis.backgrounds
    elif type_processes == "data":
        list_processes = ["data"]

    # loop on processes
    for process in list_processes:

        # opening corresponding dataframe
        name_df = ""
        if type_processes != "data":
            name_df = process["input_df"]
        else:
            name_df = myAnalysis.data_input_df

        df = pd.read_csv(name_df, delim_whitespace=True)
        if type_processes != "data":
            print("  -> processing", process["name"], " =", name_df)
        else:
            print("  -> processing data =", name_df)

        # getting the right process
        if type_processes != "data":
            df = df[df["process"] == process["name"]].copy()
        else:
            df = df[df["process"] == myAnalysis.data_names_df].copy()

        if "data" not in list_processes:
            process_name = process["name"]
        else:
            process_name = "data"

        # droping process column as we are now restricted to one process
        df = df.drop(["process"], axis=1)

        # summing content and quadratically summing errors
        df["error"] = df["error"] * df["error"]
        df = df.groupby(['region', 'category', 'systematic', 'variable_low', 'variable_high'])[
            "content", "error"].sum().reset_index(drop=False)
        df["error"] = df["error"]**0.5

        # removing groupby columns
        cols = [c for c in df.columns if "level_" not in c]
        df = df[cols]

        # group to match dictionary structure
        groupByList = [
            "region",
            "category",
            "systematic"]

        grouped = df.groupby(groupByList)

        # looping on groups
        for name, group in grouped:

            category = name[groupByList.index("category")]
            region = name[groupByList.index("region")]
            systematic = name[groupByList.index("systematic")]

            # getting number arrays for
            n_array = group["content"].values
            # e_array = group["error"].values

            binning = categories[category][region][1]
            binning_tmp = [float(i) for i in binning if i != "inf"]
            binning_tmp2 = [max(binning_tmp) +
                            300. for i in binning if str(i) == "inf"]
            binning = sorted(list(set(binning_tmp + binning_tmp2)))

            # if histogram is a systematics shape variation, create it on the fly
            # if (systematic != "nominal") and ("Formula" not in systematic):

            if process_name not in histDictionary[category][region].keys():
                continue

            if ("Formula" not in systematic):
                histDictionary[category][region][process_name][systematic] = createHisto(
                    process_name + "_" + category + "_" + region + "_" + systematic, binning)

            # if histogram for this process & systematic is found, fill it using root_numpy array2hist
            # if systematic in histDictionary[category][region][process_name].keys():
            if "Formula" not in systematic:
                rootw.array2hist(
                    n_array, histDictionary[category][region][process_name][systematic])

    # returning filled dictionary
    return histDictionary


def writeHistos(myAnalysis, histograms, this_type):

    for process in histograms:
        for systematic in histograms[process]:
            histo = histograms[process][systematic]
            if process != "data":
                histo.Scale(myAnalysis.luminosity)
            if histo.Integral() < 1E-12:
                if this_type != "data":
                    histo.SetBinContent(1, 1E-12)
                    histo.SetBinError(1, (1E-12)**2.)
            if this_type == "data":
                histo.Write(myAnalysis.data_names_dc)
            elif this_type == "signals":
                if systematic == "nominal":
                    histo.Write(process)
                else:
                    histo.Write(
                        process + "_" + systematic.replace("_Up", "Up").replace("_Down", "Down"))
            else:
                if systematic == "nominal":
                    histo.Write(process)
                else:
                    histo.Write(
                        process + "_" + systematic.replace("_Up", "Up").replace("_Down", "Down"))
    return


def writeRootDatacards(myAnalysis, sigHistDictionary, bkgHistDictionary, dataHistDictionary):

    outDir = "out_" + myAnalysis.analysis_name + "_" + \
        myAnalysis.dataset + "_" + myAnalysis.version + "/"
    if os.path.isdir(outDir):
        if len(glob.glob(outDir + "*.root")) != 0:
            for file in glob.glob(outDir + "*.root"):
                os.remove(file)
    else:
        os.mkdir(outDir)

    for category in dataHistDictionary:
        outRoot = outDir + category.replace("::", "_") + "_shapes.root"
        f = rootw.Open(outRoot, 'RECREATE')

        for region in dataHistDictionary[category]:

            if "nominal" in dataHistDictionary[category][region]["data"]:
                if len(dataHistDictionary[category][region]["data"]["nominal"]) == 0:
                    continue
            else:
                continue

            savdir = rootw.GetDirectory(rootw.GetPath())
            if not f.GetDirectory(region):
                savdir.mkdir(region)
            f.cd(region)

            writeHistos(
                myAnalysis, dataHistDictionary[category][region], "data")
            writeHistos(
                myAnalysis, sigHistDictionary[category][region], "signals")
            writeHistos(
                myAnalysis, bkgHistDictionary[category][region], "backgrounds")

            adir_1 = f.GetDirectory(region)
            adir_1.cd("..")
    return


def writeTxtDatacards(myAnalysis, sigHistDictionary, bkgHistDictionary, dataHistDictionary):

    outDir = "out_" + myAnalysis.analysis_name + "_" + \
        myAnalysis.dataset + "_" + myAnalysis.version + "/"

    if len(glob.glob(outDir + "*.txt")) != 0:
        for file in glob.glob(outDir + "*.txt"):
            os.remove(file)

    name_df = myAnalysis.data_input_df

    for category in dataHistDictionary:
        outTxt = outDir + category.replace("::", "_") + "_higgsDataCard.txt"
        outRoot = category.replace("::", "_") + "_shapes.root"

        local_df = pd.read_csv(name_df, delim_whitespace=True)
        local_df = local_df[local_df["category"] == category].copy()
        groups = local_df.groupby(["variable"])
        local_variable = ""
        for name, group in groups:
            local_variable = name
            break

        with open(outTxt, 'w') as text_file:

            write_dc_header(text_file, outRoot)
            write_dc_data_section(text_file, category, dataHistDictionary)
            write_dc_processes_section(
                text_file, category, dataHistDictionary, sigHistDictionary, bkgHistDictionary)
            write_dc_rate_section(
                text_file, category, dataHistDictionary, sigHistDictionary, bkgHistDictionary)
            write_dc_systematics_section(text_file, myAnalysis, local_variable, category,
                                         dataHistDictionary, sigHistDictionary, bkgHistDictionary)


def write_dc_header(text_file, outRoot):

    text_file.write("imax    *     number of categories\n")
    text_file.write("jmax    *     number of samples minus one\n")
    text_file.write("kmax    *     number of nuisance parameters\n")
    text_file.write(
        "-------------------------------------------------------------------------------\n")
    text_file.write("shapes * * " + outRoot +
                    " $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC")
    text_file.write("\n")
    text_file.write("\n")

    return


def write_dc_data_section(text_file, category, dataHistDictionary):

    t = Template("{% for n in list %}{{n}}\t" "{% endfor %}")

    text_file.write("bin\t ")

    this_list = []
    for region in dataHistDictionary[category]:
        if "nominal" in dataHistDictionary[category][region]["data"]:
            if len(dataHistDictionary[category][region]["data"]["nominal"]) != 0:
                this_list += [region]
    text_file.write(t.render(list=this_list))

    text_file.write("\n")
    text_file.write("observation\t")

    text_file.write(t.render(list=[str(int(dataHistDictionary[category][region]["data"]["nominal"].Integral()))
                                   for region in dataHistDictionary[category]
                                   if "nominal" in dataHistDictionary[category][region]["data"]]))

    text_file.write("\n")
    text_file.write(
        "-------------------------------------------------------------------------------\n")

    return


def write_dc_processes_section(text_file, category, dataHistDictionary, sigHistDictionary, bkgHistDictionary):

    t = Template("{% for n in list %}{{n}}\t" "{% endfor %}")

    text_file.write("bin\t")

    this_list = []

    for region in dataHistDictionary[category]:
        list_keys = list(sigHistDictionary[category][region].keys())
        list_keys += list(bkgHistDictionary[category][region].keys())

        for process in list_keys:
            if "nominal" in dataHistDictionary[category][region]["data"]:
                if len(dataHistDictionary[category][region]["data"]["nominal"]) != 0:
                    this_list.append(region)

    text_file.write(t.render(list=this_list))

    text_file.write("\n")
    text_file.write("\n")
    text_file.write("process\t ")

    this_list = []

    for region in dataHistDictionary[category]:
        list_keys = list(sigHistDictionary[category][region].keys())
        list_keys += list(bkgHistDictionary[category][region].keys())

        for process in list_keys:
            if "nominal" in dataHistDictionary[category][region]["data"]:
                if len(dataHistDictionary[category][region]["data"]["nominal"]) != 0:
                    this_list.append(process)

    text_file.write(t.render(list=this_list))

    text_file.write("\n")
    text_file.write("process\t ")

    this_list = []

    for region in dataHistDictionary[category]:
        if "nominal" in dataHistDictionary[category][region]["data"]:
            if len(dataHistDictionary[category][region]["data"]["nominal"]) != 0:
                this_list += [str(number)
                              for number in range(-len(sigHistDictionary[category][region]) + 1, 1)]
                this_list += [str(number) for number in range(1,
                                                              1 + len(bkgHistDictionary[category][region]))]

    text_file.write(t.render(list=this_list))

    text_file.write("\n")


def write_dc_rate_section(text_file, category, dataHistDictionary, sigHistDictionary, bkgHistDictionary):

    t = Template("{% for n in list %}{{n}}\t" "{% endfor %}")

    text_file.write("rate\t ")

    this_list = []

    for region in dataHistDictionary[category]:
        for process in sigHistDictionary[category][region]:
            if dataHistDictionary[category][region]["data"]:
                value = sigHistDictionary[category][region][process]["nominal"].Integral(
                )
                if value < 1E-12:
                    value = 1E-12
                this_list.append(str(value))
        for process in bkgHistDictionary[category][region]:
            if dataHistDictionary[category][region]["data"]:
                value = bkgHistDictionary[category][region][process]["nominal"].Integral(
                )
                if value < 1E-12:
                    value = 1E-12
                this_list.append(str(value))

    text_file.write(t.render(list=this_list))

    text_file.write("\n")
    text_file.write(
        "-------------------------------------------------------------------------------\n")


def write_dc_systematics_section(text_file, myAnalysis, local_variable,
                                 category, dataHistDictionary, sigHistDictionary, bkgHistDictionary):

    nameSysts = {}

    for systematic in myAnalysis.systematics:
        if (systematic["type"] != "lnN") and (systematic["type"] != "lnU"):
            continue
        if systematic["name"] + "::" + systematic["type"] not in nameSysts:
            nameSysts[systematic["name"] + "::" + systematic["type"]] = {}
        thisDict = {}
        for process in systematic["apply_to"]:
            value = "-"
            condition = True
            if ("variable==" + local_variable not in str(systematic["when"])):
                condition = False
            if str(systematic["when"]) == "True":
                condition = True

            value = str(systematic["value"])

            if "signals" in process:
                for process2 in myAnalysis.signals:
                    if condition:
                        thisDict[process2["name"]] = value
            elif "backgrounds" in process:
                for process2 in myAnalysis.backgrounds:
                    if condition:
                        thisDict[process2["name"]] = value
            else:
                if condition:
                    thisDict[process] = value

        if systematic["name"] + "::" + systematic["type"] not in nameSysts:
            nameSysts[systematic["name"] + "::" +
                      systematic["type"]] = thisDict
        else:
            nameSysts[systematic["name"] + "::" + systematic["type"]] = dict(nameSysts[
                systematic["name"] + "::" + systematic["type"]].items() + thisDict.items())

    for region in dataHistDictionary[category]:
        for process in sigHistDictionary[category][region]:
            for systematic2 in sigHistDictionary[category][region][process]:
                thisDict = {}
                if systematic2 == "nominal":
                    continue
                thisDict[process] = "1"
                if systematic2.replace("_Up", "").replace("_Down", "") + "::" + "shape" not in nameSysts:
                    nameSysts[systematic2.replace("_Up", "").replace(
                        "_Down", "") + "::" + "shape"] = thisDict
                else:
                    nameSysts[systematic2.replace("_Up", "").replace("_Down", "") + "::" + "shape"] = dict(nameSysts[
                        systematic2.replace("_Up", "").replace("_Down", "") +
                        "::" + "shape"].items() + thisDict.items())
        for process in bkgHistDictionary[category][region]:
            for systematic2 in bkgHistDictionary[category][region][process]:
                thisDict = {}
                if systematic2 == "nominal":
                    continue
                thisDict[process] = "1"
                if systematic2.replace("_Up", "").replace("_Down", "") + "::" + "shape" not in nameSysts:
                    nameSysts[systematic2.replace("_Up", "").replace(
                        "_Down", "") + "::" + "shape"] = thisDict
                else:
                    nameSysts[systematic2.replace("_Up", "").replace("_Down", "") + "::" + "shape"] = dict(nameSysts[
                        systematic2.replace("_Up", "").replace("_Down", "") +
                        "::" + "shape"].items() + thisDict.items())

    nameSysts = collections.OrderedDict(sorted(nameSysts.items()))

    t = Template("{% for n in list %}{{n}}\t" "{% endfor %}")

    for syst in nameSysts:

        this_list = []

        this_list.append(syst.replace("::", " "))

        for region in dataHistDictionary[category]:
            if not dataHistDictionary[category][region]["data"]:
                continue

            list_keys = list(sigHistDictionary[category][region].keys())
            list_keys += list(bkgHistDictionary[category][region].keys())

            for process in list_keys:
                if process in sigHistDictionary[category][region]:
                    if process in nameSysts[syst]:
                        this_list.append(nameSysts[syst][process])
                    else:
                        this_list.append("-")
                elif process in bkgHistDictionary[category][region]:
                    if process in nameSysts[syst]:
                        this_list.append(nameSysts[syst][process])
                    else:
                        this_list.append("-")

        text_file.write(t.render(list=this_list))
        text_file.write("\n")


def main(config_file):

    # read config
    myAnalysis = Analysis(config_file)
    categories = getCategorization(myAnalysis)

    # create histograms
    sigHistDictionary = createDictionary(myAnalysis, categories, "signals")
    bkgHistDictionary = createDictionary(myAnalysis, categories, "backgrounds")
    dataHistDictionary = createDictionary(myAnalysis, categories, "data")
    # print ("bkgHistDictionary =",bkgHistDictionary)
    # print ("sigHistDictionary =",sigHistDictionary)
    # print ("dataHistDictionary =",dataHistDictionary)

    # fill histograms
    parallel = alphatwirl.parallel.build_parallel(
        parallel_mode="multiprocessing",
        processes=4,
    )
    parallel.begin()

    myHists = [sigHistDictionary, bkgHistDictionary, dataHistDictionary]
    myTypes = ["signals", "backgrounds", "data"]
    for i in range(0, len(myHists)):
        parallel.communicationChannel.put(
            fillDictionary, myAnalysis, myHists[i], myTypes[i], categories)

    finalDicts = parallel.communicationChannel.receive()
    parallel.end()

    # write histograms & text files
    writeRootDatacards(myAnalysis, finalDicts[0], finalDicts[1], finalDicts[2])
    writeTxtDatacards(myAnalysis, finalDicts[0], finalDicts[1], finalDicts[2])

    # profiling
    # alphatwirl.misc.print_profile_func(
    #     func=functools.partial(fillDictionary,myAnalysis, sigHistDictionary, "signals"), profile_out_path=None
    # )
