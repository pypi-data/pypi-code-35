import tempfile

from PIL import Image


def get_object_ids(objects):
    return [object['id'] for object in objects]


def get_test_image():
    """
    Возвращает тестовую картинку
    """
    file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    # Записываю картинку в файл, чтобы файл мог пройти валидацию Django для картинок
    image = Image.new('RGB', (200, 200), 'white')
    image.save(file, 'PNG')
    return file


def get_object_by_id(objects, object_id):
    object = list(filter(
        lambda object: object['id'] == object_id,
        objects
    ))[0]
    return object
