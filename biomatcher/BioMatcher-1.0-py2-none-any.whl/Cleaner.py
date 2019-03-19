import numpy
import click
import pandas as pd
from Bio import SeqIO
import Exceptions as exc
from tqdm import tqdm


@click.command()
@click.option('--mature', '-m', required=True, default="mature_plant.fa",
              help='This is the path of fasta file of plant microRNA')
@click.option('--pathcleaned', '-o', required=False, default="mature_plant_cleaned.fa",
              help='This is the path of the clean file fasta')
@click.option('--patherrors', '-e', required=False, default="mature_plant_errors.fa",
              help='This is the path of the fasta microRNA file with errors')
@click.option('--pathredundant', '-r', required=False, default="mature_plant_redundant.csv",
              help='This is the path of the csv file of redundant microRNAs')
def cleaning(mature, pathcleaned, patherrors, pathredundant):
    """
    This component makes it possible to clean the microRNAs that pass in input from errors or redundancies

    Parameters
    ----------
    mature
        This is the path of fasta file of plant microRNA
    pathcleaned
        This is the path of the clean file fasta
    patherrors
        This is the path of the fasta microRNA file with errors
    pathredundant
        This is the path of the fasta file of redundant microRNAs

    Raises
    ------
    ErrorInFileException
        If there are errors in the parameters
    """
    allplant, errors, redundant, alreadyanalize = [], [], [], []

    # In this cycle, I replaced the " " with "|" to generalize the components
    for s in SeqIO.parse(mature, "fasta"):
        descr = s.description
        if '|' not in s.description:
            descr = s.description.replace(" ", "|")

        # While the description contains more than 4 "|" means that the species is composed of more than 2 words
        # So you have to remove the "|" between these words
        while len(descr.split('|')) > 4:
            ind = [i for i, a in enumerate(descr) if a == '|']  # this array contains the pipe's positions
            piperemove = ind[len(ind)-2]  # locate the pipe's position to remove
            descr = descr[0:piperemove] + " " + descr[piperemove+1:]
            # locate the pipe's position to remove
            newdescr = ""
            for p in descr.split('|'):
                newdescr += p.strip() + "|"
            descr = newdescr[:len(newdescr)-1]

        allplant.append('>' + descr + '\n' + str(s.seq) + '\n')  # this is the new FASTA
    cleaned = allplant
    if len(cleaned) == 0:
        raise exc.ErrorInFileException

    # In this for, I removed the microRNA with errors
    for s in cleaned[:]:
        i = 0
        while i < len(s.split('\n')[1]):
            if s.split('\n')[1][i] not in {'A', 'C', 'G', 'U'}:
                errors.append(s)
                cleaned.remove(s)
                i = len(s.split('\n')[1])  # force the exit
            i += 1

    seqclean = []
    newclean = []

    # The elimination of redundancies starts here
    with tqdm(total=len(cleaned), desc="Cleaning in progress") as pbar:
        for s in cleaned:
            idseq = s.split('|')[1]
            seq = s.split('\n')[1]
            # If the sequence has not yet been analyzed
            if seq not in seqclean:
                newclean.append(s)
                seqclean.append(seq)
            else:
                # Position of the first microRNA with that sequence
                num = [i for i, x in enumerate(cleaned)if x.split('\n')[1] == seq]
                mainid = cleaned[num[0]].split('|')[1]

                # Position of the main id in the redundant list
                pos = [i for i, x in enumerate(redundant) if x["Main id"] == mainid]
                if len(pos) != 0:
                    redundant[pos[0]]["Redund id"] += "|" + idseq
                else:
                    redundant.append(dict({"Main id": mainid, "Redund id": idseq}))
            pbar.update(1)

    # compar = 0
    # for s in range(1, len(cleaned)):
    #     compar += (len(cleaned) - s)
    # descr = 'Cleaning in progress'  # description to be included in the progress bar

    # The elimination of redundancies starts here
    # with tqdm(total=compar, desc=descr) as pbar:
    #     i = 0  # counter of first for
    #     j = 0  # counter of effective comparisons
    #     for s1 in cleaned[:]:
    #         redundantids = ""
    #         for s2 in cleaned[i:]:
    #             pbar.update(1)
    #             if s2 not in alreadyanalize:  # Analyze the string if it has not already been analyzed
    #                 if s1.split('|')[1] != s2.split('|')[1]:  # compare the id
    #                     if len(s1.split('\n')[1]) == len(s2.split('\n')[1]):  # compare the lenght of first line of microRNA
    #                         if s1.split('\n')[1] == s2.split('\n')[1]:  # compare the seq
    #                             alreadyanalize.append(s1)
    #                             redundantids += '|' + s2.split('|')[1]
    #                             cleaned.remove(s2)
    #                             if i != 0:
    #                                 i -= 1  # Because I removed a line from cleaned
    #             j += 1
    #
    #         if len(redundantids) != 0:
    #             redundant.append({"main": s1.split('|')[1],
    #                               "redundant": redundantids[1:]})  # remove first "|"
    #         i += 1
    #
    #     pbar.update(compar - j)  # to fill the bar

    # I created the cleaned FASTA file
    with open(pathcleaned, "w") as f:
        for x in newclean:
            f.write(x)

    # I created the CSV file with redundand microRNA
    if not len(redundant) == 0:
        with open(pathredundant, "w") as f:
            f.write("Main ID, Redundant IDs\n")  # print header
            for r in redundant:
                data = pd.DataFrame(r, columns=['Main id', 'Redund id'], index=[0])
                data.to_csv(f, encoding='utf-8', index=False, header=False, line_terminator='\n')

    # I created the FASTA file with errors
    if not len(errors) == 0:
        with open(patherrors, "w") as f:
            for x in errors:
                f.write(x)

    # I managed the message in output
    print("Operation completed successfully.\n"
            "You can find your mature file cleaned in " + pathcleaned + " ", end='')
    if not len(errors) == 0:
        print("- the errors in " + patherrors, end='')
    if not len(redundant) == 0:
        print("- the redundancies in " + pathredundant)


if __name__ == '__main__':
    cleaning()
