import pandas as pd
from loguru import logger
from tqdm import tqdm

from mailgun_cli import Mailgun

def clear_existing_routes(mailgun, mark):
    # STEP 1: delete all existing routes with mark
    logger.info(f'Delete Existing routes with description `{mark}`')
    for route in tqdm(mailgun.list_routes()['items'], desc='routes to check and may delete'):
        if route['description'].startswith(mark):
            id = route['id']
            resp = mailgun.delete(id)
            assert resp.status_code == 200

def update_from_csv(url, mark='[created by mailgun-cli]', proirity=50, stop=True):
    """update the route using csv"""
    logger.info(f'update the route using csv: {url}')
    forwardlist = pd.read_csv(url)
    mailgun = Mailgun()

    clear_existing_routes(mailgun, mark)

    # STEP 2: create routes
    for id, row in tqdm(forwardlist.iterrows(), total=forwardlist.shape[0], desc='routes to create'):
        from_ = row[0].lower()
        to = row[1].lower()

        expression = f"match_recipient('{from_}')"
        action = f"forward('{to}')"
        if stop:
            action = (action, 'stop()')
        description = f"{mark}"

        resp = mailgun.create_route(expression=expression, action=action, priority=proirity, description=description)

        assert resp.status_code == 200





if __name__ == '__main__':
    pass
