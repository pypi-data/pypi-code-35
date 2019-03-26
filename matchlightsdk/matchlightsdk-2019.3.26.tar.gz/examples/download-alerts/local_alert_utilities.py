import records


def get_last_saved_alert(db):
    return db.query(
        'SELECT Max(alerts.number) AS max_alert_number FROM alerts'
    )[0]


def get_number_of_local_alerts(db):
    return db.query('SELECT Count(*) as count from alerts')[0].count


def save_new_alert(db, new_alert):
    db.query(
        f'INSERT INTO alerts (id, number) '
        f'VALUES     ("{new_alert.id}", "{new_alert.number}")'
    )


def setup_example_database(db):
    # Create a new example database everytime with some fake data.
    # Tip: In this example we just store the alert number for simplicity
    # but in your application you should store all the alert object
    # metadata.
    # Reference: https://python-matchlightsdk.readthedocs.io/en/latest/api.html#alert
    db.query('DROP TABLE IF EXISTS alerts')
    db.query(
        'CREATE TABLE alerts (id int PRIMARY KEY, number int)'
    )
    db.query(
        'INSERT INTO alerts '
        'VALUES      ("39de2145a1d66330b9d443a84c90d34f", 1)'
    )
    return db
