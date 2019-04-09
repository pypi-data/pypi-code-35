"""This test creates a troup with a huge number of workers that
   receives a huge number of messages.  The attempt to send messages
   and create workers should both encounter throttling limits (either
   system process or fd limits, and also the transmit limits).  In
   addition, most of the transmits from the PrimaryActor occur before
   the troup manager has even been started, so this tests the attempt
   to send a large number of messages to an address that is still
   local.  The troupe workers also block for a length period of time
   in a manner where they are unresponsive.  And the transmits and
   receives have associated log messages.

"""

import time
from thespian.actors import *
from thespian.test import *

from thespian.troupe import troupe
from thespian.actors import ActorTypeDispatcher
from thespian.actors import ActorSystem
from thespian.actors import WakeupMessage
import logging
import time


class StartTestMsg(object):
    def __init__(self, delay_time = 5):
        self._delay_time = delay_time


class PrimaryActor(ActorTypeDispatcher):
    def receiveMsg_StartTestMsg(self, msg, sender):
        if not hasattr(self, "batch_number"):
            self.submission_actor_pool_size = 2
            self.batch_number = 0
            self.last_secondary_actor_used = -1
            self.secondary_actors = self.create_secondary_actor_pool( SecondaryActor, self.submission_actor_pool_size )

        next_submission_actor_to_use = self.last_secondary_actor_used + 1
        if next_submission_actor_to_use > self.submission_actor_pool_size - 1:
            next_submission_actor_to_use = -1

        for x in range(0, 5000):
            message = {"number": x, "batch": self.batch_number, "delay": msg._delay_time}
            logging.info("Sending message number {0} {1}".format(self.batch_number, x))
            self.send(self.secondary_actors[next_submission_actor_to_use], message)

        self.batch_number += 1

        if self.batch_number >= 5:
            return


        self.last_submission_actor_used = next_submission_actor_to_use
        # self.wakeupAfter(1)

    def create_secondary_actor_pool(self, actor_code, pool_size):
        submission_actor_pool = []
        for x in range(0, pool_size):
            submission_actor_pool.append(self.createActor(actor_code))
        return submission_actor_pool

    def receiveMsg_str(self, strmsg, sender):
        self.send(self.secondary_actors[self.last_submission_actor_used], (sender, strmsg))

@troupe(max_count=4000, idle_count=1)
class SecondaryActor(ActorTypeDispatcher):
    def receiveMsg_dict(self, msg, sender):
        logging.info("Received message number {0} {1}".format(msg["batch"], msg["number"]))
        time.sleep(msg["delay"])
    def receiveMsg_tuple(self, lastmsg, sender):
        self.send(*lastmsg)

class TestIssue38():

    def test_issue38_1(self, asys):
        actor_system_unsupported(asys,
                                 'multiprocUDPBase',  # can drop messages and leave (large) actors behind
                                 'multiprocQueueBase', # doesn't work well
                                 'multiprocTCPBase-AdminRouting',  # disable for now
                                 'multiprocTCPBase-AdminRoutingTXOnly',  # disable for now
                                 )
        primary_actor = asys.createActor(PrimaryActor)
        asys.tell(primary_actor, StartTestMsg(0 if asys.base_name in ['simpleSystemBase'] else 5))
        r = asys.ask(primary_actor, "done", 360)
        assert r == "done"


