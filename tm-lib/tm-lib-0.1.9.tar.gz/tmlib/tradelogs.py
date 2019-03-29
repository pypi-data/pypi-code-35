import re

from connexion import NoContent
from mongoengine import ValidationError

from tmlib.models import TradeLog



def get_trade_logs(ticket=None, account_number=None, from_date=None,  include_expired=False):
    """
    Get trade logs by ticket ID;
    Return all the logs if no ticket id is specified
    :param ticket:
    :return:
    """
    order_type_filters = ['OP_BUY', 'OP_SELL']
    if include_expired:
        order_type_filters += ['OP_BUYSTOP', 'OP_BUYLIMIT', 'OP_SELLSTOP', 'OP_SELLLIMIT']

    mongo_filter = {
        "order_type__in": order_type_filters
    }
    if ticket:
        mongo_filter['ticket'] = ticket
    if account_number:
        mongo_filter['account'] = account_number
    if from_date:
        from_date_pattern = re.compile(f"{from_date} *")
        mongo_filter['order_close_time'] = from_date_pattern
        
    trade_logs: TradeLog = TradeLog.objects_without_id(**mongo_filter)
    return [t.to_mongo() for t in trade_logs], 200


def post_trade_logs(tradelogs_body):
    """
    Add a new trade log. Proxy function for the put method
    :param tradelogs_body:
    :return:
    """
    return put_trade_logs(tradelogs_body)


def put_trade_logs(tradelogs_body):
    """
    Add a new trade log.
    :param tradelogs_body:
    :return:
    """
    account = tradelogs_body.get('account')
    ticket = tradelogs_body.get('ticket')
    try:
        trade_log = TradeLog.objects(account=account, ticket=ticket).update(
            upsert=True, full_result=True, **{f'set__{k}': v for k, v in tradelogs_body.items()}
        )
        if trade_log.matched_count == 1:
            status = 200
        else:
            status = 201
        res = TradeLog.objects.get(account=account, ticket=ticket).to_dict()
    except ValidationError as e:
        status = 400
        res = {
            "detail": e.message,
            "status": status,
            "title": "Bad Request",
            "type": "about:blank"
        }
    return res, status

def delete_trade_logs(account_number, minion_name, symbol, ticket):
    trade_logs = TradeLog.objects(account=account_number, minion_name=minion_name, symbol=symbol, ticket=ticket)
    if len(trade_logs):
        status = 204
        trade_logs.delete()
    else:
        status = 404
    return NoContent, status