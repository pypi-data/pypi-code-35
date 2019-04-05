import os
import signal
from threading import Event

import click
from click import echo, secho
from redis import Redis

DEFAULT_REDIS = dict(
    host=os.environ.get('REDIS_HOST') or 'localhost',
    port=os.environ.get('REDIS_PORT') or 6379,
    db=os.environ.get('REDIS_DB') or 0,
    password=os.environ.get('REDIS_PASS'),
)


def setup_interupt_signal() -> Event:
    interupted = Event()

    def interupt(signo, _frame):
        print(f"Interrupted by {signo}, shutting down")
        interupted.set()
        exit(0)

    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG' + sig), interupt)
    return interupted


@click.command()
@click.argument('keys', nargs=-1)
@click.option('--from-set', help='take keys from set key')
@click.option('--prometheus', default=None, help='enable prometheus polling on port', type=click.INT)
@click.option('--tick-rate', default=1, help='how often to check in seconds', show_default=True)
@click.option('--no-color', is_flag=True, help='disable output color')
@click.option('-h', 'host', default=DEFAULT_REDIS['host'], help='redis hoststring', show_default=True)
@click.option('-p', 'port', default=DEFAULT_REDIS['port'], help='redis port', show_default=True)
@click.option('-a', 'password', default=DEFAULT_REDIS['password'], help='redis password')
@click.option('-db', 'db', default=DEFAULT_REDIS['db'], help='redis host', show_default=True)
def main(prometheus, tick_rate, keys, no_color, from_set, **redis_kwargs):
    """track redis keys to stdout and/or prometheus"""
    # example prometheus results as Gauge:
    # redis_track{key="github",source="redis@localhost/0:6379",type="set"} 36189.0
    if not keys and not from_set:
        click.echo('either keys argument or --from-set option has to be provided', err=True)
        exit(1)
        return
    if prometheus:
        from prometheus_client import Gauge, Info, start_http_server
        start_http_server(prometheus)
        queue_gauge = Gauge(
            f'redis_track', 'redis key value tracking',
            ['key', 'source', 'type']
        )
        queue_info = Info(
            f'redis_track', 'redis key value tracking',
            ['key', 'source', 'type']
        )

    def send_prometheus(key, value, type_):
        """send info to prometheus depending on redis key type"""
        if type_ in ['set', 'zset', 'none']:
            queue_gauge.labels(
                key=key,
                source=source,
                type=type_
            ).set(value)
        elif type_ in ['string']:
            queue_info.labels(
                key=key,
                source=source,
                type=type_
            ).info({key: value})

    redis = Redis(decode_responses=True, **redis_kwargs)
    source = 'redis@{host}/{db}:{port}'.format(**redis_kwargs)

    alternate = True
    alt1 = {'fg': 'white', 'bg': 'black'}
    alt2 = {'bg': 'white', 'fg': 'black'}

    if not keys:
        keys = redis.smembers(from_set)
        if not keys:
            echo(f'no queues found in {from_set}', err=1)
            exit(1)
    for key, value, type_ in _track_queues(tick_rate, redis, keys):
        if all(v is None for v in [key, value, type_]):
            alternate = True
            click.clear()
            continue
        if no_color:
            echo(f'{key:<50}{value:>10}')
        else:
            secho(f'{key:<50}{value:>10}', **(alt1 if alternate else alt2))
        alternate = not alternate
        if prometheus:
            send_prometheus(key, value, type_)


def _track_queues(tick_rate, redis, queues):
    interrupted = setup_interupt_signal()
    while not interrupted.is_set():
        for key in queues:
            key_type = redis.type(key)
            if key_type == 'none':
                value = 0
            elif key_type == 'zset':
                value = redis.zcard(key)
            elif key_type == 'set':
                value = redis.scard(key)
            elif key_type == 'string':
                value = redis.get(key)
            else:
                raise ValueError(f'unsupported key type: {key_type}')
            yield key, value, key_type
        yield None, None, None  # indicate page break
        interrupted.wait(tick_rate)


if __name__ == '__main__':
    main()
