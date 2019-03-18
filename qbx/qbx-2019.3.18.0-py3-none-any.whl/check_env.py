"""
Usage:
    udpate_package.py [<pkg>...]


"""
import socket


def check_redis():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect(('service.qbtrade.org', 6379))
    except:
        print('fail connect to service.qbtrade.org:6379')
        return False
    sock.close()
    return True


def check_contract():
    import requests
    r = requests.get('http://api.qbtrade.org/contracts?count=1')
    return r.status_code == 200


def check_kong():
    import requests
    r = requests.get('http://kong-admin.qbtrade.org/apis')
    return r.status_code == 200


def check_env_single():
    success = True
    for func in [check_redis, check_contract, check_kong]:
        try:
            r = func()
            if not r:
                raise Exception('check fail')
        except:
            print(func, 'fail')
            success = False
    return success


def check_env():
    import arrow
    start = arrow.now()
    t = 5
    import time
    while True:
        r = check_env_single()
        if r:
            break
        print('sleep', t)
        time.sleep(t)
        t *= 2
        t = min(t, 300)
        if (arrow.now() - start).total_seconds() > 20 * 60:
            print('too long, exit with code 1', start, arrow.now())
            exit(1)
    print('check success, time to sprint')
    # sock.settimeout(None)
    # fileobj = sock.makefile('rb', 0)


if __name__ == '__main__':
    # docopt(__doc__)

    # docopt = docoptinit(['qbtrade', 'otlib'])
    check_env()
    # update_package(['qbtrade', 'otlib'])
    # if docopt['--daemon']:
    #     pass
    # else:
    #     qb.run_until_complete(play())
