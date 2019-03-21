from django.dispatch import Signal


create_rating = Signal(
    use_caching=True)

update_rating = Signal(
    providing_args=['instance', 'user_from'],
    use_caching=True)

delete_rating = Signal(
    providing_args=['instance', 'user_from'],
    use_caching=True)
