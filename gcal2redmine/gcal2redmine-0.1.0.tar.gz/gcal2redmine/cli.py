#!/usr/bin/env python3

from re import sub, subn

import click

from .gcal import GoogleCalendar
from .redmine import RedmineTimeTracking
from .utils import format_date, strike, validate_date


@click.command()
@click.option("-d", "--dry-run", is_flag=True, help="Print only, make no action.")
@click.option("--no-mark", is_flag=True, help="Do not mark events as processed in Calendar.")
@click.option("--no-track", is_flag=True, help="Do not add track entry in Redmine.")
@click.option(
    "-f",
    "--from-date",
    callback=validate_date,
    default="today",
    help="Must be in format: YYYY-MM-DD, today, yesterday [default=today]",
)
@click.option(
    "-t",
    "--to-date",
    callback=validate_date,
    default="today",
    help="Must be in format: YYYY-MM-DD, today, yesterday [default=today]",
)
def main(dry_run, no_mark, no_track, from_date, to_date):
    gcal = GoogleCalendar(from_date, to_date)
    redmine = RedmineTimeTracking()
    events = []
    total_time = 0.0

    # get and show all events to be added
    for event_id, spent_on, event, hours in gcal.events:
        issue_id = subn(r"^.*#(\d+).*$", r"\1", event)
        comments = sub(r"#\d+$", r"", event)
        spent_on = format_date(spent_on).date()
        if issue_id[1]:
            click.echo(
                "{} | #{}: {} (time: {})".format(spent_on, issue_id[0], comments, hours)
            )
            events.append([event_id, issue_id[0], hours, spent_on, comments])
            total_time += hours

    click.echo("Total time: {}".format(total_time))
    # ask for confirmation before adding
    if click.confirm("Do you want to proceed?") and not dry_run:
        with click.progressbar(events) as events_bar:
            for event in events_bar:
                event_id = event.pop(0)
                if not no_track:
                    redmine.add_time(*event)
                if not no_mark:
                    gcal.mark_event(event_id)
        click.echo("Events successfully added.")
    else:
        click.echo("Nothing have been done.")


if __name__ == "__main__":
    main()
