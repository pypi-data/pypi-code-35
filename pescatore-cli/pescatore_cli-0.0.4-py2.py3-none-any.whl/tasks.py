from celery import shared_task
from celery.utils.log import get_task_logger

from .functions import cerca_stringa_in_bacino as cerca_stringa_in_bacino_f

logger = get_task_logger(__name__)


@shared_task(bind=True)
def cerca_stringa_in_bacino(self, stringa, bacino, id_licenza=None,
                            id_esca=None, id_consumer=None, note=None,
                            intervallo=5):
    errors = []
    uscita = None

    try:
        uscita = cerca_stringa_in_bacino_f(stringa, bacino, id_licenza, id_esca,
                                           id_consumer, note, intervallo)

    except Exception as e:
        if hasattr(e, 'message'):
            msg = e.message
        else:
            msg = str(e)

        logger.exception(msg)
        errors.append(msg)

    return {
        'data': {
            'uscita': uscita
        },
        'meta': {
            'status': 'OK' if len(errors) == 0 else 'ERROR',
            'errors': {
                'cerca_stringa_in_bacino': errors
            }
        }
    }
