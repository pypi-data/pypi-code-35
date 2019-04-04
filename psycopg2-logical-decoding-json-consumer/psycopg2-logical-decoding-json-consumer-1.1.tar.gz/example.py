#   Copyright 2019 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging
import time

from psycopg2_logical_decoding_json_consumer import Consumer

DSN = ""
SLOT = "example"

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(message)s")


def transactions_callback(transactions):
    log.info("Got transactions: {}".format(transactions))


def a():
    log.info("a")
    time.sleep(4)
    consumer.call_later(5, a)


def b():
    log.info("b")
    consumer.call_later(3, b)


consumer = Consumer(transactions_callback, max_transactions_gather_count=None, max_transactions_gather_time=1)
a()
b()
consumer.connect(DSN, SLOT)
consumer.run()
