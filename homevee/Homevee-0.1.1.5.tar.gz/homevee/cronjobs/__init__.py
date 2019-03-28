#!/usr/bin/python
# -*- coding: utf-8 -*-
from _thread import start_new_thread

from homevee.Helper import Logger
from . import run_automations
from . import save_sensor_data
from . import save_energy_data
from . import user_ping
from . import video_surveillance
from . import zwave_value_loader
from . import philips_hue_value_loader
from . import weather_updater
from . import overview_notification
from . import calendar_reminder
from . import heating_scheme

def start_cronjobs():
    Logger.log("starting cronjobs...")

    # Load Z-Wave values
    start_new_thread(zwave_value_loader.init_thread, ())

    # Load Philips Hue values
    start_new_thread(philips_hue_value_loader.init_thread, ())

    # Save values to database
    start_new_thread(save_sensor_data.init_thread, ())

    # Save values to database
    start_new_thread(save_energy_data.init_thread, ())

    # Update weather cache
    start_new_thread(weather_updater.init_thread, ())

    # User anpingen
    # start_new_thread(cronjobs.user_ping.init_thread, ())

    # Benachrichtigung mit Infos für den Tag senden
    start_new_thread(overview_notification.init_thread, ())

    # Benachrichtigung mit Termin-Erinnerungen
    start_new_thread(calendar_reminder.init_thread, ())

    # Zeitgesteuerte Automatisierungen ausführen
    start_new_thread(run_automations.init_thread, ())

    # Heizplan ausführen
    start_new_thread(heating_scheme.init_thread, ())