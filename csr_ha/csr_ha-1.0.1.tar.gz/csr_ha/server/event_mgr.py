#!/usr/bin/env python
from multiprocessing import Process
from csr_cloud.csr_cloud import csr_cloud as cloud
from os.path import expanduser

cert_file = "/etc/ssl/certs/ca-bundle.trust.crt"


def handler(node, event_type):
    c = cloud("HA")
    c.ha.set_event_logger(node, event_type)
    try:

        c.ha.event_logger.info("Event type is %s" % event_type)

        # Verify the node has been sufficiently configured
        rc = c.ha.verify_node(node, event_type)
        if 'OK' != rc:
            c.ha.event_logger.info("Event processing aborted")
            return

        c.ha.event_logger.info("CSR HA: %s event for node" %event_type)

        route_table = c.ha.get_route_table(node, event_type)
        if not route_table:
            # since there are no route tables in gcp cloud, we expect a None for RT
            c.ha.event_logger.info("Route table not found.")

        c.ha.event_logger.info("CSR HA: Set route table for %s" % event_type)
        response = c.ha.set_route_table(node, event_type, route_table)

    except Exception as e:
        c.ha.event_logger.exception("Event Handler Exception: %s" % e)


def handle_event(node, event_type):
    c = cloud("HA")
#    print "Starting an event handler process"
    try:
        p = Process(target=handler, args=(node, event_type))
        p.start()
        p.join()
    except Exception as e:
        c.log.exception("HA Server Exception: %s" % e)

