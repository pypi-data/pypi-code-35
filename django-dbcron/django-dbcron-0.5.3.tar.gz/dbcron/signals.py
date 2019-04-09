from django.dispatch import Signal

job_started = Signal(providing_args=['job'])
job_done = Signal(providing_args=['job'])
job_failed = Signal(providing_args=['job', 'error'])
