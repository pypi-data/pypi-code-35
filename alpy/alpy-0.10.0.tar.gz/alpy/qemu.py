# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
import logging
from . import utils


class QemuProcess:
    def __init__(self, args, timeout):
        self._timeout = timeout
        logger = logging.getLogger(__name__)
        with utils.StepResultLogger(logger, "Start QEMU"):
            logger.debug(f"Starting subprocess: {args}")
            self._process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
            )

    def close(self):
        logger = logging.getLogger(__name__)
        with utils.StepResultLogger(logger, "Close QEMU"):
            utils.close_verbose_process(
                process=self._process,
                process_name="qemu",
                logger=logger,
                check=False,
                timeout=self._timeout,
            )


class QemuControlled:
    def __init__(self, qmp_controller):
        self._qmp_controller = qmp_controller

    def __enter__(self):
        logger = logging.getLogger(__name__)
        with utils.StepResultLogger(
            logger, "Accept connection from QEMU to QMP monitor"
        ):
            self._qmp_controller.accept()

    def __exit__(self, *exc):
        logger = logging.getLogger(__name__)
        with utils.StepResultLogger(logger, "Quit QEMU"):
            self._qmp_controller.command("quit")


def read_events(qmp_controller):
    logger = logging.getLogger(__name__)
    logger.debug("Read QEMU events")
    while qmp_controller.pull_event():
        pass


def wait_shutdown(qmp_controller):

    logger = logging.getLogger(__name__)

    with utils.StepResultLogger(logger, "Wait until the VM is powered down"):
        while qmp_controller.pull_event(wait=True)["event"] != "SHUTDOWN":
            pass

    with utils.StepResultLogger(logger, "Wait until the VM is stopped"):
        while qmp_controller.pull_event(wait=True)["event"] != "STOP":
            pass


def get_qmp_args(qmp_path):

    return [
        "-chardev",
        "socket,id=id_char_qmp,path=" + qmp_path,
        "-mon",
        "chardev=id_char_qmp,mode=control",
    ]


def get_network_interface_args(interface_index, interface_name):

    packet_capture_filename = f"link{interface_index}.pcap"
    netdev_id = f"id_net{interface_index}"

    return [
        "-netdev",
        f"tap,id={netdev_id},ifname={interface_name},script=no,downscript=no",
        "-device",
        f"e1000,netdev={netdev_id}",
        "-object",
        f"filter-dump,id=id_dump{interface_index},netdev={netdev_id},file="
        + packet_capture_filename,
    ]


def get_network_interfaces_args(tap_interfaces):

    args = []
    for interface_index, interface_name in enumerate(tap_interfaces):
        args.extend(get_network_interface_args(interface_index, interface_name))
    return args


def get_serial_port_args(tcp_port):

    return [
        "-chardev",
        f"socket,id=id_char_serial,port={tcp_port},"
        "host=127.0.0.1,ipv4,nodelay,server,nowait,telnet",
        "-serial",
        "chardev:id_char_serial",
    ]


def get_uefi_firmware_args(ovmf_vars_path):

    args = []

    # firmware executable code
    args.append("-drive")
    args.append(
        "if=pflash,format=raw,unit=0,readonly,file=/usr/share/OVMF/OVMF_CODE.fd"
    )

    # firmware variable store
    args.append("-drive")
    args.append("if=pflash,format=raw,unit=1,file=" + ovmf_vars_path)

    return args
