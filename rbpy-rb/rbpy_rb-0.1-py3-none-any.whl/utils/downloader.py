import logging
import logging.config
import os
import zipfile
import wget
import sys
import json
from rb.core.lang import Lang

LINKS = {
    Lang.EN: {
        'models': {
            'coca': "https://nextcloud.readerbench.com/index.php/s/H5ccMZwRLyMffG4/download"
        }
    },
    Lang.RO: {
        'models': {
            'diacritics': "https://nextcloud.readerbench.com/index.php/s/pfC25G64JgxcfZS/download",
            'readme': "https://nextcloud.readerbench.com/index.php/s/g9etLBeSTmKxjM8/download",
        },
        'spacy': {
            'ro_ud_ft_ner': "https://nextcloud.readerbench.com/index.php/s/GLdDH8R4jpkFfnd/download",
        }
    }
}

logger = logging.getLogger()

def download_model(lang: Lang, name: str) -> bool:
    if not lang in LINKS:
        logger.info('{} not supported.'.format(lang))
        return False
    if not name in LINKS[lang]['models']:
        logger.info('No model named {}.'.format(name))
        return False
    logger.info("Downloading model {} for {} ...".format(name, lang.value))
    link = LINKS[lang]['models'][name]
    folder = "resources/{}/models/".format(lang.value)
    os.makedirs(folder, exist_ok=True)     
    filename = wget.download(link, out=folder, bar=wget.bar_thermometer)
    logger.info('Downloaded {}'.format(filename))
    if zipfile.is_zipfile(filename):
        logger.info('Extracting files from {}'.format(filename))
        with zipfile.ZipFile(filename,"r") as zip_ref:
            zip_ref.extractall(folder)
        os.remove(filename)
    return True

def download_spacy_model(lang: Lang, name: str = 'latest') -> bool:
    if not lang in LINKS:
        return False
    if not name in LINKS[lang]['spacy']:
        return False
    logger.info("Downloading spacy model {} for {}...".format(name, lang.value))
    link = LINKS[lang]['spacy'][name]
    folder = "resources/{}/spacy/".format(lang.value)
    os.makedirs(folder, exist_ok=True)     
    filename = wget.download(link, out=folder, bar=wget.bar_thermometer)
    logger.info('Downloaded {}'.format(filename))
    with zipfile.ZipFile(filename,"r") as zip_ref:
        zip_ref.extractall(folder)
    os.remove(filename)
    return True
        
if __name__ == "__main__":
    download_model(Lang.EN, 'coca')

