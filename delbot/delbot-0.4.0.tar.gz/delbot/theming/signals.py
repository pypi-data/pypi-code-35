from django.dispatch import Signal


sample_data_requested = Signal(providing_args=('clear',))
