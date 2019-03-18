from tetrapod.laniidae import connections


connections.configure(
    default={
        'host': '127.0.0.1:8000',
        'schema': 'http',
    },

    super_user={
        'host': '127.0.0.1:8000',
        'schema': 'http',
        'token': 'o8S7u_x_zsbMwHVaEvbKu0mkLAA=',
    },
)
