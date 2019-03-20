import logging
from redis import Redis
from pb.error_event import publish_to_error
from rest_framework.response import Response
from django.db import connection
from rest_framework import status

redis = Redis('localhost')

def handle_error(data, counter, project_id, topic_name):
    if counter > 5:
        logging.info("retry exceeded")
        print(data, 'datadata')
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE jobs set status = 'failed' WHERE id={0}".format(
                    data['job']
                )
            )
        publish_to_error(data={'job_id': data['job']}, project_id=project_id, topic_name=topic_name)

        return Response(status=status.HTTP_200_OK)


def create_key(request):
    # This helper function creates a unique key for a message
    return "%s_%s" % (request['subscription'], request['message']['messageId'])


def get_fail_count(key):
    # In case you want to wait some arbitrary time before your message "fails"
    redis.incr(key)
    counter = int(redis.get(key))
    return counter


