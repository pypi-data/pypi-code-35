from . import settings
from .api.licenze import (list as list_licenze, read as read_licenza)
from .api.esche import (list as list_esche, create as create_esca,
                        read as read_esca)
from .api.uscite import create as create_uscita


def cerca_stringa_in_bacino(stringa, bacino, id_licenza=None, id_esca=None,
                            id_consumer=None, note=None, intervallo=5):
    if settings.DEBUG:
        print('cerca_stringa_in_bacino', bacino, 'stringa', stringa)

    licenze = list_licenze()
    licenze = licenze.get('data', [])

    esche = list_esche()
    esche = esche.get('data', [])

    licenza = None
    esca = None

    if id_licenza is None:
        for el in licenze:
            if el['bacino'] == bacino:
                if el['active']:
                    licenza = el
                    break
    else:
        licenza = read_licenza(id_licenza, consumer_id=id_consumer).get('data')[0]

        if licenza['bacino'] != bacino:
            raise Exception('This licenza is for {}.'.format(licenza['bacino']))

    if id_esca is None:
        for el in esche:
            if el['stringa'] == stringa:
                if el['active']:
                    esca = el
                    break
    else:
        esca = read_esca(id_esca, consumer_id=id_consumer).get('data')[0]

    if esca is None:
        esca_body = {
            'stringa': stringa
        }
        esca = create_esca(esca_body, consumer_id=id_consumer).get('data')[0]

    if licenza is None:
        raise Exception('Unable to find licenza for bacino {}.'.format(bacino))
    if esca is None:
        raise Exception(
            'Unable to find esca with stringa "{}".'.format(stringa))

    obj = {
        'licenza': licenza['uuid'],
        'esca': esca['uuid'],
        'intervallo': intervallo
    }
    if note is not None:
        obj['note'] = note

    uscita = create_uscita(obj, consumer_id=id_consumer)

    return uscita
