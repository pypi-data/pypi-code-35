#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime, time, timedelta
from os import environ
from pathlib import Path
from re import sub

from googleapiclient import discovery
import httplib2
from oauth2client import client, tools
from oauth2client.file import Storage
from tzlocal import get_localzone

from .utils import format_date


class GoogleCalendar:
    def __init__(self, from_date="today", to_date="today"):
        """Instanciate attributes."""

        self.config_dir = (
            Path(environ.get("G2C_CONFIG_HOME", default="~/.config/g2c"))
            .expanduser()
            .resolve()
        )
        self.secret_file = Path(self.config_dir, "google.secret.json")
        self.token_file = Path(self.config_dir, "google.token.json")
        self.scopes = "https://www.googleapis.com/auth/calendar"
        self.application_name = "gcal2redmine"
        self.service = self._get_service()
        self.events = self._get_events(from_date, to_date)

    def _get_service(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        """

        Path(self.config_dir).mkdir(mode=0o700, parents=True, exist_ok=True)

        store = Storage(self.token_file)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.secret_file, self.scopes)
            flow.user_agent = self.application_name

            class FakeFlags:
                logging_level = "INFO"
                noauth_local_webserver = False
                auth_host_port = [8080, 8090]
                auth_host_name = "localhost"

            flags = FakeFlags()
            credentials = tools.run_flow(flow, store, flags)
            print("Storing credentials to {}".format(self.token_file))

        http = credentials.authorize(httplib2.Http())
        service = discovery.build("calendar", "v3", http=http)

        return service

    def _get_events(self, from_date="today", to_date="today"):
        local_tz = get_localzone()
        today_morning = datetime.combine(datetime.now().date(), time(0, 0, 0))
        today = local_tz.localize(today_morning).isoformat()

        # start date is assumed to be beginning of the specified day
        if from_date == "today":
            start = today
        elif from_date == "yesterday":
            start = local_tz.localize(today_morning - timedelta(days=1)).isoformat()
        else:
            from_date_morning = datetime(*from_date, 0, 0, 0)
            start = local_tz.localize(from_date_morning).isoformat()

        # end date is assumed to be end of the specified day
        if to_date == "today":
            end = local_tz.localize(today_morning + timedelta(days=1)).isoformat()
        elif to_date == "yesterday":
            end = today
        else:
            to_date_evening = datetime(*to_date, 0, 0, 0) + timedelta(days=1)
            end = local_tz.localize(to_date_evening).isoformat()

        events = list()
        events_params = {
            "calendarId": "primary",
            "timeMin": start,
            "timeMax": end,
            "singleEvents": True,
            "orderBy": "startTime",
        }

        events_result = self.service.events().list(**events_params).execute()
        events_items = events_result.get("items", [])

        for event_item in events_items:
            start = event_item["start"].get("dateTime", event_item["start"].get("date"))
            end = event_item["end"].get("dateTime", event_item["end"].get("date"))
            duration = format_date(end) - format_date(start)
            duration_float = duration.seconds / 3600.0
            events.append(
                (event_item["id"], start, event_item["summary"], duration_float)
            )

        return events

    def mark_event(self, event_id):
        event = (
            self.service.events().get(calendarId="primary", eventId=event_id).execute()
        )
        summary = sub(r"^(.*#)(\d+)$", r"\1!\2", event["summary"])
        event["summary"] = summary
        marked_event = (
            self.service.events()
            .update(calendarId="primary", eventId=event["id"], body=event)
            .execute()
        )

        return marked_event["id"]
