# -*- coding: utf-8 -*-
#
# Copyright 2019 SoloKeys Developers
#
# Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
# http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
# http://opensource.org/licenses/MIT>, at your option. This file may not be
# copied, modified, or distributed except according to those terms.

import sys

import click
from cryptography.hazmat.primitives import hashes
from fido2.client import ClientError as Fido2ClientError
from fido2.ctap1 import ApduError

import solo
from solo.cli.update import update
import solo.fido2


# https://pocoo-click.readthedocs.io/en/latest/commands/#nested-handling-and-contexts
@click.group()
def key():
    """Interact with Solo keys, see subcommands."""
    pass


@click.group()
def rng():
    """Access TRNG on key, see subcommands."""
    pass


@click.command()
@click.option("--count", default=8, help="How many bytes to generate (defaults to 8)")
@click.option("-s", "--serial", help="Serial number of Solo to use")
def hexbytes(count, serial):
    """Output COUNT number of random bytes, hex-encoded."""
    if not 0 <= count <= 255:
        print(f"Number of bytes must be between 0 and 255, you passed {count}")
        sys.exit(1)

    print(solo.client.find(serial).get_rng(count).hex())


@click.command()
@click.option("-s", "--serial", help="Serial number of Solo to use")
def raw(serial):
    """Output raw entropy endlessly."""
    p = solo.client.find(serial)
    while True:
        r = p.get_rng(255)
        sys.stdout.buffer.write(r)


@click.command()
@click.option("-s", "--serial", help="Serial number of Solo use")
@click.argument("hash-type")
@click.argument("filename")
def probe(serial, hash_type, filename):
    """Calculate HASH."""

    hash_type = hash_type.upper()
    assert hash_type in ("SHA256", "SHA512")

    data = open(filename, "rb").read()
    # < CTAPHID_BUFFER_SIZE
    # https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html#usb-message-and-packet-structure
    # also account for padding (see data below....)
    # so 6kb is conservative
    assert len(data) <= 6 * 1024

    p = solo.client.find(serial)
    import fido2

    serialized_command = fido2.cbor.dumps({"subcommand": hash_type, "data": data})
    from solo.commands import SoloBootloader

    result = p.send_data_hid(SoloBootloader.HIDCommandProbe, serialized_command)
    print(result.hex())
    # print(fido2.cbor.loads(result))


# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo use")
# @click.argument("filename")
# def sha256sum(serial, filename):
#     """Calculate SHA256 hash of FILENAME."""

#     data = open(filename, 'rb').read()
#     # CTAPHID_BUFFER_SIZE
#     # https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html#usb-message-and-packet-structure
#     assert len(data) <= 7609
#     p = solo.client.find(serial)
#     sha256sum = p.calculate_sha256(data)
#     print(sha256sum.hex().lower())

# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo use")
# @click.argument("filename")
# def sha512sum(serial, filename):
#     """Calculate SHA512 hash of FILENAME."""

#     data = open(filename, 'rb').read()
#     # CTAPHID_BUFFER_SIZE
#     # https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html#usb-message-and-packet-structure
#     assert len(data) <= 7609
#     p = solo.client.find(serial)
#     sha512sum = p.calculate_sha512(data)
#     print(sha512sum.hex().lower())


@click.command()
@click.option("-s", "--serial", help="Serial number of Solo use")
def reset(serial):
    """Reset key - wipes all credentials!!!"""
    if click.confirm(
        "Warning: Your credentials will be lost!!! Do you wish to continue?"
    ):
        print("Press the button to confirm -- again, your credentials will be lost!!!")
        solo.client.find(serial).reset()
        click.echo("....aaaand they're gone")


@click.command()
@click.option("-s", "--serial", help="Serial number of Solo use")
@click.option(
    "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
)
def verify(serial, udp):
    """Verify key is valid Solo Secure or Solo Hacker."""

    if udp:
        solo.fido2.force_udp_backend()

    # Any longer and this needs to go in a submodule
    print("Please press the button on your Solo key")
    try:
        cert = solo.client.find(serial).make_credential()
    except Fido2ClientError:
        print("Error getting credential, is your key in bootloader mode?")
        print("Try: `solo program aux leave-bootloader`")
        sys.exit(1)

    solo_fingerprint = b"r\xd5\x831&\xac\xfc\xe9\xa8\xe8&`\x18\xe6AI4\xc8\xbeJ\xb8h_\x91\xb0\x99!\x13\xbb\xd42\x95"
    hacker_fingerprint = b"\xd0ml\xcb\xda}\xe5j\x16'\xc2\xa7\x89\x9c5\xa2\xa3\x16\xc8Q\xb3j\xd8\xed~\xd7\x84y\xbbx~\xf7"
    udp_fingerprint = b"\x05\x92\xe1\xb2\xba\x8ea\rb\x9a\x9b\xc0\x15\x19~J\xda\xdc16\xe0\xa0\xa1v\xd9\xb5}\x17\xa6\xb8\x0b8"

    if cert.fingerprint(hashes.SHA256()) == solo_fingerprint:
        print("Valid Solo Secure firmware from SoloKeys")
    elif cert.fingerprint(hashes.SHA256()) == hacker_fingerprint:
        print("Valid Solo Hacker firmware")
    elif cert.fingerprint(hashes.SHA256()) == udp_fingerprint:
        print("Local software key")
    else:
        print("Unknown fingerprint! ", cert.fingerprint(hashes.SHA256()))


@click.command()
@click.option("-s", "--serial", help="Serial number of Solo use")
@click.option(
    "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
)
def version(serial, udp):
    """Version of firmware on key."""

    if udp:
        solo.fido2.force_udp_backend()

    try:
        major, minor, patch = solo.client.find(serial).solo_version()
        print(f"{major}.{minor}.{patch}")
    except solo.exceptions.NoSoloFoundError:
        print("No Solo found.")
        print("If you are on Linux, are your udev rules up to date?")
    except (solo.exceptions.NoSoloFoundError, ApduError):
        # Older
        print("Firmware is out of date (key does not know the SOLO_VERSION command).")


@click.command()
@click.option("-s", "--serial", help="Serial number of Solo use")
@click.option(
    "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
)
def wink(serial, udp):
    """Send wink command to key (blinks LED a few times)."""
    if udp:
        solo.fido2.force_udp_backend()

    solo.client.find(serial).wink()


key.add_command(rng)
rng.add_command(hexbytes)
rng.add_command(raw)
key.add_command(reset)
key.add_command(update)
key.add_command(probe)
# key.add_command(sha256sum)
# key.add_command(sha512sum)
key.add_command(version)
key.add_command(verify)
key.add_command(wink)
