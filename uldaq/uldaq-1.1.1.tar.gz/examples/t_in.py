#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Wrapper call demonstrated:    ai_device.t_in()

    Purpose:                      Reads the user-specified A/D input channels.

    Demonstration:                Displays the analog input temperature data
                                  for each of the user-specified channels.

    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices.
    2. Create a DaqDevice object.
    3. Call daq_device.get_ai_device() to get the ai_device object for the
       analog input subsystem.
    4. Verify the ai_device object is valid.
    5. Verify the device supports temperature channels types.
    6. Call daq_device.connect() to establish a UL connection to the DAQ device.
    7. Call ai_device.t_in() to read a value from an A/D input channel.
    8. Display the data for each channel.
    9. Call daq_device.disconnect() and daq_device.release() before exiting the
       process.
"""
from __future__ import print_function
from time import sleep
from os import system
from sys import stdout

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   TempScale, AiChanType, ULException, ULError)


def main():
    daq_device = None

    descriptor_index = 0
    interface_type = InterfaceType.USB
    low_channel = 0
    high_channel = 3
    scale = TempScale.CELSIUS

    try:
        # Get descriptors for all of the available DAQ devices.
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)
        if number_of_devices == 0:
            raise Exception('Error: No DAQ devices found')

        print('Found', number_of_devices, 'DAQ device(s):')
        for i in range(number_of_devices):
            print('  ', devices[i].product_name, ' (', devices[i].unique_id,
                  ')', sep='')

        # Create the DAQ device object for the specified descriptor index.
        daq_device = DaqDevice(devices[descriptor_index])

        # Get the AiDevice object and verify that it is valid.
        ai_device = daq_device.get_ai_device()
        if ai_device is None:
            raise Exception(
                'Error: The DAQ device does not support analog input')

        # Verify that the DAQ device has temperature channels.
        ai_info = ai_device.get_info()
        chan_types = ai_info.get_chan_types()
        if (AiChanType.TC not in chan_types
                and AiChanType.RTD not in chan_types
                and AiChanType.SEMICONDUCTOR not in chan_types
                and AiChanType.THERMISTOR not in chan_types):
            raise Exception(
                'Error: The DAQ device does not support temperature channels')

        # Establish a connection to the DAQ device.
        descriptor = daq_device.get_descriptor()
        print('\nConnecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()

        print('\n', descriptor.dev_string, ' ready', sep='')
        print('    Function demonstrated: ai_device.t_in()')
        print('    Channels: ', low_channel, '-', high_channel)
        # Display channel configuration information.
        ai_config = ai_device.get_config()
        for chan in range(low_channel, high_channel + 1):
            chan_type = -1
            chan_type_str = 'N/A'
            try:
                chan_type = ai_config.get_chan_type(chan)
                chan_type_str = chan_type.name
            except ULException as ul_error:
                if ul_error.error_code != ULError.CONFIG_NOT_SUPPORTED:
                    raise ul_error

            if chan_type == AiChanType.TC:
                tc_type = ai_config.get_chan_tc_type(chan)
                chan_type_str += ' Type ' + tc_type.name
            elif (chan_type == AiChanType.RTD
                  or chan_type == AiChanType.THERMISTOR):
                connect_type = ai_config.get_chan_sensor_connection_type(chan)
                chan_type_str += ' ' + connect_type.name
            print('        Channel', chan, 'type:', chan_type_str)
        print('    Temperature scaling:', scale.name)

        try:
            input('\nHit ENTER to continue\n')
        except (NameError, SyntaxError):
            pass

        system('clear')

        try:
            while True:
                try:
                    reset_cursor()
                    print('Please enter CTRL + C to terminate the process\n')

                    # Display data for the specified analog input channels.
                    for channel in range(low_channel, high_channel + 1):
                        try:
                            data = ai_device.t_in(channel, scale)
                            print('Channel(', channel, ') Data: ',
                                  '{:10.6f}'.format(data), sep='')
                        except ULException as ul_error:
                            if ul_error.error_code == ULError.OPEN_CONNECTION:
                                print('Channel(', channel, ') Data: ',
                                      'Open Connection', sep='')
                            else:
                                raise ul_error

                    sleep(0.3)
                except (ValueError, NameError, SyntaxError):
                    break

        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()


def reset_cursor():
    stdout.write('\033[1;1H')


if __name__ == '__main__':
    main()
