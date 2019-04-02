import logging

from datetime import timedelta
from datetime import datetime

import psutil
from pynvml import *

from .timer import Timer

MACHINE_ACTIVITY_MONITOR = 'machine_activity_monitors'

class GPUMonitor:
    def __init__(self):
        self.alive = True

        try:
            nvmlInit()
        except NVMLError as exception:
            self.alive = False

    def get_gpu_usage(self):
        if not self.alive:
            return []

        usage = []

        device_count = nvmlDeviceGetCount()
        for i in range(device_count):
            handle = nvmlDeviceGetHandleByIndex(i)
            try:
                util = nvmlDeviceGetUtilizationRates(handle)
                usage.append(util.gpu)
            except NVMLError as err:
                continue

        return usage

class MachineActivity:
    def __init__(self, dead_duration=timedelta(hours=1)):
        """
        :param dead_duration: If machine is inactive longer than this time, it is considered "dead".
        :type dead_duration timedelta
        """
        self.dead_duration = dead_duration
        self.inactive_since = None

    def is_active(self):
        """return: true if the machine is considered active."""
        raise NotImplementedError

    def get_duration_inactive(self):
        """return: timedelta of how long machine has been inactive"""
        if self.inactive_since is None:
            return timedelta()

        return self.get_now() - self.inactive_since

    def is_dead(self):
        """:return true if machine has been inactive longer than, or equal to dead_duration"""
        if self.inactive_since is None:
            return False

        duration_inactive = self.get_now() - self.inactive_since
        return duration_inactive >= self.dead_duration

    def check_activity(self):
        """Checks if the machine is currently active. If it is, inactivity timer is reset.
            :return True if active, False otherwise"""
        if self.is_active():
            print('resetting activity')
            self.inactive_since = None
            return True

        if self.inactive_since is None:
            self.inactive_since = self.get_now()

        return False

    def get_now(self):
        """Convenience method for getting current time. It is a method so subclasses can override and
            specify timezone, etc, if needed.
        """
        return datetime.now()


class ThresholdMachineActivity(MachineActivity):
    def __init__(self, cpu_threshold=0.25, gpu_threshold=0.25, user_activity_threshold=timedelta(minutes=20), dead_duration=timedelta(hours=1)):
        """
        :param cpu_threshold: If all CPU usage is below this percentage, it is considered inactive
        :type cpu_threshold float
        :param gpu_threshold: If GPU (if exits) is below this percentage, it is considered inactive.
        :type gpu_threshold float
        :param user_activity_threshold: If user has not ran a command within this time
        :type user_activity_threshold timedelta
        :param dead_duration: If machine is inactive longer than this time, it is considered "dead".
        :type dead_duration timedelta
        """
        MachineActivity.__init__(self, dead_duration)

        self.cpu_threshold = cpu_threshold
        self.gpu_threshold = gpu_threshold
        self.user_activity_threshold = user_activity_threshold
        self.gpu_monitor = GPUMonitor()

    def is_cpu_active(self):
        """:return true if all CPU usage is >= cpu_threshold"""

        cpu_usage = psutil.cpu_percent(percpu=True)

        for cpu_use in cpu_usage:
            if cpu_use >= self.cpu_threshold:
                return True

        return False

    def is_gpu_active(self):
        """:return true if GPU exists on machine and GPU usage is >= gpu_threshold"""

        for gpu_usage in self.gpu_monitor.get_gpu_usage():
            if gpu_usage >= self.gpu_threshold:
                return True

        return False

    def is_user_active(self):
        """:return true if user has ran a command """
        return False

    def is_active(self):
        """return: true if the machine is considered active."""
        active = self.is_cpu_active() or self.is_user_active()

        print('r:', active)

        if not self.gpu_monitor.alive:
            return active

        return active or self.is_gpu_active()


    def get_cpu_stats(self):
        stats = []
        cpu_usage = psutil.cpu_percent(percpu=True)

        for cpu_use in cpu_usage:
            stats.append(cpu_use)

        return stats

    def get_gpu_stats(self):
        stats = []
        for gpu_usage in self.gpu_monitor.get_gpu_usage():
            stats.append(gpu_usage)

        return stats

    def get_statistics(self):
        return {
            'cpu': {
                'usage': self.get_cpu_stats(),
                'threshold': self.cpu_threshold,
                'active': self.is_cpu_active()
            },
            'gpu': {
                'usage': self.get_gpu_stats(),
                'threshold': self.gpu_threshold,
                'active': self.is_gpu_active(),
            },
            'user_active': self.is_user_active()
        }


class MachineActivityMonitor(Timer):
    def __init__(self,  activity_monitor, dead_callback):
        """
        :param activity_monitor:
        :type activity_monitor MachineActivity
        """
        # Run every 60 seconds
        Timer.__init__(self, 60)
        self.activity_monitor = activity_monitor
        self.dead_callback = dead_callback

        self.logger = logging.getLogger(MACHINE_ACTIVITY_MONITOR)

    def run(self):
        while not self.stop_flag.wait(self.delay):
            self.logger.info('checking activity, we are active: {}'.format(self.activity_monitor.check_activity()))

            if self.activity_monitor.is_dead() and self.dead_callback is not None:
                self.dead_callback()
                return



