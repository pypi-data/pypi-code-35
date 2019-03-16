import requests
from progress.bar import Bar
import logging
import time
import furl
from goto import with_goto

def get(*args, **kwargs):
    return list(gen(*args, **kwargs))

@with_goto
def gen(endpoint,
        silent=False,
        next_key='next',
        count_key='count',
        results_key='results',
        sleep=60,   # seconds [sleep when exception, e.g., 60]
        pause=None, # seconds [pause between requests: e.g., 1]
        proxies=None,
        debug=False,
        limit=None, # count of pages to return, e.g., 1 to return just first page
        remove_keys_in_url=[],  # remove keys from urls included
        include_query_url=True, # include query urls.
        method='get'): # post or get
    '''
    e.g., get('')
    '''

    results = []

    count = 0

    while True:

        if endpoint:
            if debug:
                print(endpoint)
            try:
                if proxies:
                    data = getattr(requests, method)(endpoint, proxies=proxies).json()
                else:
                    data = getattr(requests, method)(endpoint).json()
            except Exception as e:
                print(e, endpoint)

                data = None

                # Sleep
                if callable(sleep):
                    s = sleep()
                else:
                    s = sleep

                logging.log(20, 'Sleeping for {} seconds'.format(s))

                if debug:
                    print('Sleeping for {} seconds'.format(s))

                time.sleep(s)
        else:
            break

        if data:

            # return results, if there is count_key
            if callable(count_key):
                if not count_key(data):
                    goto .end
            elif not data.get(count_key):
                goto .end

            if not silent:

                if 'bar' not in locals():

                    if callable(count_key):
                        if callable(results_key):
                            chunk = len(results_key(data))
                        else:
                            chunk = len(data.get(results_key))
                        bar = Bar('API Pages:', max=round(count_key(data)/chunk))
                    elif count_key in data.keys():
                        chunk = len(data.get(results_key))
                        bar = Bar('API Pages:', max=round(data.get(count_key)/chunk))

                bar.next()

            # if we have results, extend the results variable.
            if callable(results_key):
                if results_key(data):

                    if include_query_url:
                        results.extend([dict(result, **{'--': furl.furl(endpoint).remove(remove_keys_in_url).url}) for result in results_key(data)])
                    else:
                        results.extend(results_key(data))

            elif results_key in data.keys():

                if include_query_url:
                    results.extend([dict(result, **{'--': furl.furl(endpoint).remove(remove_keys_in_url).url}) for result in data[results_key]])
                else:
                    results.extend(data[results_key])

            # if there is url for next result set, set it as endpoint.
            if callable(next_key):
                endpoint = next_key(data)
            elif next_key not in data.keys():
                break
            elif not data.get(next_key):
                break
            else:
                endpoint = data[next_key]

            # pause in between requests
            if callable(pause):
                t = pause()
            else:
                t = pause

            if t:
                time.sleep(t)

            count += 1

            # stop if limit has been reached
            if limit:
                if count == limit:
                    break

            # generate instead
            for item in results:
                yield item
            del results
            results = []

    if not silent:
        bar.finish()

    label .end
    for item in results:
        yield item
