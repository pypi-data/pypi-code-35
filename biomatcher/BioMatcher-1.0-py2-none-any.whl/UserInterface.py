import Manager
import click
import Exceptions as Exc


@click.command()
@click.option('--filehuman', '-h', required=True, default="mature_human_reduced.fa",
              help='This is the path of fasta file of human microRNA')
@click.option('--fileplant', '-p', required=True, default="mature_plant_reduced.fa",
              help='This is the path of fasta file of plant microRNA')
@click.option('--jsonconfig', '-c', required=True, default="jsoncomp.json",
              help='This is the path of json containing all the types of comparisons you want to make')
@click.option('--pathoutput', '-o', required=True, default="fileoutput.csv",
              help='This is the path of output csv file')
@click.option('--jsonidhuman', '-hid', required=False,
              help='This is the json containing all the human id you have selected (opzional)')
@click.option('--jsonidplant', '-pid', required=False,
              help='This is the json containing all the plant id you have selected (opzional)')
def userinterface(filehuman, fileplant, jsonconfig, pathoutput, jsonidhuman=None, jsonidplant=None):
    """
    This software is used to find the identical seed between human and plant microRNAs

    Parameters
    ----------
    filehuman
        This is the path of fasta file of human microRNA
    fileplant
        This is the path of fasta file of plant microRNA
    jsonconfig
        This is the json containing all the types of comparisons you want to make
    pathoutput
        This is the path of output csv file
    jsonidhuman
        This is the json containing all the human id you have selected (opzional)
    jsonidplant
        This is the json containing all the plant id you have selected (opzional)
    """

    dictinput = {'filehuman': filehuman, 'fileplant': fileplant, 'jsonconfig': jsonconfig,
                 'pathoutput': pathoutput, 'jsonidhuman': jsonidhuman, 'jsonidplant': jsonidplant}

    try:
        Manager.manager(dictinput)
    except Exc.NoCompSelectException:
        click.echo("ERROR! No comparison has been selected!")
    except Exc.NoSeedEqualException:
        click.echo("WARNING! No identical seed was found in the files passed in input")
    except TypeError as e:
        click.echo("ERROR!\n" + e)
    except ValueError as e:
        click.echo("ERROR!\n" + e)
    except IOError as e:
        click.echo("ERROR! Could not read a file \n" + e)
    else:
        click.echo("Operation completed successfully. You can find your CSV output in " + pathoutput)


if __name__ == '__main__':
    userinterface()
