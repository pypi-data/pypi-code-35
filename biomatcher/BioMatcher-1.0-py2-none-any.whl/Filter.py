import json
import click
import Exceptions as Exc
from Bio import SeqIO


@click.command()
@click.option('--mature', '-m', required=True,  # default="mature_plant_reduced.fa",
              help='This is the path of fasta file of plant microRNA')
@click.option('--jsonspecies', '-s', required=True,  # default="jsonspecies.json",
              help='This is the path of the json containing all the species you want to filter')
@click.option('--pathoutput', '-o', required=False, default="mature_plant_filtered.fa",
              help='This is the path of output file')
def filtering(mature, jsonspecies, pathoutput):
    """
    This component serves to filter the microRNAs passed in input with the selected species

    Parameters
    ----------
    mature
        This is the path of fasta file of plant microRNA
    jsonspecies
        This is the path of the json containing all the species you want to filter
    pathoutput
        This is the path of output file

    Raises
    ------
    NoSpeciesSelectException
        If no species has been selected
    ErrorInFileException
        If there are errors in the parameters
    """
    plant, plantselected, selectedspecies = [], [], []

    # In this cycle, I replaced the " " with "|" to generalize the components
    for s in SeqIO.parse(mature, "fasta"):
        descr = s.description
        if '|' not in s.description:
            descr = s.description.replace(" ", "|")
        # While the description contains more than 4 "|" means that the species is composed of more than 2 words
        # So you have to remove the "|" between these words
        while len(descr.split('|')) > 4:
            ind = [i for i, a in enumerate(descr) if a == '|']  # this array contains the pipe's positions
            piperemove = ind[len(ind) - 2]  # locate the pipe's position to remove
            descr = descr[0:piperemove] + " " + descr[piperemove + 1:]
            # In this for, I removed unnecessary spaces
            newdescr = ""
            for p in descr.split('|'):
                newdescr += p.strip() + "|"
            descr = newdescr[:len(newdescr) - 1]
        plant.append('>' + descr + '\n' + str(s.seq) + '\n')  # this is the new FASTA

    if len(plant) == 0:
        raise Exc.ErrorInFileException

    # I Created the filtered FASTA file
    with open(jsonspecies) as f:
        selectedspecies = json.load(f)

    try:
        if len(selectedspecies["selectedspecies"]) == 0:
            pass
    except KeyError:
        raise Exc.ErrorInFileException

    # If no species was selected raise an exception
    if len(selectedspecies["selectedspecies"]) == 0:
        print("ERROR! No species has been selected!")
        raise Exc.NoSpeciesSelectException

    for seq in plant:
        if seq.split('|')[2] in selectedspecies["selectedspecies"]:
            plantselected.append(seq)

    # I created the filtered FASTA file
    with open(pathoutput, 'w') as f:
        for j in plantselected:
            f.write(j)

    click.echo("Operation completed successfully.\n")
    click.echo("You can find your mature file filtered in " + pathoutput)


if __name__ == '__main__':
    filtering()
