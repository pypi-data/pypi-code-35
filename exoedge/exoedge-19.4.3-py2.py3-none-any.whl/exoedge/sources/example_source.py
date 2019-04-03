# -*- coding: utf-8 -*-
# pylint: disable=W1202
import sys
import time
import datetime
from exoedge.sources import ExoEdgeSource
from exoedge import logger

LOG = logger.getLogger(__name__)

def sixteen():
    return 16

class ExampleSource(ExoEdgeSource):
    """
      Below is an example config_io object for this ExoEdgeSource.

{
  "channels": {
    "sixteen": {
      "display_name": "The number 16, according to the example_source.",
      "protocol_config": {
        "report_on_change": false,
        "report_rate": 5000,
        "application": "ExoEdgeSource",
        "app_specific_config": {
          "function": "sixteen",
          "module": "example_source",
          "parameters": {},
          "positionals": []
        },
        "sample_rate": 5000,
        "down_sample": "ACT"
      }
    },
    "thirty_minutes_from_now": {
      "display_name": "The time, thirty minutes from now, according to the gateway.",
      "protocol_config": {
        "report_on_change": false,
        "report_rate": 5000,
        "application": "ExoEdgeSource",
        "app_specific_config": {
          "function": "minutes_from_now",
          "module": "example_source",
          "parameters": {
            "minutes": 30
          },
          "positionals": []
        },
        "sample_rate": 5000,
        "down_sample": "ACT"
      }
    }
  }
}
    """

    def minutes_from_now(self, minutes=0.0):
        return datetime.datetime.fromtimestamp(float(minutes)*60 + time.time()).strftime('%c')

    def run(self):

        exoedge_source_channels = self.get_channels_by_application('ExoEdgeSource')
        example_source_channels = self.get_channels_by_module(__name__)
        # filter by only the channels in this example
        my_channels = list(set(exoedge_source_channels).intersection(example_source_channels))

        LOG.critical("Starting with channels: {}".format(my_channels))

        while True:

            for channel in my_channels:
                if channel.is_sample_time():
                    func = channel.protocol_config.app_specific_config['function']
                    if hasattr(sys.modules.get(__name__), func):
                        function = getattr(sys.modules[__name__], func)
                        par = channel.protocol_config.app_specific_config['parameters']
                        pos = channel.protocol_config.app_specific_config['positionals']
                        LOG.warning("calling '{}' with: **({})"
                                    .format(function, par))
                        try:
                            channel.put_sample(function(*pos, **par))
                        except Exception as exc: # pylint: disable=W0703
                            LOG.warning("Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                    elif hasattr(self, func):
                        function = getattr(self, func)
                        par = channel.protocol_config.app_specific_config['parameters']
                        pos = channel.protocol_config.app_specific_config['positionals']
                        LOG.warning("calling '{}' with: **({})"
                                    .format(function, par))
                        try:
                            channel.put_sample(function(*pos, **par))
                        except Exception as exc: # pylint: disable=W0703
                            LOG.warning("Exception".format(format_exc=exc))
                            channel.put_channel_error(exc)
                    else:
                        channel.put_channel_error(
                            'MySource has no function: {}'.format(func))

            time.sleep(0.01) # throttle a bit to lay off the processor
