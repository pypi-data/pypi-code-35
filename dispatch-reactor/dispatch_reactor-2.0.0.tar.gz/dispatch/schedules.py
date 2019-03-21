from datetime import timedelta, datetime, time

def one_time_schedule(timestamp):
    yield timestamp

def interval_schedule(start=None, days=0, hours=0, minutes=0, seconds=0, miliseconds=0, till=None):
    hours += days * 24
    minutes += hours * 60
    seconds += minutes * 60
    interval = seconds + (miliseconds / 1000)
    if start is None:
        start = datetime.now()
    yield start
    current = start
    while True:
        current = current + timedelta(seconds=interval)
        if till and current >= till:
            break
        yield current

class CalendarSchedule():
    ALL = '*'
    weekdays = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }

    def __init__(self, start=None, days=None, days_of_week=None, hours=None, minutes=None, seconds=None, till=None):
        self.start = start
        self.days = days
        self.days_of_week = days_of_week
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.till = till
        self._determine_specification()
        self._set_defaults() # This NEEDS to come second as the above should remove some of the nulls

        self.last_run = self.start

    def _determine_specification(self):
        """ 
            The defaults change based on the must specifc parameter thats given.
            We assume "Every ___" for each parameter they don't specify as we get
            more specfic. Once we reach a specified parameter we assume "00" as the value
            of every null parameter after it. 

            This allows Calendar(hour=7) to mean every day at 7
            While Calendar(second=4) to mean every minute of every hour of every day on the 4th second

            Since we dont allow seconds to be all by defaut, it means specifying no parameters would
            result in every minute on the 0th second.
        """
        if self.days is not None or self.days_of_week is not None:
            # They specified days so we dont have to do anything
            return True

        # They didnt sepcify days, fallback to every
        self.days = self.ALL
        
        if self.hours is not None:
            return True

        # They didnt sepcify hours, fallback to every
        self.hours = self.ALL

        if self.minutes is not None:
            return True

        # They didnt sepcify minutes, fallback to every
        self.minutes = self.ALL

    def _set_defaults(self):
        if self.hours is None:
            self.hours = [0]
        if self.minutes is None:
            self.minutes = [0]
        if self.seconds is None:
            self.seconds = [0]
        if self.start is None:
            self.start = datetime.now()
        if isinstance(self.days, list):
            self.days.sort()
        if isinstance(self.hours, list):
            self.hours.sort()
        if isinstance(self.minutes, list):
            self.minutes.sort()
        if isinstance(self.seconds, list):
            self.seconds.sort()

        if isinstance(self.days, list):
            for day in self.days:
                if day < 1 or day > 31:
                    raise ValueError('Invalid day of month: ' + str(day))

        validated_weekdays = []
        if self.days_of_week:
            for day in self.days_of_week:
                if isinstance(day, str):
                    mapped_day = self.weekdays.get(day.lower(), None)
                    if mapped_day is None:
                        raise ValueError('Invalid day of week: ' + day)
                    else:
                        validated_weekdays.append(mapped_day)
                else:
                    if day < 0 or day > 6:
                        raise ValueError('Invalid weekday: ' + str(day))
        self.days_of_week = validated_weekdays

    def __iter__(self):
        return self

    def _day_matches(self, timestamp):
        if self.days == self.ALL or self.days_of_week == self.ALL:
            return True
        if self.days is not None and tiemstamp.day in self.days:
            return True
        if self.days_of_week is not None and timestamp.weekday() in self.days_of_week:
            return True
        return False

    def _next_valid_day(self, timestamp):
        day = timestamp
        
        while True:
            day = day + timedelta(days=1)
            if self._day_matches(day):
                break
        # Every time we step days we want to reset the time
        day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        return day

    def _next_choice(self, current, options):
        if not options:
            return None
        choice = None
        for option in options:
            if option > current:
                return option
        return choice

    def _next_valid_time(self, timestamp):
        moment = timestamp.replace()
        day = moment.day
        while day == moment.day:
            if not (self.hours == self.ALL or moment.hour in self.hours):
                next_hour = self._next_choice(moment.hour, self.hours)
                if next_hour is None:
                    # We dont increase the day, we just say no valid time this day
                    return None 
                moment = moment.replace(hour=next_hour, minute=0, second=0)

            if not (self.minutes == self.ALL or moment.minute in self.minutes):
                next_minute = self._next_choice(moment.minute, self.minutes)
                if next_minute is None:
                    moment = moment + timedelta(hours=1)
                    moment = moment.replace(minute=0, second=0)
                    continue
                moment = moment.replace(minute=next_minute, second=0)

            if not (self.seconds == self.ALL or moment.second in self.seconds):
                next_second = self._next_choice(moment.second, self.seconds)
                if next_second is None:
                    moment = moment + timedelta(minutes=1)
                    moment = moment.replace(second=0)
                    continue
                moment = moment.replace(second=next_second)
            return moment
        return None

    def __next__(self):
        current = self.last_run
        # if we aren't even on a valid day take care of that first
        if not self._day_matches(current):
            current = self._next_valid_day(current)

        # if there is a valid time left in this day get it
        next_valid_time = self._next_valid_time(current)
        if next_valid_time is None:
            current = self._next_valid_day(current)
            current = self._next_valid_time(current)
            if current is None:
                raise ValueError('No valid time with this pattern')
        else:
            current = next_valid_time

        # Stop @ till
        if self.till and current >= till:
            raise StopIteration

        # Increase by 1 second so we never return the same value
        self.last_run = current + timedelta(seconds=1) 
        return current
