import Matcher
import Output
import json
import Exceptions as Exc
from time import sleep
from tqdm import tqdm
from Bio import SeqIO


def manager(dictinput):
    """
    This component has the role of being the manager of the pipeline and serves to sort the various information given in
    input and using the Matcher component is able to collect all the compatible microRNAs and with the Output component
    is able to print the various results on file.

    Parameters
    ----------
    dictinput
        This is the dictionary with all the information given by the user in UserInterface

    Raises
    ------
    NoCompSelectException
        If no comparison was selected
    NoSeedEqualException
        If no identical microRNA was found
    ErrorInFileException
        If there are errors in the parameters
    """
    stringsfound = {}  # dict of the same strings found
    humannone, plantnone = False, False
    idhuman, idplant = {}, {}
    exact_matches = []

    if dictinput['jsonidhuman'] is not None:
        with open(dictinput['jsonidhuman']) as f:
            idhuman = json.load(f)
    if len(idhuman) == 0:
        humannone = True
    if dictinput['jsonidhuman'] is not None:
        with open(dictinput['jsonidplant']) as f:
            idplant = json.load(f)
    if len(idplant) == 0:
        plantnone = True
    with open(dictinput['jsonconfig']) as f:
        matches = json.load(f)
        try:
            for j in matches["exact_matches"]:
                if j["active"] == "True":
                    exact_matches.append(j)
        except KeyError as e:
            print("Error in JSON file of comparisons\n" + e)
            raise Exc.ErrorInFileException

    if len(exact_matches) == 0:
        raise Exc.NoCompSelectException  # if no comparison was selected

    output = Output.Output(dictinput['pathoutput'], exact_matches)

    idpos = 1
    for x in exact_matches:
        try:
            idcomp = x["id"]
            n1, m1, n2, m2 = int(x["h_start"]), int(x["h_end"]), int(x["p_start"]), int(x["p_end"])
        except KeyError or TypeError as e:
            print("Error in JSON file of comparisons.\n" + e)
            raise Exc.ErrorInFileException

        lines_human, lines_plant = [], []

        # In this cycle, I replaced the " " with "|" to generalize the components
        for seq_human in SeqIO.parse(dictinput['filehuman'], "fasta"):
            descr = seq_human.description
            if '|' not in seq_human.description:
                descr = seq_human.description.replace(" ", "|")

            # While the description contains more than 4 "|" means that the species is composed of more than 2 words
            # So you have to remove the "|" between these words
            while len(descr.split('|')) > 4:
                ind = [i for i, a in enumerate(descr) if a == '|']  # this array contains the pipe's positions
                piperemove = ind[len(ind) - 2]  # locate the pipe's position to remove
                descr = descr[0:piperemove] + " " + descr[piperemove + 1:]
                # locate the pipe's position to remove
                newdescr = ""
                for p in descr.split('|'):
                    newdescr += p.strip() + "|"
                descr = newdescr[:len(newdescr) - 1]
            try:
                if humannone or seq_human.description.split(' ')[1] in idhuman["id_human"]:
                    lines_human.append(">" + descr + '\n' + str(seq_human.seq) + '\n')  # real human strings
            except KeyError:
                print("Error in JSON file of human ID")
                raise Exc.ErrorInFileException

        if len(lines_human) == 0:
            print("Error in human FASTA file")
            raise Exc.ErrorInFileException

        # In this cycle, I replaced the " " with "|" to generalize the components
        for seq_plant in SeqIO.parse(dictinput['fileplant'], "fasta"):
            descr = seq_plant.description
            if '|' not in seq_plant.description:
                descr = seq_plant.description.replace(" ", "|")
            while len(descr.split('|')) > 4:
                ind = [i for i, a in enumerate(descr) if a == '|']
                piperemove = ind[len(ind) - 2]
                descr = descr[0:piperemove] + " " + descr[piperemove + 1:]
                newdescr = ""
                for p in descr.split('|'):
                    newdescr += p.strip() + "|"
                descr = newdescr[:len(newdescr) - 1]
            try:
                if plantnone or seq_plant.description.split('|')[1] in idplant["id_plant"]:
                    lines_plant.append(">" + descr + '\n' + str(seq_plant.seq) + '\n')  # real plant strings
            except KeyError:
                print("Error in JSON file of plant ID")
                raise Exc.ErrorInFileException

        if len(lines_plant) == 0:
            print("Error in human FASTA file")
            raise Exc.ErrorInFileException

        num_compar = (len(lines_human) * len(lines_plant))  # number of comparisons to be made
        descr = 'Comparisons ' + idcomp + ' in progress'  # description to be included in the progress bar

        with tqdm(total=num_compar, desc=descr) as pbar:
            for seq_human in lines_human:
                for seq_plant in lines_plant:
                    if Matcher.match(seq_human.split('\n')[1], seq_plant.split('\n')[1], n1, m1, n2, m2):
                        stringsfound.update({'Human id': seq_human.split('|')[1],
                                             'Plant id': seq_plant.split('|')[1],
                                             'Comparison id': idcomp})
                        output.stack(stringsfound)
                    pbar.update(1)

        # If isn't the last kind of comparison
        if len(exact_matches) != idpos:
            sleep(1)  # 1 second of delay
        idpos += 1

    output.close()
    print()  # written to have a carriage return in the console
    if len(stringsfound) == 0:
        raise Exc.NoSeedEqualException
